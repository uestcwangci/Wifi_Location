# -*- coding: utf-8 -*-
# 用于将获取的数据按8:2比例分为train set和test set
import scipy.io as sio


# 读取数据
sample_x = sio.loadmat('x_set_5.mat')
sample_x = sample_x['x_set_5'].tolist()

sample_y = sio.loadmat('y_set_5.mat')
sample_y = sample_y['y_set_5'].tolist()

# 把每个坐标对应有多少数据存储下来
loc_max = max(sample_y)[0]
count_loc = [0] * loc_max  # 列表，每处值表示每个坐标含有多少个数据集
for iSample in sample_y:
    # if iSample[0] >= 42:
    #     iSample[0] = iSample[0] - 2
    count_loc[iSample[0] - 1] += 1


def split_data(count_data, features, labels):
    """
    把传入的数据库按8:2比例分为训练集和测试集，并存为mat文件
    param1：每个位置对应多少数据个数列表
    param2：特征值的数据库
    param2：标签的数据库
    """
    foot = 0  # 用于记录每次切片起始位置
    x_test = []
    y_test = []
    for loc_num in count_data:
        temp = len(features[foot:foot + loc_num - 1:5])
        # 记录切片长度
        x_test = x_test + features[foot:foot + loc_num - 1:5]   # 每5步取一个数据保存入test集
        del features[foot:foot + loc_num - 1:5]     # 删除测试集剩下的即为训练集

        y_test = y_test + labels[foot:foot + loc_num - 1:5]
        del labels[foot:foot + loc_num - 1:5]

        foot = foot + loc_num - temp    # 起始位置 = 上一个切片的起始位置 + 对应位置总数据个数 - 删去的测试的个数

    sio.savemat('x_test_rssi.mat', {'x_test_rssi': x_test})
    sio.savemat('x_train_rssi.mat', {'x_train_rssi': features})
    sio.savemat('y_test_rssi.mat', {'y_test_rssi': y_test})
    sio.savemat('y_train_rssi.mat', {'y_train_rssi': labels})
    print("Split successfully")


split_data(count_loc, sample_x, sample_y)

print('########## 3 ##########')

