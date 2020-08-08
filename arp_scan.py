#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import ARP, srp, Ether
from datetime import datetime

ip_range = "192.168.10.1/24"

def arpscan():
    print("ARP-scan started...")
    print("-"*40 + "\n")

    start_time = datetime.now()

    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    answer = srp(ether/arp, timeout=3, verbose=0)[0]

    res = []

    for sent, recieved in answer:
        res.append({'IP': recieved.psrc, 'MAC': recieved.hwsrc})

    print("Devices in current network:")
    print("IP" + 20*" " + "MAC")
    for device in res:
        print("{:16}     {}".format(device['IP'], device['MAC']))

    print("\n" + "-"*40)
    print("ARP-scan ended")

    end_time = datetime.now()

    print("Duration: ", end_time - start_time)

if __name__ == '__main__':
    arpscan()
