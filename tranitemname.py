#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-

# 协议头
import operator

HEADER = 'rft'
# 版本
VERSION = [0x01, 0x00]
# 优先级
NORMAL = 0x00
DATA_OFFSET = 11
SIGN = 'sign'
UTF8 = 'utf-8'
TERMINAL_NO = 'terminal_no'
TRAN_CODE = 'tran_code'
TRAN_JNL = 'tran_jnl'
TRAN_DATE = 'tran_date'
NONCE = 'nonce'
POS_JNL_PREFIX = "POS"

if __name__ == '__main__':
    dict3 = {'name': 'z', 'Age': 7, 'class': 'First', 'sex': '1', 'b': 'qwe'}
    ret = sorted(dict3.items(), key=operator.itemgetter(0))
    print(ret)