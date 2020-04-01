import ipaddress
from ifaddr import get_adapters


def get_ip():
    ignore_list = ["lo", "lo0"]
    res = {}
    for iface in get_adapters():
        # ignore "lo" (the local loopback)
        if iface.ips and iface.name not in ignore_list:
            for addr in iface.ips:
                if addr.is_IPv4:
                    res[iface.nice_name] = addr.ip
                    break
    if res.get("wlan"):
        return res.get("wlan")
    elif res.get("en0"):
        return res.get("en0")
    elif res.get("eth0"):
        return res.get("eth0")
    else:
        # We don't know which one. Return the first one.
        return list(res.values())[0]


def get_packed_ip(ip):
    packed = ipaddress.ip_address(ip).packed
    return packed


def unpack_ip(byte_ip):
    return ipaddress.ip_address(byte_ip)
