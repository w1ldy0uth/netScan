#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import argparse

import src.utils.system_utils as system_utils
from src.services.arp import Arp
from src.services.icmp import Ping
from src.services.tcp import Port


def print_help() -> None:
    """Shows help information"""

    help_text = """
netScan is a simple application for managing local network information, made with Python and Scapy.

Usage: sudo python main.py [options]

SCAN METHODS:
    -a, --arp             ARP scan; requires verbose.
    -p, --ping, --icmp    ICMP (ping) scan; requires verbose.
    -t, --tcp, --port     TCP (port) scan; requires verbose, host IP, and port range.

OTHER METHODS:
    -i, --info            Show main information about the current host (IP, MAC, network interfaces).
    -h, --help            Show this help message.

Examples:
    sudo python main.py -a -v
    sudo python main.py -t -v 192.168.0.1 80-100

    """
    print(help_text)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="netScan",
        description="Manage local network hosts' information.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
    sudo python -m src.main arp [-t TIMEOUT] [-v]
    sudo python -m src.main ping [-t TIMEOUT] [-th NUMBER_OF_THREADS] [-v]
    sudo python -m src.main tcp [--target TARGET_ADDRESS] [-s START_PORT] [-e END_PORT] [-t TIMEOUT] [-th NUMBER_OF_THREADS] [-v]
    sudo python -m src.main info
        """
    )

    subparsers = parser.add_subparsers(title="SCAN METHODS", dest="scan_method")

    # ARP scan
    arp_parser = subparsers.add_parser("arp", help="Scan local network with ARP packets.")
    arp_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    arp_parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout for scan response")

    # Ping scan
    ping_parser = subparsers.add_parser("ping", help="Ping all hosts in local network with ICMP packets.")
    ping_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    ping_parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout for scan response")
    ping_parser.add_argument("-th", "--threads", type=int, default=100, help="Amount of threads to use")

    # TCP scan
    tcp_parser = subparsers.add_parser("tcp", help="Scan ports of target host with TCP packets.")
    tcp_parser.add_argument("--target", type=str, default=system_utils.get_ip_address(), help="Target IP address")
    tcp_parser.add_argument("-s", "--start_port", type=int, default=0, help="Start of port range")
    tcp_parser.add_argument("-e", "--end_port", type=int, default=1000, help="End of port range")
    tcp_parser.add_argument("-t", "--timeout", type=int, help="Timeout for port scan")
    tcp_parser.add_argument("-th", "--threads", type=int, default=100, help="Amount of threads to use")
    tcp_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    tcp_parser.add_argument("-o", "--open_only", action="store_true", help="Flag for showing only open ports")

    # Information about current host
    parser.add_argument("-i", "--info", action="store_true", help="Show main information about the current host")

    return parser


def main() -> None:
    """Handles arguments of CLI and shows appropriate output"""
    if not system_utils.is_running_as_root():
        print("Access denied. Run this program as root.")
        exit(1)

    parser = parse_args()
    args = parser.parse_args()

    if args.scan_method == "arp":
        print(f"Running ARP scan with {args.timeout} seconds timeout")
        scanner = Arp(verbose=args.verbose, timeout=args.timeout)
        scanner.scan()
        results = scanner.get_results()

        print("IP".ljust(15) + "MAC")
        for host in results:
            print(f"{host['IP'].ljust(15)}{host['MAC']}")

    elif args.scan_method == "ping":
        print(f"Running ICMP scan with {args.timeout} seconds timeout and {args.threads} thread(s)")
        scanner = Ping(verbose=args.verbose, timeout=args.timeout, threads=args.threads)
        results = scanner.get_results()
        for host in results:
            print(f"{host} is alive")

    elif args.scan_method == "tcp":
        print(f"Running TCP scan for {args.target}:{args.start_port}-{args.end_port} with {args.timeout} seconds timeout and {args.threads} thread(s)")
        scanner = Port(
            verbose=args.verbose,
            timeout=args.timeout,
            threads=args.threads,
            ip=args.target,
            port_begin=args.start_port,
            port_end=args.end_port
        )
        results = scanner.get_results()
        opened, closed, filtered = results[0], results[1], results[2]

        print(f"Opened ports: {len(opened)}\n_______________________")
        for port in opened:
            print(f"{port} is open")
        if not args.open_only:
            print(f"Closed ports: {len(closed)}\n_______________________")
            for port in closed:
                print(f"{port} is closed")
            print(f"Filtered ports: {len(filtered)}\n_______________________")
            for port in filtered:
                print(f"{port} is filtered (silently dropped)")

    elif args.info:
        print(
            "HOST INFO:\n____________________________________________",
            "\nNetwork interface ", system_utils.get_network_interface(),
            "\nOS                ", system_utils.get_os_info(),
            "\nIP address        ", system_utils.get_ip_address(),
            "\nMAC address       ", system_utils.get_mac_address(),
            "\nHostname          ", system_utils.get_hostname(),
            "\nBoot time         ", system_utils.get_boot_time(),
            "\nNumber of CPUs    ", system_utils.get_cpu_count(),
            "\nTotal memory      ", system_utils.get_total_memory(),
            end="\n"
        )


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print_help()
