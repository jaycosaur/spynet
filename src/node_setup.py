import threading
import typing
from abc import ABC, abstractmethod

import imagezmq

from .network import NetworkService


class CameraBase(ABC):
    @abstractmethod
    def read(self) -> typing.Tuple[bool, typing.Any]:
        ...

    @abstractmethod
    def release(self) -> None:
        ...


class CameraNode(threading.Thread):
    def __init__(
        self,
        hub: NetworkService,
        camera: CameraBase,
        node_id: str,
        group=None,
        target=None,
        name=None,
        args=(),
        kwargs=None,
    ):
        if not isinstance(camera, CameraBase):
            raise AttributeError("camera must subclass the CameraBase class")
        super().__init__(group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
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
