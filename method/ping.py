#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import IP, ICMP, sr1, getmacbyip
from sub.ipget import cidr_ip
import ipaddress
import threading
from queue import Queue


class Ping:
    def __init__(self, verbose, ip, threads):
        self.verbose = verbose
        self.threads = 100

        self.print_lock = threading.Lock()
        self.q = Queue()

        self.hosts = [str(ip) for ip in ipaddress.IPv4Network(ip)]
        self.res = []

    def scan(self, ipaddr):
        if getmacbyip(ipaddr) is None:
            pass
        else:
            icmp = IP(dst=ipaddr)/ICMP()
            ans = sr1(icmp, timeout=5, verbose=self.verbose)
            if ans:
                self.res.append(ipaddr)

    def threader(self):
        while True:
            current = self.q.get()
            self.scan(current)
            self.q.task_done()

    def work_process(self):
        for thread in range(self.threads):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()

        for curr in self.hosts:
            self.q.put(curr)

        self.q.join()

        return self.res


if __name__ == '__main__':
    scan = Ping(verbose=False, ip=cidr_ip(), threads=100)
    print(scan.work_process())
