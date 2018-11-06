# -*- coding: utf-8 -*-
import scipy.io as sio


# 读取数据
sample_x = sio.loadmat('x_set_5Loc.mat')
sample_x = sample_x['x_set_5Loc'].tolist()
sample_y = sio.loadmat('y_set_5Loc.mat')
sample_y = sample_y['y_set_5Loc'].tolist()


# 以10为一个等级，给RSSI量化
for num_list in sample_x:
    for num in num_list:
        i = num_list.index(num)
        if -100 <= num <= -90:
            num_list[i] = 9
        elif -90 < num <= -80:
            num_list[i] = 8
        elif -80 < num <= -70:
            num_list[i] = 7
        elif -70 < num <= -60:
            num_list[i] = 6
        elif -60 < num <= -50:
            num_list[i] = 5
        elif -50 < num <= -40:
            num_list[i] = 4
        elif -40 < num <= -30:
            num_list[i] = 3
        elif -30 < num <= -20:
            num_list[i] = 2
        elif -20 < num <= -10:
            num_list[i] = 1
        elif -10 < num <= 0:
            num_list[i] = 0
        else:
            pass

sio.savemat('x_qu_5Loc.mat', {'x_qu_5Loc': sample_x})
sio.savemat('y_qu_5Loc.mat', {'y_qu_5Loc': sample_y})
print('Quantification')
print('########## 2 ##########')

