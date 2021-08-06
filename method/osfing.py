#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import sys
import platform
from p0f import P0f


class Fingerprint:
    def __init__(self, verbose, ip) -> None:
        self.verbose = verbose
        self.ip = ip
    
    def main(self):
        p0f = P0f("p0f.sock")
        host_info = p0f.get_info(self.ip, self.verbose)
        p0f.close()
        return host_info['os_flavor']



if __name__ == "__main__":
    if platform.system() == "Windows":
        print("Due to unsupported AF_UNIX socket in Windows based systems, this function is unavailable on your platrofm...",
              "\nWe apologize for the inconvenience", end="")
        sys.exit()
    else:
        osfpt = Fingerprint(False, "192.168.0.1")
        osfpt.main()
