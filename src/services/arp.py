#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import ARP, srp, Ether
from src.utils.system_utils import get_cidr_address


class Arp:
    """
    This class describes ARP scanning methods.
    It allows to send ARP announce to multicast address and receive IP and MAC of each host in current network.
    """

    def __init__(self, verbose: bool, timeout: int) -> None:
        """
        Constructor

        Args:
            verbose (boolean): sets verbose mode of packets.
            timeout (int): sets timeout of packets receiving in seconds.
        """
        self.verbose = verbose
        self.timeout = timeout

        self.ip = get_cidr_address()

        self.answer = None
        self.results = []

    def scan(self) -> None:
        """
        Sends packets to multicast and receives answers.
        """
        arp = ARP(pdst=self.ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")

        self.answer = srp(ether/arp, timeout=self.timeout, verbose=self.verbose)[0]

    def get_results(self) -> list:
        """
        Returns results of ARP scan.

        Returns:
            list: IP and MAC of each found host.
        """
        for snd, rcv in self.answer:
            self.results.append({"IP": rcv.psrc, "MAC": rcv.hwsrc})

        return self.results


if __name__ == "__main__":
    scanner = Arp(verbose=False, timeout=10)
    scanner.scan()
    print(scanner.get_results())
