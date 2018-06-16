# -*- coding: utf-8 -*-
# 将输入的数据打乱顺序
import scipy.io as sio
import random
# 读取数据
x_sample = sio.loadmat('x_set.mat')
x_sample = x_sample['x_set'].tolist()

y_sample = sio.loadmat('y_set.mat')
y_sample = y_sample['y_set'].tolist()


# 将数据库打乱顺序
for numX in range(len(x_sample)):
    x_sample[numX] += y_sample[numX]
random.shuffle(x_sample)

for numX in range(len(x_sample)):
    y_sample[numX] = x_sample[numX][-1:]
    x_sample[numX] = x_sample[numX][0:-1]
sio.savemat('x_set_random.mat', {'x_set_random': x_sample})
sio.savemat('y_set_random.mat', {'y_set_random': y_sample})
print('Save set in random')
print('########## 3 ##########')
