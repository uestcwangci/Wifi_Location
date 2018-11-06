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


x_sample = sio.loadmat('x_set_5Loc.mat')['x_set_5Loc'].tolist()
y_sample = sio.loadmat('y_set_5Loc.mat')['y_set_5Loc'].tolist()
total = []
afterSort = []
for data in x_sample:
    data.append(y_sample[x_sample.index(data)][0])
    total.append(data)
total.sort(key=takeLastData)
total_array = np.array(total)
sio.savemat('10m.mat', {'total': total_array})
sio.savemat('x_sort_5Loc.mat', {'x_sort_5Loc': total_array[:, 0:-1]})
sio.savemat('y_sort_5Loc.mat', {'y_sort_5Loc': [[i] for i in total_array[:, -1].tolist()]})
