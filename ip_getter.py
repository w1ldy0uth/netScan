import platform
import subprocess


def getip():
    if platform.system() == 'Linux':
        ip = subprocess.check_output(
            ["bash", "-c",
             "hostname --all-ip-addresses"]).decode("utf-8")[:-1:]

        return ip


def cidrip():
    ip = getip()

    while ip[-1] != '.':
        ip = ip[:-1:]

    return ip + '0/24'


if __name__ == '__main__':
    print(cidrip())
