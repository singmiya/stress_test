#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket

from tcpclient import TcpClient
from locust import User,Locust


class TcpSocketLocust(User):
    """
    This is the abstract Locust class which should be subclassed. It provides an TCP socket client
    that can be used to make TCP socket requests that will be tracked in Locust's statistics.
    author: Max.bai@2017
    """
    def __init__(self, *args, **kwargs):
        super(TcpSocketLocust, self).__init__(*args, **kwargs)
        self.client = TcpClient(socket.AF_INET, socket.SOCK_STREAM)
