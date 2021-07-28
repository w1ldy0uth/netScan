#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import platform
import subprocess
try:
    from sub.iface import get_iface
except ImportError:
    from iface import get_iface


def get_mac() -> str:
    """Returns the current MAC address of device via bash CLI and web interface"""
    
    if platform.system() == "Linux":
        iface=get_iface()
        mac = subprocess.check_output(["bash", "-c",
                                       "ifconfig " + iface + " | grep ether"])
        return mac.decode("utf-8")[14:31:]
    
    elif platform.system() == "Windows":
        from getmac import get_mac_address
        return get_mac_address()

if __name__ == "__main__":
    print(get_mac())
