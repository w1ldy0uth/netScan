#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import os
import sys
import platform
from method.arp import Arp
from method.ping import Ping
from method.port import Port
from method.sub.iface import get_iface
from method.sub.ipget import get_ip
from method.sub.macget import get_mac

PATH = "method\sub\ifc.bat"

def root() -> None:
    """Checks if app is run as root"""
    
    if os.geteuid() != 0:
        print("Access denied. Run this program as root.")
        exit()

def help() -> None:
    """Shows help information"""

    print("""\nnetScan is a simple application for managing local network hosts' information, made with Python and Scapy.
 
Usage: sudo python main.py [-method] [verbose] [-args] [...]

SCAN METHODS:
\t-a (--arp): ARP scan; requires only verbose;
\t-p (--ping): ICMP, or just ping, scan; requires only verbose;
\t-t (--tcp): TCP, or just port, scan; requires verbose, host ip and ports interval (from where to where).
OTHER METHODS:
\t-i (--info): shows main info about current running host (IP, MAC, network interfaces)

If unexpected errors occur while the program is running, contact with developer 
by leaving an issue on GitHub repository page or by email: shurygin1vs@gmail.com""")

def main() -> None:
    """Handles arguments of CLI and shows appropriate output"""
    if platform.system() != "Windows":
        root()

    if sys.argv[1] in ("-h", "--help"):
        help()
    
    elif sys.argv[1] in ("-a", "--arp"):
        obj = Arp(int(sys.argv[2]))
        out = obj.scan()
        print("IP", " "*10, "MAC")
        for host in out:
            print(host["IP"] + "  " + host["MAC"])
    
    elif sys.argv[1] in ("-p", "--ping"):
        obj = Ping(int(sys.argv[2]))
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
    
    elif sys.argv[1] in ("-i", "--info"):
        print("Network interfaces -", get_iface(PATH), "\nIP -", get_ip(), "\nMAC -", get_mac(), end="")


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        help()
