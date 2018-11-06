# -*- coding: utf-8 -*-
import scipy.io as sio
import numpy as np

"""
计算均值与方差
"""

x_sample = sio.loadmat('x_sort_5Loc.mat')['x_sort_5Loc'].tolist()
y_sample = sio.loadmat('y_sort_5Loc.mat')['y_sort_5Loc'].tolist()


def myMean(x, y):
    """
    计算每个点的均值及方差
    :param x: 每个点rssi
    :param y: 坐标
    """
    # 把每个坐标对应有多少数据存储下来
    loc_max = max(y)[0]
    count_loc = [0] * loc_max  # 列表，每处值表示每个坐标含有多少个数据集

    for iSample in y:
        count_loc[iSample[0] - 1] += 1
    x_ave = np.array([[0.0] * len(x[0])] * loc_max)
    x_var = np.array([[0.0] * len(x[0])] * loc_max)
    y_mean = [0] * len(count_loc)
    x_array = np.array(x)
    lastnum = 0
    nextnum = 0
    for i in range(loc_max):
        y_mean[i] = y[nextnum]
        nextnum += count_loc[i]
        for j in range(len(x[0])):
            # print(np.average(x_array[lastnum:nextnum-1, j]))
            x_ave[i][j] = np.average(x_array[lastnum:nextnum-1, j])
            x_var[i][j] = np.var(x_array[lastnum:nextnum-1, j])
        lastnum += count_loc[i]
    x_temp = x_ave.tolist()

    total = []
    foot = 0
    for data in x_temp:
        data.append(y_mean[foot][0])
        total.append(data)
        foot += 1
    sio.savemat('x_ave.mat', {'x_ave': x_ave})
    sio.savemat('x_var.mat', {'x_var': x_var})
    sio.savemat('y_mean.mat', {'y_mean': y_mean})
    sio.savemat('10m.mat', {'total': total})
    print(count_loc)
    # print(x_ave)
    # print(x_var)
    # print(y_mean)


myMean(x_sample, y_sample)
