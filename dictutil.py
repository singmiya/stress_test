#!/usr/bin/python
# -*- coding: utf-8 -*-
import operator


def to_query_string(dict_, is_sort=True, exclude=None):
    """
    把字典转成查询字符串
    :param dict_:
    :param is_sort:
    :param exclude:
    :return:
    """
    if is_empty(dict_):
        return ''
    dict_ = sorted(dict_.items(), key=operator.itemgetter(0)) if is_sort else dict_
    k_v = []
    for key, value in dict_:
        is_exclude = False if None is exclude or key not in exclude else True
        if not is_exclude:
            k_v.append(key + '=' + str(value))
    return '&'.join(k_v)


def is_empty(dict_):
    """
    字典是否为空
    :param dict_:
    :return:
    """
    return None is dict_ or len(dict_) == 0
