netScan
=====

netScan is a Python based application with using Scapy library. Its main task is to provide convenient tools for auditing a local network, such as wide range of scanners and application routines.

How the application works
=====

There are 3 main scanning methods, each based on ARP, ICMP and TCP protocols. The first two are used to get hosts on the local network, while the third method gets the port information of the selected host. All methods was designed and made multithreaded.

#### Main methods:

+ ARP scan: uses `srp` function to send and recieve packets on layer 2, multithreaded by default;
+ Ping (ICMP) scan: uses `sr1` function to send and recieve packets on layer 3, multithreaded with Python standard library tools;
+ Port (TCP) scan: uses `sr1` and `sr` functions to send and recieve packets on layer 3, multithreaded with Python standard library tools;

#### Sub methods:

+ Interface getter: returns current network interface of running host, uses bash script;
+ IP getter: returns the IP of running host and CIDR IP /24 block, uses bash script;
+ MAC getter: returns the MAC of running host, uses bash script;

Disclamer
=====

This application is meant to be crossplatform. However, there are stil Windows and macOS versions has not been tested yet, so they could be unstable. At this point, I warn you to use this app very carefully on macOS and Windows devices.

Requirements
=====

The program requires the following components:

+ Python 3.6+
+ Scapy 2.4.5
+ git
+ npcap or winpcap (for Windows users)
+ getmac python library

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
