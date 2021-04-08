#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import platform
import subprocess


def get_iface():
    if platform.system() == 'Windows':
        from scapy.all import get_windows_if_list, get_if_list

        winList = get_windows_if_list()
        intfList = get_if_list()

        # Pull guids and names from the windows list
        guidToNameDict = {e["guid"]: e["name"] for e in winList}

        # Extract the guids from the interface list
        guidsFromIntfList = [(e.split("_"))[1] for e in intfList]

        # Using the interface list of guids, pull the names from the
        # Windows map of guids to names
        namesAllowedList = [guidToNameDict.get(e) for e in guidsFromIntfList]

        return namesAllowedList

    elif platform.system() == "Linux":
        iface = subprocess.check_output(
            ["bash", "-c", "route | grep default | awk '{print $8}'"])

        return iface.decode("utf-8")[:-1:]


if __name__ == '__main__':
    print(get_iface())
