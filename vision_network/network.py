from threading import Event, Thread
from dataclasses import dataclass, asdict
import typing
from abc import ABC, abstractmethod
import uuid

from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo
from .utils import ip as util_ip


HUB_TYPE = "HUB"
NODE_TYPE = "NODE"
SERVICE_TYPES = (HUB_TYPE, NODE_TYPE)


@dataclass
class NetworkService:
    service_type: str
    service_id: str
    ip_addr: str
    port: int
    network_id: str


def get_about_service(zeroconf, type, name) -> typing.Optional[NetworkService]:
    info = zeroconf.get_service_info(type, name)
    if not info:
        return
    service_type = info.properties.get(b"type")
    if service_type:
        service_type = service_type.decode("utf-8")
    service_id = info.properties.get(b"id")
    if service_id:
        service_id = service_id.decode("utf-8")
    service_network_id = info.properties.get(b"network_id")
    if service_network_id:
        service_network_id = service_network_id.decode("utf-8")
    addresses = info.addresses
    port = info.port
    if (
        service_type in SERVICE_TYPES
        and service_type
        and service_id
        and service_network_id
    ):
        return NetworkService(
            service_type=service_type,
            service_id=service_id,
            ip_addr=[util_ip.unpack_ip(ip) for ip in addresses][0],
            port=info.port,
            network_id=service_network_id,
        )
    else:
        print(
            f"Unknown service {name} discovered at addresses:",
            [util_ip.unpack_ip(ip) for ip in addresses],
            "port",
            port,
        )


class NetworkHandler(ABC):
    @abstractmethod
    def on_service_added(self, service: NetworkService) -> None:
        ...

    @abstractmethod
    def on_service_removed(self, service: NetworkService) -> None:
        ...


class ServiceListener:
    def __init__(self, service_id: str, handler: NetworkHandler):
        if not isinstance(handler, NetworkHandler):
            raise AttributeError(
                "handler must subclass abstract base class NetworkHandler"
            )

        self._service_id = service_id
        self._handler = handler

    def remove_service(self, zeroconf, type, name):
        service_info = get_about_service(zeroconf, type, name)
        if service_info and service_info.service_id != self._service_id:
            self._handler.on_service_removed(service_info)

    def add_service(self, zeroconf, type, name):
        service_info = get_about_service(zeroconf, type, name)
        if service_info and service_info.service_id != self._service_id:
            self._handler.on_service_added(service_info)


class Network(Thread):
    def __init__(
        self,
        service_type: str,
        port: int,
        network_id: str,
        network_handler: NetworkHandler,
        service_id: str = str(uuid.uuid4()),
    ):
        if not isinstance(network_handler, NetworkHandler):
            raise AttributeError(
                "network_handler must subclass abstract base class NetworkHandler"
            )

        super().__init__(name=f"Network(service_id={service_id})", daemon=True)
        self.service_id = service_id
        self.service_type = service_type
        self.port = port
        self.network_id = network_id
        self.network_handler = network_handler
        self._is_stopped = False
        self._stop_event = Event()

    def __repr__(self) -> str:
        return "Network(service_id=%s,service_type=%s,network_id=%s,port=%s)" % (
            self.service_id,
            self.service_type,
            self.network_id,
            self.port,
        )

    def run(self):
        print(str(self))
        ip = util_ip.get_ip()
        info = ServiceInfo(
            "_http._tcp.local.",
            f"{self.service_type}-{self.service_id}._http._tcp.local.",
            addresses=[util_ip.get_packed_ip(ip)],
            port=self.port,
            properties={
                "type": self.service_type,
                "id": self.service_id,
                "network_id": self.network_id,
            },
        )

        zeroconf = Zeroconf()
        zeroconf.register_service(info)
        listener = ServiceListener(
            service_id=self.service_id, handler=self.network_handler
        )
        browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

        try:
            self._stop_event.wait()
        finally:
            browser.cancel()
            zeroconf.unregister_service(info)
            zeroconf.close()

    def stop(self):
        self._is_stopped = True
        self._stop_event.set()
