# -*- coding: utf-8 -*-
# 将输入的数据打乱顺序
import scipy.io as sio
import random

TRAIN = 0
TEST = 1
# 读取数据
x_train = sio.loadmat('x_train_rssi.mat')['x_train_rssi'].tolist()
y_train = sio.loadmat('y_train_rssi.mat')['y_train_rssi'].tolist()


x_test = sio.loadmat('x_test_rssi.mat')['x_test_rssi'].tolist()
y_test = sio.loadmat('y_test_rssi.mat')['y_test_rssi'].tolist()


def disorder(x_sample, y_sample, flag):
    # 将数据库打乱顺序
    for numX in range(len(x_sample)):
        x_sample[numX] += y_sample[numX]
    random.shuffle(x_sample)

    for numX in range(len(x_sample)):
        y_sample[numX] = x_sample[numX][-1:]
        x_sample[numX] = x_sample[numX][0:-1]
    if flag == TRAIN:
        sio.savemat('x_train_rRssi.mat', {'x_train_rRssi': x_sample})
        sio.savemat('y_train_rRssi.mat', {'y_train_rRssi': y_sample})
    elif flag == TEST:
        sio.savemat('x_test_rRssi.mat', {'x_test_rRssi': x_sample})
        sio.savemat('y_test_rRssi.mat', {'y_test_rRssi': y_sample})
    else:
        print("Unknown")


disorder(x_train, y_train, TRAIN)
disorder(x_test, y_test, TEST)
print('Disorder Set')
print('########## 4 ##########')
