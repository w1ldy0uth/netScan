#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

from scapy.all import IP, ICMP, TCP, sr1
from ip_getter import tcp_ip
import ipaddress
import concurrent.futures
import sys
import random


class Port:
    def __init__(self, ip):
        pass
