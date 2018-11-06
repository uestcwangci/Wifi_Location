#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : Gaussi.py 
@Time: 2018/10/23 20:40
@Desc:
"""

from scipy.ndimage import filters
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

# 读入特征值训练
sample = sio.loadmat('10m.mat')
sample = sample['total']
ap1 = sample[65000:, 2]
ap2 = sample[65000:, 3]
ap3 = sample[65000:, 9]
ap4 = sample[65000:, 10]
ap5 = sample[65000:, 39]
ap6 = sample[65000:, 41]
ap7 = sample[65000:, 42]
ap8 = sample[65000:, 50]
ap9 = sample[65000:, 53]
ap10 = sample[65000:, 63]
x = np.arange(1, 1001)
y = ap1
plt.figure(1)
plt.plot(x, y)
plt.show()
a=1