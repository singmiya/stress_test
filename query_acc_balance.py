#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: tcp.py 并发数 每个线程请求次数 \nexample: tcp.py 500 10')
        exit(0)

    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])