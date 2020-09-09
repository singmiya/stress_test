#!/usr/bin/python
# -*- coding: utf-8 -*-

# client

import socket

import time

from locust import events


class TcpClient(socket.socket):
    def __init__(self, af_inet, socket_type):
        super(TcpClient, self).__init__(af_inet, socket_type)

    def connect(self, addr):
        start_time = time.time()
        try:
            super(TcpClient, self).connect(addr)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="connect", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="connect", response_time=total_time,
                                        response_length=0)

    def send(self, msg):
        start_time = time.time()
        try:
            super(TcpClient, self).send(msg)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="send", response_time=total_time,
                                        response_length=0)

    def recv(self, bufsize):
        recv_data = ''
        start_time = time.time()
        try:
            recv_data = super(TcpClient, self).recv(bufsize)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="recv", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="recv", response_time=total_time,
                                        response_length=0)
        return recv_data
