import threading

import cv2
import imagezmq

from .network import NetworkHandler, Network, HUB_TYPE


class Discovery(NetworkHandler):
    def on_service_added(self, service):
        print("ADDED", service)

    def on_service_removed(self, service):
        print("REMOVED", service)


class Hub(threading.Thread):
    def __init__(self, network_id: str, message_handler, port=5555):
        super().__init__(name=f"Hub(network_id={network_id})")
        self.message_hub = imagezmq.ImageHub(open_port=f"tcp://*:{port}")
        self.service = Network(
            service_type=HUB_TYPE,
            port=port,
            network_id=network_id,
            network_handler=Discovery(),
        )
        self._is_message_handler_stopped = False
        self.message_handler = message_handler

    def run(self):
        while not self._is_message_handler_stopped:
            cam_id, image = self.message_hub.recv_image()
            self.message_handler(cam_id, image)
            self.message_hub.send_reply(b"OK")

    def start(self):
        self.service.start()
        super().start()

    def stop(self):
        self._is_message_handler_stopped = True
        self.service.stop()
