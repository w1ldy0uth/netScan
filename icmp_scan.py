#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import concurrent.futures
import ipaddress
from scapy.all import IP, ICMP, sr1
from datetime import datetime
from ip_getter import cidrip

ipr = [str(ip) for ip in ipaddress.IPv4Network(cidrip())]


def icmpscan(ip):
    print("ICMP-scan started...")
    print("-" * 40 + "\n")

    start_time = datetime.now()

    icmp = IP(dst=ip) / ICMP()

    answer = sr1(icmp, timeout=10, verbose=False)

    if answer is None:
        print("Host is down")
    else:
        print("Host is up")

    print("\n" + "-" * 40)
    print("ICMP-scan ended")

    end_time = datetime.now()

    print("Duration: ", end_time - start_time)


def process():
    exec = concurrent.futures.ThreadPoolExecutor(254)
    ping_hosts = [exec.submit(icmpscan, str(ip)) for ip in ipr]


if __name__ == '__main__':
    process()
