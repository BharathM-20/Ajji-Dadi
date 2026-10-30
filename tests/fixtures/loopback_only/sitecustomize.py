"""Limit isolated Gradio launch probes (and their children) to loopback sockets."""

import ipaddress
import socket
import sys


def local_host(host):
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except (ValueError, TypeError):
        return False


def local_network_only(event, args):
    if event in {"socket.connect", "socket.bind", "socket.sendto", "socket.sendmsg"}:
        if args[0].family == socket.AF_UNIX:
            return
        # sendmsg and sendto audit arguments both end with the destination address.
        address = args[-1]
        if not isinstance(address, tuple) or not local_host(address[0]):
            raise RuntimeError(
                "ERROR: external socket blocked. WHY: UI probe is localhost-only. "
                "FIX: use MOCK=True and 127.0.0.1."
            )
    elif event in {
        "socket.getaddrinfo",
        "socket.gethostbyname",
        "socket.gethostbyaddr",
        "socket.getnameinfo",
    }:
        host = args[0][0] if isinstance(args[0], tuple) else args[0]
        if not local_host(host):
            raise RuntimeError(
                "ERROR: external DNS blocked. WHY: UI probe is localhost-only. "
                "FIX: use 127.0.0.1 instead of an external host."
            )


sys.addaudithook(local_network_only)
