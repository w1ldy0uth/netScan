#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import os
import sys
from method.arp import Arp
from method.ping import Ping
from method.port import Port


def root():
    if os.geteuid() != 0:
        print("Access denied. Run this program as root.")
        exit()

def main():
    root()
    if sys.argv[1] in ("-h", "--help"):
        print("Nscan: usage: sudo python main.py [-args] [verbose] [...]",
              "\nSCAN METHODS:",
              "\n\t-a (--arp): ARP scan; requires only verbose",
              "\n\t-p (--ping): ICMP, or just ping, scan; requires verbose and number of threads",
              "\n\t-t (--tcp): TCP, or just port, scan; requires verbose, threads and border ports")
    
    elif sys.argv[1] in ("-a", "--arp"):
        obj = Arp(int(sys.argv[2]))
        out = obj.scan()
        print("IP", " "*10, "MAC")
        for host in out:
            print(host["IP"] + "  " + host["MAC"])
    
    elif sys.argv[1] in ("-p", "--ping"):
        obj = Ping(int(sys.argv[2]), int(sys.argv[3]))
        out = obj.work_process()
        for host in out:
            print("{} is alive".format(host))
    
    elif sys.argf[1] in ("-t", "--tcp"):
        pass

if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("Wrong arguments specified, try again")