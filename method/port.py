#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import threading 
import random
from queue import Queue
from scapy.all import IP, ICMP, TCP, sr1, sr
try:
    from method.sub.ipget import get_ip
except ImportError:
    from sub.ipget import get_ip


class Port:
    """A class to recieve a state of each host's port."""

    def __init__(self, verbose, ip, port_begin, port_end, threads=100) -> None:
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

        self.open, self.closed, self.dropped = [], [], []

    def scan(self, dst) -> None:
        """Scans each port by performing 3-way TCP hadnshake."""

        src = random.randint(1025, 65534) # random port for scanning from
        rsp = sr1(
            IP(dst=self.ip)/TCP(sport=src, dport=dst, flags="S"), # TCP packet to send
            timeout=1, verbose=0)

        if(str(type(rsp))=="<class 'NoneType'>"): # if type is None, port is filtered
            self.dropped.append(self.ip + ":" + str(dst))
        elif(rsp.haslayer(TCP)):
            if(rsp.getlayer(TCP).flags == 0x12): # with this code port is opened
                send_rst = sr(IP(dst=dst)/TCP(sport=src,dport=dst,flags="R"),timeout=1)
                self.open.append(self.ip + ":" + str(dst))
            elif (rsp.getlayer(TCP).flags == 0x14): # with this code port is closed
                self.closed.append(self.ip + ":" + str(dst))
        elif(rsp.haslayer(ICMP)): 
            # with one of this codes port is filtered
            if(int(rsp.getlayer(ICMP).type)==3 and int(rsp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                self.dropped.append(self.ip + ":" + str(dst))
    
    def threader(self) -> None:
        """Creates a single thread."""

        while True:
            current = self.q.get()
            self.scan(current)
            self.q.task_done()
    
    def main(self) -> list:
        """Makes threads work and returns state of each port from range."""
        
        for thread in range(self.threads):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()
            
        for curr in range(self.port_begin, self.port_end):
            self.q.put(curr)

        self.q.join()

        info = [self.open, self.closed, self.dropped] # for understanding purposes
        return info


if __name__ == "__main__":
    scan = Port(verbose=False, ip=get_ip(), port_begin=1, port_end=100, threads=100)
    print(scan.main())