#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        pass
        # self.syncParam()

    def syncParam(self):
        body = {'terminalNo': 'POS00181'}
        self.client.post('/syncParams', data=body)

    @task(1)
    def index(self):
        body = {'terminalNo': 'POS00181'}
        self.client.post('/syncParams', data=body)


class WebUser(HttpUser):
    task_set = UserBehavior
    host = 'http://openapi.greatge.net'
    min_wait = 5000
    max_wait = 9000



if __name__ == '__main__':
    os.system('locust -f locustio.py --host=http://openapi.greatge.net')