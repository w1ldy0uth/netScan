#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import platform
import subprocess
from iface import get_iface


def get_mac(iface=get_iface()):
    if platform.system() == 'Linux':
        mac = subprocess.check_output(['bash', '-c',
                                       'ifconfig '+iface+' | grep ether'])
        return mac.decode('utf-8')[14:31:]


if __name__ == '__main__':
    print(get_mac())
