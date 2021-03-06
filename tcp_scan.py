#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import sys
from datetime import datetime
from scapy.all import IP, TCP, sr1, ICMP
import random

ip = sys.argv[1]
ports_input = sys.argv[2]

ports = []
port = ''
first = ''
last = ''
ind = 0

if ports_input.isdigit() is True:
    ports.append(int(ports_input))

elif ',' in ports_input:
    for i in range(len(ports_input)):
        if ports_input[i].isdigit() is True:
            port += ports_input[i]
        elif ports_input[i] == ',':
            ports.append(int(port))
            port = ''
    ports.append(int(port))

elif '-' in ports_input:
    for i in range(len(ports_input)):
        if ports_input[i].isdigit() is True:
            first += ports_input[i]
        elif ports_input[i] == '-':
            ind = i
            break
    for i in range(ind, len(ports_input)):
        if ports_input[i].isdigit() is True:
            last += ports_input[i]
    first = int(first)
    last = int(last)
    print(first, last)
    while True:
        ports.append(first)
        first += 1
        if first > last:
            break


def tcpscan():
    print("TCP-scan started...")
    print("-"*40 + "\n")

    start_time = datetime.now()

    for dst in ports:
        src = random.randint(1025, 65534)
        rsp = sr1(IP(dst=ip)/TCP(sport=src,dport=dst,flags='S'),timeout=1, verbose=0)

        if rsp is None:
            print("{}:{} is filtered (silently dropped)".format(ip, dst))

        elif rsp.haslayer(TCP):
            if rsp.getlayer(TCP).flags == 0x12:
                send_rst = sr1(IP(dst=ip)/TCP(sport=src,dport=dst,flags='R'),timeout=1, verbose=0)
                print("{}:{} is open".format(ip, dst))

            elif rsp.getlayer(TCP).flags == 0x14:
                print("{}:{} is closed".format(ip, dst))

        elif rsp.haslayer(ICMP):
            if (int(rsp.getlayer(ICMP).type) == 3) and (int(rsp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                print("{}:{} is filtered (silently dropped)".format(ip, dst))

    print("\n" + "-"*40)
    print("TCP-scan ended")

    end_time = datetime.now()

    print("Duration: ", end_time - start_time)


if __name__ == '__main__':
    tcpscan()
