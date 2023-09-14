#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import threading
import random
from queue import Queue
from scapy.all import IP, ICMP, TCP, sr1, sr
from src.utils.system_utils import get_ip_address


class Port:
    """
    This class describes TCP (port) scanning methods.
    It allows to send 3-way TCP handshakes to each host and check target ports.
    """

    def __init__(self, verbose: bool, ip: str, port_begin: int, port_end: int, timeout: int, threads: int) -> None:
        """
        Constructor

        Args:
            verbose (bool): if True, prints messages to console
            ip (str): target IP address
            port_begin (int): first port to scan
            port_end (int): last port to scan
            threads (int): number of threads
        """

        self.verbose = verbose
        self.timeout = timeout
        self.ip = ip
        self.threads = threads
        self.port_begin = port_begin
        self.port_end = port_end

        self.print_lock = threading.Lock()
        self.q = Queue()

        self.open, self.closed, self.dropped = [], [], []

    def check_port(self, target_port: int) -> None:
        """
        Scans each port by performing 3-way TCP handshake.

        Args:
            target_port (int): port to scan
        """
        source_port = random.randint(1025, 65534)  # random source port for scanning from
        rsp = sr1(
            IP(dst=self.ip) / TCP(sport=source_port, dport=target_port, flags="S"),  # TCP packet to send
            timeout=1,
            verbose=self.verbose
        )

        if str(type(rsp)) == "<class 'NoneType'>":  # if type is None, port state is undefined
            self.dropped.append(self.ip + ":" + str(target_port))
        elif rsp.haslayer(TCP):
            if rsp.getlayer(TCP).flags == 0x12:  # with this code port is opened
                sr(IP(dst=target_port) / TCP(sport=source_port, dport=target_port, flags="R"), timeout=1)
                self.open.append(self.ip + ":" + str(target_port))
            elif rsp.getlayer(TCP).flags == 0x14:  # with this code port is closed
                self.closed.append(self.ip + ":" + str(target_port))
        elif rsp.haslayer(ICMP):
            # with one of these codes port state is undefined
            if int(rsp.getlayer(ICMP).type) == 3 and int(rsp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                self.dropped.append(self.ip + ":" + str(target_port))

    def threader(self) -> None:
        """Creates and runs a job within a single thread."""
        while True:
            current = self.q.get()
            self.check_port(current)
            self.q.task_done()

    def get_results(self) -> list:
        """
        Runs all threads and gathers ports info of target host.

        Returns:
            list: Ports of target hosts.
        """
        for _ in range(self.threads):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()

        for curr in range(self.port_begin, self.port_end):
            self.q.put(curr)

        self.q.join()

        info = [self.open, self.closed, self.dropped]
        return info


if __name__ == "__main__":
    scan = Port(verbose=False, ip=get_ip_address(), port_begin=1, port_end=100, timeout=3, threads=100)
    print(scan.get_results())
