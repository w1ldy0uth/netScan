#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import ipaddress
import threading
from queue import Queue
from scapy.all import IP, ICMP, sr1, getmacbyip
try:
    from method.sub.ipget import cidr_ip
except ImportError:
    from sub.ipget import cidr_ip


class Ping:
    """A class to recieve IPs of host in current network."""

    def __init__(self, verbose, threads=100) -> None:
        """
        Constructs all the necessary attributes.

        verbose: bool
            permission for output of additional info about packets
        threads: int
            amount of threads (default - 100)
        ip: string
            IPs of hosts in CIDR notation
        hosts: list
            list of IPs of network to check
        res: list
            list of active IPs
        """

        self.verbose = verbose
        
        self.threads = threads
        self.print_lock = threading.Lock()
        self.q = Queue()

        ip = cidr_ip()
        self.hosts = [str(ip) for ip in ipaddress.IPv4Network(ip)]
        self.res = []

    def scan(self, ipaddr) -> None:
        """Scans network and catches active IPs."""

        if getmacbyip(ipaddr) is None: # checks if host's MAC cannot be resolved
            pass
        else: # checks if host is online (for assurance)
            icmp = IP(dst=ipaddr)/ICMP() # icmp packet to send
            ans = sr1(icmp, timeout=5, verbose=self.verbose) # sending a request 
            if ans:
                self.res.append(ipaddr) # keeping an answered host's IP

    def threader(self) -> None:
        """Creates a single thread."""

        while True:
            current = self.q.get()
            self.scan(current)
            self.q.task_done()

    def main(self) -> list:
        """Makes (magic) threads work and returns IPs."""

        for thread in range(self.threads):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()

        for curr in self.hosts:
            self.q.put(curr)

        self.q.join()

        return self.res


if __name__ == "__main__":
    scan = Ping(verbose=False, threads=100)
    print(scan.main())
