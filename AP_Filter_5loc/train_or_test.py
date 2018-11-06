# -*- coding: utf-8 -*-
# 用于将获取的数据按8:2比例分为train set和test set
import scipy.io as sio
import os


def split_data(filename):
    """
    把传入的数据库按8:2比例分为训练集和测试集，并存为mat文件
    param1：特征值的数据库
    param2：标签的数据库
    """
    features = sio.loadmat('x' + filename + '.mat')
    features = features['x' + filename].tolist()
    labels = sio.loadmat('y' + filename + '.mat')
    labels = labels['y' + filename].tolist()

    # 把每个坐标对应有多少数据存储下来
    loc_max = max(labels)[0]
    count_loc = [0] * loc_max  # 列表，每处值表示每个坐标含有多少个数据集
    for iSample in labels:
        # if iSample[0] >= 42:
        #     iSample[0] = iSample[0] - 2
        count_loc[iSample[0] - 1] += 1

    foot = 0  # 用于记录每次切片起始位置
    x_test = []
    y_test = []
    for loc_num in count_loc:
        temp = len(features[foot:foot + loc_num - 1:5])
        # 记录切片长度
        x_test = x_test + features[foot:foot + loc_num - 1:5]  # 每5步取一个数据保存入test集
        del features[foot:foot + loc_num - 1:5]  # 删除测试集剩下的即为训练集

        y_test = y_test + labels[foot:foot + loc_num - 1:5]
        del labels[foot:foot + loc_num - 1:5]

        foot = foot + loc_num - temp  # 起始位置 = 上一个切片的起始位置 + 对应位置总数据个数 - 删去的测试的个数
    str_test = '_test_' + filename.lstrip('_sort')
    str_train = '_train_' + filename.lstrip('_sort')
    sio.savemat('x' + str_test + '.mat', {'x' + str_test: x_test})
    sio.savemat('x' + str_train + '.mat', {'x' + str_train: features})
    sio.savemat('y' + str_test + '.mat', {'y' + str_test: y_test})
    sio.savemat('y' + str_train + '.mat', {'y' + str_train: labels})
    print("Split train or test")


if os.path.exists('x_sort_5Loc.mat'):
    file = '_sort_5Loc'
    split_data(file)


if os.path.exists('x_qu_5Loc.mat'):
    file = '_qu_5Loc'
    split_data(file)


print('########## 3 ##########')

