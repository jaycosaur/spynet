import threading
import typing
import time

import cv2
import imagezmq

from .network import (
    Network,
    NetworkHandler,
    NetworkService,
    ServiceType,
)
from .camera import CameraBase
from .utils import image as image_utils

ImageFilterCallable = typing.Callable[[typing.Any], bool]


class CameraNode(threading.Thread):
    def __init__(
        self,
        hub: NetworkService,
        camera: CameraBase,
        node_id: str,
        network_id: str,
        image_filter: typing.Optional[ImageFilterCallable],
    ):
        if not isinstance(camera, CameraBase):
            raise AttributeError("camera must subclass the CameraBase class")
        self._network_id = network_id
        super().__init__(name=repr(self), daemon=True)
        self.hub = hub
        self.camera = camera
        self.node_id = node_id
        self._is_stopped = False
        if image_filter:
            self._image_filter = image_filter
        else:
            self._image_filter = lambda _: True

    def __repr__(self) -> str:
        return f"Node(network_id={self._network_id})"

    def run(self):
        sender = imagezmq.ImageSender(
            connect_to="tcp://" + str(self.hub.ip_addr) + ":" + str(self.hub.port)
        )
        while not self._is_stopped:
            ok, image = self.camera.read()
            if not ok:
                continue

            image_pass = self._image_filter(image)

            if image_pass:
                sender.send_image(self.node_id, image)

        print(f"Node {self.node_id} Finished")

    def stop(self):
        self._is_stopped = True


class Discovery(NetworkHandler):
    services: typing.List[NetworkService] = []
    hub: typing.Optional[NetworkService] = None
    node: typing.Optional[CameraNode] = None

    def __init__(
        self,
        node_id: str,
        network_id: str,
        camera: CameraBase,
        image_filter: typing.Optional[ImageFilterCallable] = None,
    ):
        self.camera = camera
        self.node_id = node_id
        self.network_id = network_id
        self.image_filter = image_filter

    def __len__(self):
        return len(self.services)

    def on_service_added(self, service: NetworkService):
        self.services.append(service)
        print(f"Now have {len(self)} active services.")
        if service.service_type is ServiceType.HUB:
            print("Hub has come online. Registering")
            self.hub = service
            self.node = CameraNode(
                node_id=self.node_id,
                hub=self.hub,
                camera=self.camera,
                network_id=self.network_id,
                image_filter=self.image_filter,
            )
            self.node.start()

    def on_service_removed(self, removed_service: NetworkService):
        for idx, service in enumerate(self.services):
            if service.service_id == removed_service.service_id:
                self.services.pop(idx)
        if service.service_type is ServiceType.HUB:
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
        self,
        node_id: str,
        camera: CameraBase,
        network_id: str,
        port=8080,
        image_filter: typing.Optional[ImageFilterCallable] = None,
    ):
        self.node_id = node_id
        self.camera = camera
        self.network_id = network_id
        self.service = Network(
            service_type=ServiceType.NODE,
            port=8080,
            network_id=network_id,
            network_handler=Discovery(
                node_id=self.node_id,
                network_id=self.network_id,
                camera=self.camera,
                image_filter=image_filter,
            ),
            service_id=self.node_id,
        )

    def start(self):
        self.service.start()

    def stop(self):
        self.service.stop()
