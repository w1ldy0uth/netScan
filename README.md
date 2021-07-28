netScan
=====

netScan is a Python based application with using Scapy library. Its main task is to provide convenient tools for auditing a local network, such as wide range of scanners and application routines.

How the application works
=====

There are 3 main scanning methods, each based on ARP, ICMP and TCP protocols. The first to are used to get hosts on the local network, while the third method gets the port information of the selected host. All methods was designed and made multithreaded.

#### Main methods:

+ ARP scan: uses `srp` function to send and recieve packets on layer 2, multithreaded by default;
+ Ping (ICMP) scan: uses `sr1` function to send and recieve packets on layer 3, multithreaded with Python standard library tools;
+ Port (TCP) scan: uses `sr1` and `sr` functions to send and recieve packets on layer 3, multithreaded with Python standard library tools;

#### Sub methods:

+ Interface getter: returns current web interface of running host, uses bash script;
+ IP getter: returns the IP of running host and CIDR IP /24 block, uses bash script;
+ MAC getter: returns the MAC of running host, uses bash script;

Disclamer
=====

This application is meant to be crossplatform. However, there are still no support for Windows system, as well as macOS version has not been tested yet could be unstable. At this point, I warn you to use this app very carefully on macOS platforms. For those who want to implement Windows compatibility in netScan, I recomend you to install `winpcap` first.

Requirements
=====

The program requires the following components:

+ Python 3.6+
+ Scapy 2.4.5
+ git

Make sure that following Python libraries are working properly on your machine:

+ platform
+ subprocess
+ threading
+ queue

Also, make sure that you can run `ifconfig` in bash console interface.

Instalation and usage
=====

```
git clone https://github.com/w1ldy0uth/netScan.git
cd netScan
sudo python main.py --help
```
