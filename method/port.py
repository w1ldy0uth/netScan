#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import threading 
import random
from queue import Queue
from scapy.all import IP, ICMP, TCP, sr1
try:
    from method.sub.ipget import get_ip
except ImportError:
    from sub.ipget import get_ip


class Port:
    """A class to recieve a state of each host's port."""

    def __init__(self, verbose, ip, threads, port_begin, port_end):
        """
        Constructs all the necessary attributes.

        verbose: bool
            permission for output of additional info about packets
        ip: string
            IP of scannable host
        threads: int
            amount of threads (default - 100)
        port_begin, port_end: int, int
            starting and ending ports
        open, closed, dropped: list, list, list:
            list of each type of ports
        """

        self.verbose = verbose
        self.ip = str(ip)

        self. threads = threads
        self.print_lock = threading.Lock()
        self.q = Queue()
    
        self.port_begin = port_begin
        self.port_end = port_end

        self.open = self.closed = self.dropped = []

    def scan(self, dst):
        """Scans each port by performing 3-way TCP hadnshake."""

        src = random.randint(1025, 65534) # random port for scanning from
        rsp = sr1(
            IP(dst=self.ip)/TCP(sport=src, dport=dst, flags='S'), # TCP packet to send
            timeout=1, verbose=0)

        if rsp is None:
            self.dropped.append(self.ip + ":" + str(dst)) # Empty response signals about firewall

        elif rsp.haslayer(TCP):
            if rsp.getlayer(TCP).flags == 0x12: # Code 12 response means that port is open
                send_rst = sr1(
                    IP(dst=self.ip)/TCP(sport=src, dport=dst, flags='R'),
                    timeout=1, verbose=0)
                self.open.append(self.ip + ":" + str(dst))

            elif rsp.getlayer(TCP).flags == 0x14: # Code 14 response says that port is close
                self.closed.append(self.ip + ":" + str(dst))

        elif rsp.haslayer(ICMP): # Codes 1, 2, 3, 9, 10 or 13 response signals about firewall
            if (int(rsp.getlayer(ICMP).type) == 3) and (int(rsp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                self.dropped.append(self.ip + ":" + str(dst))
    
    def threader(self):
        """Creates a single thread."""

        while True:
            current = self.q.get()
            self.scan(current)
            self.q.task_done()
    
    def work_process(self):
        """Makes threads work and returns state of each port from range."""
        
        for thread in range(self.threads):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()
            
        for curr in range(self.port_begin, self.port_end):
            self.q.put(curr)

        self.q.join()

        return self.open, self.closed, self.dropped


if __name__ == "__main__":
    scan = Port(verbose=False, ip=get_ip(), threads=100, port_begin=1, port_end=100)
    print(scan.work_process())