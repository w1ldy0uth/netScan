#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import ipaddress
import threading
from queue import Queue
from scapy.all import IP, ICMP, sr1, getmacbyip
from src.utils.system_utils import get_cidr_address


class Ping:
    """
    This class describes ICMP (classical ping) scanning methods.
    It allows to send ICMP packet to each host and checks if they are alive by answer.
    """

    def __init__(self, verbose: bool, timeout: int, threads: int) -> None:
        """
        Constructor

        Args:
            verbose (bool): if True, prints all the messages about packets.
            timeout (int): sets timeout of packets receiving in seconds.
            threads (int): number of threads to run.
        """

        self.verbose = verbose
        self.threads = threads
        self.timeout = timeout

        self.print_lock = threading.Lock()
        self.q = Queue()

        self.hosts = [str(ip) for ip in ipaddress.IPv4Network(get_cidr_address())]

        self.res = []

    def check_host(self, host: str) -> None:
        """
        Scans target IP and adds to resulting array if it is alive.

        Args:
            host (str): target IP.
        """
        if getmacbyip(host) is not None:
            icmp = IP(dst=host) / ICMP()
            ans = sr1(icmp, timeout=self.timeout, verbose=self.verbose)
            if ans:
                self.res.append(ans.src)

    def threader(self) -> None:
        """Creates and runs a job within a single thread."""
        while True:
            current = self.q.get()
            self.check_host(current)
            self.q.task_done()

    def get_results(self) -> list:
        """
        Runs all threads and gathers IPs of alive hosts.

        Returns:
            list: IPs of alive hosts.
        """
        for _ in range(self.threads):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()

        for curr in self.hosts:
            self.q.put(curr)

        self.q.join()

        return self.res


if __name__ == "__main__":
    scan = Ping(verbose=False, timeout=5, threads=100)
    print(scan.get_results())
