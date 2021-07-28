#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import os
import sys
import platform
from method.arp import Arp
from method.ping import Ping
from method.port import Port

def root() -> None:
    """Checks if app is run as root"""
    
    if os.geteuid() != 0:
        print("Access denied. Run this program as root.")
        exit()

def main() -> None:
    """Handles arguments of CLI and shows appropriate output"""
    if platform.system() != "Windows":
        root()
    if sys.argv[1] in ("-h", "--help"):
        print("""netScan is a simple application for managing local network hosts' information, made with Python and Scapy. 
Usage: sudo python main.py [-args] [verbose] [...]
SCAN METHODS:
\t-a (--arp): ARP scan; requires only verbose;
\t-p (--ping): ICMP, or just ping, scan; requires verbose and number of threads;
\t-t (--tcp): TCP, or just port, scan; requires verbose, host ip, threads and border ports""")
    
    elif sys.argv[1] in ("-a", "--arp"):
        obj = Arp(int(sys.argv[2]))
        out = obj.scan()
        print("IP", " "*10, "MAC")
        for host in out:
            print(host["IP"] + "  " + host["MAC"])
    
    elif sys.argv[1] in ("-p", "--ping"):
        obj = Ping(int(sys.argv[2]), int(sys.argv[3]))
        out = obj.main()
        for host in out:
            print("{} is alive".format(host))
    
    elif sys.argv[1] in ("-t", "--tcp"):
        obj = Port(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])) 
        out = obj.main()
        opened = out[0]
        closed = out[1]
        filtered = out[2]
        for port in opened:
            print("{} is open".format(port))
        for port in closed:
            print("{} is closed".format(port))
        for port in filtered:
            print("{} is filtered (silently dropped)".format(port))


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("Wrong arguments specified, try again")