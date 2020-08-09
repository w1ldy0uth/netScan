#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import sys
from scapy.all import IP, ICMP, sr1
from datetime import datetime

ip = sys.argv[1]

def icmpscan():
    print("ICMP-scan started...")
    print("-"*40 + "\n")

    start_time = datetime.now()

    icmp = IP(dst=ip)/ICMP()

    answer = sr1(icmp,timeout=10)

    if answer == None:
        print("Host is down")
    else:
        print("Host is up")

    print("\n" + "-"*40)
    print("ICMP-scan ended")

    end_time = datetime.now()

    print("Duration: ", end_time - start_time)

if __name__ == '__main__':
    icmpscan()
