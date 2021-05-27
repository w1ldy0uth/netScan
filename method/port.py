#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import IP, ICMP, TCP, sr1
from sub.ipget import get_ip
import threading 
import random
from queue import Queue


class Port:
    def __init__(self, verbose, ip, port_begin, port_end):
        self.verbose = verbose
        self.ip = str(ip)[:-1:]

        self. threads = 100
        self.print_lock = threading.Lock()
        self.q = Queue()
    
        self.port_begin = port_begin
        self.port_end = port_end

    def scan(self, dst):
        src = random.randint(1025, 65534)
        rsp = sr1(
            IP(dst=self.ip)/TCP(sport=src, dport=dst, flags='S'),
            timeout=1, verbose=0)

        if rsp is None:
            print("{}:{} is filtered (silently dropped)".format(self.ip, dst))

        elif rsp.haslayer(TCP):
            if rsp.getlayer(TCP).flags == 0x12:
                send_rst = sr1(
                    IP(dst=self.ip)/TCP(sport=src, dport=dst, flags='R'),
                    timeout=1, verbose=0)
                print("{}:{} is open".format(self.ip, dst))

            elif rsp.getlayer(TCP).flags == 0x14:
                print("{}:{} is closed".format(self.ip, dst))

        elif rsp.haslayer(ICMP):
            if (int(rsp.getlayer(ICMP).type) == 3) and (int(rsp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                print("{}:{} is filtered (silently dropped)".format(self.ip, dst))
    
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
            
        for curr in range(self.port_begin, self.port_end):
            self.q.put(curr)

        self.q.join()


if __name__ == "__main__":
    scan = Port(verbose=False, ip=get_ip(), port_begin=1, port_end=100)
    scan.work_process()