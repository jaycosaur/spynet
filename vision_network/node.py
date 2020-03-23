import threading
import typing
import time

import cv2
import imagezmq

from .network import Network, NetworkHandler, NetworkService, HUB_TYPE, NODE_TYPE
from .camera import CameraBase
from .utils import image as image_utils


class CameraNode(threading.Thread):
    def __init__(
        self, hub: NetworkService, camera: CameraBase, node_id: str, network_id: str,
    ):
        if not isinstance(camera, CameraBase):
            raise AttributeError("camera must subclass the CameraBase class")
        super().__init__(name=f"Node(network_id={network_id})", daemon=True)
        self.hub = hub
        self.camera = camera
        self.node_id = node_id
        self._is_stopped = False

    def run(self):
        sender = imagezmq.ImageSender(
            connect_to="tcp://" + str(self.hub.ip_addr) + ":" + str(self.hub.port)
        )
        while not self._is_stopped:
            ok, image = self.camera.read()
            if ok:
                sender.send_image(self.node_id, image)

        print(f"Node {self.node_id} Finished")

    def stop(self):
        self._is_stopped = True


class Discovery(NetworkHandler):
    services: typing.List[NetworkService] = []
    hub: typing.Optional[NetworkService] = None
    node: typing.Optional[CameraNode] = None

    def __init__(self, node_id: str, network_id: str, camera: CameraBase):
        self.camera = camera
        self.node_id = node_id
        self.network_id = network_id

    def __len__(self):
        return len(self.services)

    def on_service_added(self, service: NetworkService):
        self.services.append(service)
        print(f"Now have {len(self)} active services.")
        if service.service_type == HUB_TYPE:
            print("Hub has come online. Registering")
            self.hub = service
            self.node = CameraNode(
                node_id=self.node_id,
                hub=self.hub,
                camera=self.camera,
                network_id=self.network_id,
            )
            self.node.start()

    def on_service_removed(self, removed_service: NetworkService):
        for idx, service in enumerate(self.services):
            if service.service_id == removed_service.service_id:
                self.services.pop(idx)
        if service.service_type == HUB_TYPE:
            self.hub = None
            if self.node:
                self.node.stop()
                self.node = None

        print(f"Now have {len(self)} active services.")

    def stop(self):
        print(f"Stopping Node")
        if self.node:
            self.node.stop()
            self.node = None


class Node:
    def __init__(
        self, node_id: str, camera: CameraBase, network_id: str, port=8080,
    ):
        self.node_id = node_id
        self.camera = camera
        self.network_id = network_id
        self.service = Network(
            service_type=NODE_TYPE,
            port=8080,
            network_id=network_id,
            network_handler=Discovery(
                node_id=self.node_id, network_id=self.network_id, camera=self.camera,
            ),
            service_id=self.node_id,
        )

    def start(self):
        self.service.start()

    def stop(self):
        self.service.stop()
