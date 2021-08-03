#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import ARP, srp, Ether
try:
    from method.sub.ipget import cidr_ip
except ImportError:
    from sub.ipget import cidr_ip


class Arp:
    """A class to recieve IP and MAC addresses of hosts in current network."""

    def __init__(self, verbose) -> None:
        """
        Constructs all the necessary attributes.

        verbose: bool
            permission for output of additional info about packets 
        """

        self.verbose = verbose
        self.ip = cidr_ip()

    def scan(self) -> list:
        """Scans network and pulls out IPs and MACs from recieved packets."""

        # arp packets's parts (to send)
        arp = ARP(pdst=self.ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")

        ans = srp(ether/arp, timeout=4, verbose=self.verbose)[0] # sending packet to network

        res = [] # storage for addresses

        for snd, rcv in ans:
            res.append({"IP": rcv.psrc, "MAC": rcv.hwsrc}) # pulling out IPs and MACs

        return res


if __name__ == "__main__":
    scanner = Arp(verbose=False) 
    print(scanner.scan())
