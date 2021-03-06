#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import IP, ICMP, sr1
from ip_getter import cidrip
import ipaddress
import concurrent.futures
import sys


class Ping:
    def __init__(self, verbose, ip):
        self.verbose = verbose

        self.hosts = [str(ip) for ip in ipaddress.IPv4Network(ip)]

        self.online_hosts, self.offline_hosts = [], []

    def scanner(self, ipaddr):
        icmp = IP(dst=ipaddr)/ICMP()

        answer = sr1(
            icmp, timeout=5, verbose=self.verbose
        )

        if answer is None:
            self.offline_hosts.append(ipaddr)
        else:
            self.online_hosts.append(ipaddr)

    def return_online(self):
        for ip in self.online_hosts:
            print("{} is online".format(ip))

    def return_offline(self):
        for ip in self.offline_hosts:
            print("{} is offline".format(ip))

    def output(self):
        try:
            if str(sys.argv[1]) == "-all":
                self.return_online()
                self.return_offline()
            elif str(sys.argv[1]) == "-on":
                self.return_online()
            elif str(sys.argv[1]) == "-off":
                self.return_offline()
            else:
                print("Wrong key argument, try again")
        except IndexError:
            print("No key arguments were specified, exiting")
            sys.exit()

    def process(self):
        exec = concurrent.futures.ThreadPoolExecutor(254)
        ping_hosts = [exec.submit(self.scanner, str(ip)) for ip in self.hosts]

        sorted(self.online_hosts)
        sorted(self.offline_hosts)

        self.output()


if __name__ == '__main__':
    scan = Ping(verbose=False, ip=cidrip())
    scan.process()
