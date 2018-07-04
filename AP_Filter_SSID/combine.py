# -*- coding: utf-8 -*-

import scipy.io as sio


x_temp1 = sio.loadmat('x_set_180613_0.mat')['x_set_180613_0'].tolist()
x_temp2 = sio.loadmat('x_set_180613_1.mat')['x_set_180613_1'].tolist()
x_temp = x_temp1 + x_temp2
sio.savemat('x_set.mat', {'x_set': x_temp})

y_temp1 = sio.loadmat('y_set_180613_0.mat')['y_set_180613_0'].tolist()
y_temp2 = sio.loadmat('y_set_180613_1.mat')['y_set_180613_1'].tolist()
y_temp = y_temp1 + y_temp2
sio.savemat('y_set.mat', {'y_set': y_temp})

print('Save set in order')

print('########## 2 ##########')
