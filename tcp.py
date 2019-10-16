#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import socket
import threading
import time

import sys

from tranrequest import TranRequest

DATEFMT = "%H:%M:%S"
FORMAT = "[%(asctime)s]\t [%(threadName)s,%(thread)d] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)

HOST = '112.74.57.217'
# HOST = '127.0.0.1'
PORT = 9992
TOTAL = 0  # 总数
SUCC = 0  # 响应成功数
FAIL = 0  # 响应失败数
EXCEPT = 0  # 响应异常数
MAX_TIME = 0  # 最大响应时间
MIN_TIME = 100  # 最小响应事件，初始值为100秒

SECTION8_ = 0
SECTION7_8 = 0
SECTION6_7 = 0
SECTION5_6 = 0
SECTION4_5 = 0
SECTION3_4 = 0
SECTION2_3 = 0
SECTION1_2 = 0 # 统计1-2秒内响应的
SECTION0_1 = 0 # 统计小于1秒响应的
TERMINAL_NO = '00035'
TOKEN = '39c44a7891224ae08823ce29b219ad8a'
"""
创建一个 threading.Thread 的派生类
"""


class TCPThread(threading.Thread):
    def __init__(self, thread_name, per_times):
        threading.Thread.__init__(self)
        self.test_count = 0
        self.name = thread_name
        self.per_times = per_times

    def run(self):
        """
        运行
        :return:
        """
        self.test_performance()

    def test_performance(self):
        """
        测试逻辑
        :return:
        """
        global TOTAL
        global SUCC
        global FAIL
        global EXCEPT

        for _ in range(self.per_times):
            tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                st = time.time()
                tcp_client.connect((HOST, PORT))
                tcp_client.send(create_query_acc_balance())
                reply = tcp_client.recv(1024)

                if reply:
                    SUCC += 1
                    # logging.info('tcp reply {}'.format(reply))
                else:
                    FAIL += 1
                    # logging.info('tcp reply error')

                time_span = time.time() - st
                self.max_time(time_span)
                self.min_time(time_span)

                self.count_section(time_span)
            except socket.error as e:
                logging.info('{} >>> {}'.format('socket error', e))
                EXCEPT += 1

            TOTAL += 1
            tcp_client.close()

    def max_time(self, ts):
        global MAX_TIME
        if ts > MAX_TIME:
            MAX_TIME = ts

    def min_time(self, ts):
        global MIN_TIME
        if ts < MIN_TIME:
            MIN_TIME = ts

    def count_section(self, ts):
        global SECTION8_
        global SECTION7_8
        global SECTION6_7
        global SECTION5_6
        global SECTION4_5
        global SECTION3_4
        global SECTION2_3
        global SECTION1_2
        global SECTION0_1

        if ts >= 8:
            SECTION8_ += 1
        elif 7 <= ts < 8:
            SECTION7_8 += 1
        elif 6 <= ts < 7:
            SECTION6_7 += 1
        elif 5 <= ts < 6:
            SECTION5_6 += 1
        elif 4 <= ts < 5:
            SECTION4_5 += 1
        elif 3 <= ts < 4:
            SECTION3_4 += 1
        elif 2 <= ts < 3:
            SECTION2_3 += 1
        elif 1 <= ts < 2:
            SECTION1_2 += 1
        else:
            SECTION0_1 += 1


def create_query_acc_balance():
    """
    构造获取账户余额请求
    :return:
    """
    request = TranRequest(TERMINAL_NO, TOKEN)
    request.begin_new_tran('query_acc_balance')
    request.put('sno', '1800999')
    return request.pack()

def create_sync_params():
    """
    构造同步参数请求
    :return:
    """
    request = TranRequest(TERMINAL_NO, TOKEN)
    request.begin_new_tran('sync_params')
    return request.pack()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.info('usage: tcp.py 并发数 每个线程请求次数')
        logging.info('example: tcp.py 500 10')
        exit(0)
    logging.info('并发数:{} 每个线程请求次数:{}'.format(sys.argv[1], sys.argv[2]))
    logging.info('{}'.format('=============== Start ==============='))
    # 开始时间
    start_time = time.time()
    # 并发线程数
    thread_count = int(sys.argv[1])
    per_times = int(sys.argv[2])
    i = 0
    while i < thread_count:
        t = TCPThread('thread' + str(i), per_times)
        t.start()
        i += 1
    t = 0

    while TOTAL < thread_count * per_times and t < 60:
        # logging.info('total:{}; succ:{}; fail:{}; except:{}'.format(TOTAL, SUCC, FAIL, EXCEPT))
        # logging.info('HOST:{}; PORT:{}'.format(HOST, PORT))
        t += 1
        time.sleep(1)

    logging.info('{}'.format('=============== End ==============='))
    logging.info('total: {}; succ: {}; fail: {}; except: {}'.format(TOTAL, SUCC, FAIL, EXCEPT))
    logging.info('response maxtime: {0:.2f}(s)'.format(MAX_TIME))
    logging.info('response mintime: {0:.2f}(s)'.format(MIN_TIME))
    logging.info('SECTION_0-1: {} Percent: {:.3f}%'.format(SECTION0_1, float(SECTION0_1 / TOTAL)))
    logging.info('SECTION_1-2: {} Percent: {:.3f}%'.format(SECTION1_2, float(SECTION1_2 / TOTAL)))
    logging.info('SECTION_2-3: {} Percent: {:.3f}%'.format(SECTION2_3, float(SECTION2_3 / TOTAL)))
    logging.info('SECTION_3-4: {} Percent: {:.3f}%'.format(SECTION3_4, float(SECTION3_4 / TOTAL)))
    logging.info('SECTION_4-5: {} Percent: {:.3f}%'.format(SECTION4_5, float(SECTION4_5 / TOTAL)))
    logging.info('SECTION_5-6: {} Percent: {:.3f}%'.format(SECTION5_6, float(SECTION5_6 / TOTAL)))
    logging.info('SECTION_6-7: {} Percent: {:.3f}%'.format(SECTION6_7, float(SECTION6_7 / TOTAL)))
    logging.info('SECTION_7-8: {} Percent: {:.3f}%'.format(SECTION7_8, float(SECTION7_8 / TOTAL)))
    logging.info('SECTION_8-: {} Percent: {:.3f}%'.format(SECTION8_, float(SECTION8_ / TOTAL)))
