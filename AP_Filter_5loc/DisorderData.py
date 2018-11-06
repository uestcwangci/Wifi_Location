# -*- coding: utf-8 -*-
# 将输入的数据打乱顺序
import scipy.io as sio
import random

TRAIN = 0
TEST = 1


def disorder(flag):
    # 读取数据
    global x_sample, y_sample
    if flag == TRAIN:
        x_sample = sio.loadmat('x_train_5Loc.mat')['x_train_5Loc'].tolist()
        y_sample = sio.loadmat('y_train_5Loc.mat')['y_train_5Loc'].tolist()
    elif flag == TEST:
        x_sample = sio.loadmat('x_test_5Loc.mat')['x_test_5Loc'].tolist()
        y_sample = sio.loadmat('y_test_5Loc.mat')['y_test_5Loc'].tolist()
    # 将数据库打乱顺序
    for numX in range(len(x_sample)):
        x_sample[numX] += y_sample[numX]
    random.shuffle(x_sample)

    for numX in range(len(x_sample)):
        y_sample[numX] = x_sample[numX][-1:]
        x_sample[numX] = x_sample[numX][0:-1]
    if flag == TRAIN:
        sio.savemat('x_train_r5Loc.mat', {'x_train_r5Loc': x_sample})
        sio.savemat('y_train_r5Loc.mat', {'y_train_r5Loc': y_sample})
    elif flag == TEST:
        sio.savemat('x_test_r5Loc.mat', {'x_test_r5Loc': x_sample})
        sio.savemat('y_test_r5Loc.mat', {'y_test_r5Loc': y_sample})
    else:
        print("Unknown")


disorder(TRAIN)
disorder(TEST)
print('Disorder Set')
print('########## 4 ##########')
