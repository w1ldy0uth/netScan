#!/usr/bin/env python3
# -*- coding: UTF=8 -*-

import os


def root():
    if os.geteuid() != 0:
        print("Access denied. Run this program as root.")
        exit()

def main():
    root()


if __name__ == "__main__":
    main()