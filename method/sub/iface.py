#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import os
import platform
import subprocess

PATH = "ifc.bat"

def get_iface(path) -> str:
    """Returns the current web interface of device"""
    
    if platform.system() == "Windows":
        stream = os.popen(path)
        output = stream.read()
        return output.strip().replace("\n", ", ")

    elif platform.system() in ("Linux", "Darwin"):
        iface = subprocess.check_output(
            ["bash", "-c", "route | grep default | awk '{print $8}'"])

        return iface.decode("utf-8")[:-1:]


if __name__ == "__main__":
    print(get_iface(PATH))
