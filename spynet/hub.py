import threading
import typing

import cv2
import imagezmq

from .network import NetworkHandler, Network, NetworkService, ServiceType


MessageHandler = typing.Callable[[str, typing.Any], None]


class Hub(threading.Thread, NetworkHandler):
    network_services: typing.List[NetworkService] = []

    def __init__(self, network_id: str, message_handler: MessageHandler, port=5555):
        self._network_id = network_id
        super().__init__(name=repr(self))
        self.message_hub = imagezmq.ImageHub(open_port=f"tcp://*:{port}")
        self.service = Network(
            service_type=ServiceType.HUB,
            port=port,
            network_id=network_id,
            network_handler=self,
        )
        self.message_handler = message_handler
        self._is_message_handler_stopped = False
        self._is_started = False

    def __repr__(self) -> str:
        return f"Hub(network_id={self._network_id})"

    def run(self):
        while not self._is_message_handler_stopped:
            cam_id, image = self.message_hub.recv_image()
            self.message_handler(cam_id, image)
            self.message_hub.send_reply(b"OK")
        self._is_started = False

    def start(self):
        if not self._is_started:
            self._is_started = True
            self.service.start()
            super().start()

    def stop(self):
        self._is_message_handler_stopped = True
        self.service.stop()

    def _get_network_service_from_name(
        self, name: str
    ) -> typing.Optional[NetworkService]:
        for service in self.network_services:
            if name == service.name:
                return service

        return None

    def on_service_added(self, service):
        exists = self._get_network_service_from_name(service.name)
        if not exists:
            self.network_services.append(service)

    def on_service_removed(self, service):
        self.network_services = [
            existing_service
            for existing_service in self.network_services
            if service.name == existing_service.name
        ]
