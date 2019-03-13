#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : Sort.py
@Time: 2018/8/1 21:43
@Desc:  把数据库按照坐标位置顺序排序
"""
import scipy.io as sio
import numpy as np


# 获取列表的最后一个元素
def takeLastData(elem):
    return elem[-1]


total = sio.loadmat('total_2.mat')['total'].tolist()
afterSort = []

total.sort(key=takeLastData)
total_array = np.array(total)
sio.savemat('total_2.mat', {'total': total_array})


print('Sort done')
print('########## 2 ##########')
