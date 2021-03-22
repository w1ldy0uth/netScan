import platform
import subprocess


def getip():
    if platform.system() == 'Linux':
        ip = subprocess.check_output(
            ["bash", "-c",
             "hostname --all-ip-addresses"]).decode("utf-8")[:-1:]

        return ip

    elif platform.system() == 'Darwin':
        output = subprocess.check_output(
            ["bash", "-c",
             "ifconfig | grep 'inet ' | grep -v 127.0.0.1"]).decode("utf-8")
        output = output[6:-1:]

        ip = ""
        for i in output:
            if i != " ":
                ip += i
            else:
                break

        return ip


def cidrip():
    ip = getip()

    while ip[-1] != '.':
        ip = ip[:-1:]

    return ip + '0/24'


if __name__ == '__main__':
    print(getip())
