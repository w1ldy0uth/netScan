#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import platform
import socket
import subprocess


def get_ip() -> str:
    """Returns the IP of current device from the bash CLI"""
    
    if platform.system() in ("Linux", "Darwin"):
        ip = subprocess.check_output(
            ["bash", "-c",
             "ifconfig | grep 'inet ' | grep -v 127.0.0.1"]).decode("utf-8")[13:-49:]

        return ip
    
    elif platform.system() == "Windows":
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip

def cidr_ip() -> str:
    """Returns the IP in CIDR notation"""
    ip = get_ip()

    while ip[-1] != '.':
        ip = ip[:-1:]

    return ip + '0/24'


if __name__ == "__main__":
    print(get_ip())
    print(cidr_ip())
