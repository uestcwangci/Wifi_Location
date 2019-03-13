#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : globalvar.py 
@Time: 2018/11/13 19:28
@Desc:
"""

def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue