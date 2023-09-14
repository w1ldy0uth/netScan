import os
import psutil
import socket
import getmac
import platform

import src.utils.format_utils as format_utils


def is_running_as_root() -> bool:
    """Checks if app is running as root
    Returns:
        bool: True if app is running as root, False otherwise"""
    if platform.system() != "Windows" and os.geteuid() != 0:
        return False
    return True


def get_network_interface() -> str:
    """Returns the network interface name"""
    interfaces = psutil.net_if_stats()
    for interface, stats in interfaces.items():
        if stats.isup and not interface.startswith("lo"):
            return interface


def get_ip_address() -> str:
    """Returns the IP address of the machine in local network"""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


def get_cidr_address() -> str:
    """Returns the CIDR address of the machine in local network"""
    return get_ip_address().rsplit('.', 1)[0] + '.0/24'


def get_mac_address() -> str:
    """Returns the MAC address of the machine"""
    return getmac.get_mac_address()


def get_os_info() -> str:
    """Returns information about the operating system of the machine"""
    return f"{platform.freedesktop_os_release()['NAME']} {platform.machine()} {platform.release()}"


def get_hostname() -> str:
    """Returns the hostname of the machine"""
    return platform.node()


def get_cpu_count() -> int:
    """Returns the number of CPUs available on the machine"""
    return psutil.cpu_count()


def get_boot_time() -> str:
    """"Returns the boot time of the machine"""
    return format_utils.format_duration(int(psutil.boot_time()))


def get_total_memory() -> str:
    """Returns the total memory of the machine"""
    return format_utils.format_memory(psutil.virtual_memory().total)


if __name__ == "__main__":
    print("Is root") if is_running_as_root() else print("Not root")
    print(get_network_interface())
    print(get_ip_address())
    print(get_cidr_address())
    print(get_mac_address())
    print(get_os_info())
    print(get_hostname())
    print(get_cpu_count())
    print(get_boot_time())
    print(get_total_memory())
