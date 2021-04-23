#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import ARP, srp, Ether
from sub.ipget import cidr_ip, get_ip
from sub.macget import get_mac


class Arp:
    def __init__(self, verbose):
        self.verbose = verbose
        self.ip = cidr_ip()
        print('Your IP address: {}'.format(get_ip()))
        print('Your physical address: {}\n'.format(get_mac()))

    def scan(self):
        arp = ARP(pdst=self.ip)
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')

        ans = srp(ether/arp, timeout=4, verbose=self.verbose)[0]

        self.res = []

        for snd, rcv in ans:
            self.res.append({'IP': rcv.psrc, 'MAC': rcv.hwsrc})

        self.output()

    def output(self):
        print("\nDevices in current network ({}):".format(len(self.res)))

        for device in self.res:
            print("{:16}     {}".format(device['IP'], device['MAC']))


if __name__ == "__main__":
    scanner = Arp(verbose=False)
    scanner.scan()
