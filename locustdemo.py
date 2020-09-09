#!/usr/bin/python
# -*- coding: utf-8 -*-
from locust import task, TaskSet

from tcpsocketlocust import TcpSocketLocust
from tranrequest import TranRequest
TERMINAL_NO = '00035'
TOKEN = '39c44a7891224ae08823ce29b219ad8a'


def create_sync_params():
    """
    构造同步参数请求
    :return:
    """
    request = TranRequest(TERMINAL_NO, TOKEN)
    request.begin_new_tran('sync_params')
    return request.pack()


class TcpTestUser(TcpSocketLocust):
    def __init__(self):
        host = "112.74.57.217"
        port = 9992
        ADDR = (host, port)
        self.client.connect(ADDR)

    min_wait = 5000
    max_wait = 9000

    class task_set(TaskSet):

        @task
        def send_data(self):
            self.client.send(create_sync_params())
            data = self.client.recv(2048).decode()
            print(data)


if __name__ == "__main__":
    user = TcpTestUser()
    user.run()