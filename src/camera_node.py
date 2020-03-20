import threading
import typing
import time

import cv2
import imagezmq

from .network import Network, NetworkHandler, NetworkService, HUB_TYPE, NODE_TYPE
from .node_setup import CameraNode, CameraBase
from .utils import image as image_utils


class CvCamera(CameraBase):
    def __init__(self, width: int, cam_id=0):
        self.__camera = cv2.VideoCapture(cam_id)
        self.__width = width

    def read(self):
        ok, frame = self.__camera.read()
        if not ok:
            return ok, None

        return ok, image_utils.resize(frame, self.__width)

    def release(self):
        self.__camera.release()


class Discovery(NetworkHandler):
    services: typing.List[NetworkService] = []
    hub: typing.Optional[NetworkService] = None
    node: typing.Optional[CameraNode] = None

    def __init__(self, node_id: str, camera: CameraBase):
        self.camera = camera
        self.node_id = node_id

    def __len__(self):
        return len(self.services)

    def on_service_added(self, service: NetworkService):
        self.services.append(service)
        print(f"Now have {len(self)} active services.")
        if service.service_type == HUB_TYPE:
            print("Hub has come online. Registering")
            self.hub = service
            self.node = CameraNode(
                node_id=self.node_id, hub=self.hub, camera=self.camera
            )
            self.node.start()

    def on_service_removed(self, removed_service: NetworkService):
        for idx, service in enumerate(self.services):
            if service.service_id == removed_service.service_id:
                self.services.pop(idx)
        if service.service_type == HUB_TYPE:
            self.hub = None
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
        self.service = Network(
            service_type=NODE_TYPE,
            port=8080,
            network_id="special",
            network_handler=Discovery(node_id=self.node_id, camera=self.camera,),
            service_id=self.node_id,
        )

    def start(self):
        self.service.start()

    def stop(self):
        self.service.stop()
