# netScan

## About

**netScan** is an application built on Python and utilizes the Scapy network tool as its foundation. Its primary objective is to offer user-friendly tools for conducting comprehensive audits of local networks. These tools encompass a diverse array of scanners and application routines.

The application employs three principal scanning techniques, each of which relies on different network protocols: ARP, ICMP, and TCP. The first two methods serve the purpose of identifying hosts within the local network, while the third method extracts port-related information from a specified host. All these methods have been meticulously designed and implemented with multithreading capabilities, enhancing their efficiency and performance.

## Warning

Although this application is meant to be compatible with multiple platforms, it's crucial to acknowledge that the Windows and macOS versions have not undergone testing. As a result, it may be unstable or cause unexpected behavior. Therefore, I strongly recommend using this application cautiously on macOS and Windows devices until further testing and improvements are carried out.

## Requirements

+ Python 3.6+
+ winpcap or npcap (preferably) *for Windows*

## Usage

### Linux & macOS

```bash
./init.sh
source netscan_env/bin/activate
sudo python -m src.main
```

### Windows

```bat
./init.sh
call netscan_env/bin/activate
python -m src.main
```
