#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import json
import uuid
from datetime import datetime
import time

import dictutil
import tranitemname

"""
 tranaction protocol
 header(3) + length(2) + priority(1) + version(2) + charset(8) + tranData(length-11)
 |<----------------------  fixed  --------------------------->|
                                                              |<----- encode by charset ---->|

                                                               * tranaction protocol

 smy 更新协议
 header(3) + length(4) + priority(1) + version(2) + charset(8) + tranData(length-11)
 |<----------------------  fixed  --------------------------->|
                                                              |<----- encode by charset ---->|
"""


class TranMessage(object):
    def __init__(self):
        """"""


class TranRequest(object):
    tran_data = {}

    def __init__(self, terminal_no=None, access_token=None):
        """"""
        self.header = tranitemname.HEADER
        self.version = tranitemname.VERSION
        self.priority = tranitemname.NORMAL
        self.terminal_no = terminal_no
        self.access_token = access_token
        self.charset = tranitemname.UTF8

    def has_item(self, key):
        """
        key是否存在
        :param key:
        :return:
        """
        return None is not key and self.tran_data.__contains__(key)

    def put(self, key, value):
        """
        添加数据
        :param key:
        :param value:
        :return:
        """
        self.tran_data[key] = value

    def get(self, key):
        """
        获取值
        :param key:
        :return:
        """
        if self.has_item(key):
            return self.tran_data[key]
        return 'null'

    def pack_tran_data(self):
        """
        :return:
        """
        sign = self.compute_sign(self.access_token)
        clone_data = dict.copy(self.tran_data)
        clone_data[tranitemname.SIGN] = sign
        return bytes(json.dumps(obj=clone_data).replace(' ', ''), self.charset)

    def unpack(self, buffer):
        """
        :return:
        """
        tran_d = TranRequest()
        tran_d.header = buffer[:3].decode('utf-8')
        length = int.from_bytes(buffer[3:7], byteorder='big', signed=True)
        tran_d.priority = buffer[7:8]
        tran_d.version = buffer[8:10]
        tran_d.charset = bytearray([b for b in buffer[10:18] if b != 0]).decode('utf-8')
        tran_d.tran_data = json.loads(buffer[18:len(buffer)])

        return tran_d

    def compute_sign(self, access_token):
        """
        计算签名
        :param access_token:
        :return:
        """
        data = dict.copy(self.tran_data)
        plain = dictutil.to_query_string(data, exclude=['sign']) + access_token
        return hashlib.sha1(plain.encode(self.charset)).hexdigest()

    def pack(self):
        """
        :return:
        """
        data_bytes = self.pack_tran_data()
        length = len(data_bytes) + tranitemname.DATA_OFFSET
        bb = bytearray()
        bb.extend(self.header.encode())
        bb.extend(int(length).to_bytes(4, byteorder='big', signed=True))
        bb.extend(int(self.priority).to_bytes(1, byteorder='big', signed=True))
        bb.extend(tranitemname.VERSION)
        charset_b = bytearray(bytes(self.charset, self.charset))
        charset_b_ = bytearray(8 - len(charset_b))
        charset_b.extend(charset_b_)
        bb.extend(charset_b)
        bb.extend(data_bytes)
        return bb

    def begin_new_tran(self, tran_code):
        """"""
        self.tran_data.clear()
        self.tran_data[tranitemname.TERMINAL_NO] = self.terminal_no
        self.tran_data[tranitemname.TRAN_CODE] = tran_code
        self.tran_data[tranitemname.NONCE] = uuid.uuid1().urn.replace('urn:uuid:', '')
        self.tran_data[tranitemname.TRAN_DATE] = datetime.now().strftime('%Y%m%d%H%M%S')
        self.tran_data[tranitemname.TRAN_JNL] = tranitemname.POS_JNL_PREFIX + '-' + self.terminal_no + '-' + datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]


if __name__ == '__main__':
    # dict3 = {'name': 'z', 'Age': 7, 'class': 'First', 'sex': '1', 'b': 'qwe'}
    # print(dictutil.to_query_string(dict3))
    #
    # dict1 = dict.copy(dict3)
    # dict1['name'] = '123'
    # print(dict1)
    # print(dict3)
    # TERMINAL_NO = '00035'
    # TOKEN = '39c44a7891224ae08823ce29b219ad8a'
    #
    # obj = TranRequest(TERMINAL_NO, TOKEN)
    # obj.begin_new_tran('query_acc_balance')
    # obj.put('sno', '1800999')
    # print(obj.compute_sign(TOKEN))
    # print(obj.pack_tran_data())
    # print(len(obj.pack()))
    # obj1 = TranRequest()
    #
    # print(obj1.unpack(obj.pack()))
    st = time.time()
    print(st)
    time.sleep(1)
    print(time.time() - st)