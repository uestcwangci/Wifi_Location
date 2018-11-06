# -*- coding: utf-8 -*-
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
sio.savemat('test.mat',{'test':total})

