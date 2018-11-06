#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : knn_5loc.py 
@Time: 2018/8/2 21:21
@Desc:
"""
import os
import scipy.io as sio
import numpy as np
import math
# 获取文件夹路径
mat_path = os.path.abspath('..\\mat_data\\For5Loc')
cur_path = os.getcwd()


# 计算欧氏距离
def Euclidean(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    distance = []
    temp1 = []
    temp2 = []
    for ii in npvec2:
        for jj in npvec1:
            temp1.append(math.sqrt(((np.array(jj[:-1])-np.array(ii))**2).sum()))
        mindis = min(temp1)
        temp2.append(mindis)
        temp2.append(temp1.index(mindis))
        distance.append(temp2)
        temp1 = []
        temp2 = []
    return distance


# 读入训练数据
################################################################################################
filename = mat_path + '\\10m.mat'
total = sio.loadmat(filename)['total'].tolist()
position = []
for i in total:
    i[-1] = i[-1] - 1
    position.append(i)


# 读入测试数据
################################################################################################
filename = mat_path + '\\x_sort_5Loc.mat'
x_sort = sio.loadmat(filename)['x_sort_5Loc'].tolist()
filename = mat_path + '\\y_sort_5Loc.mat'
y_sort = sio.loadmat(filename)['y_sort_5Loc'].tolist()

results = Euclidean(position, x_sort)
i = 0
count = 0
acc = [0] * len(position)
allNum = [0] * len(position)
for result in results:
    if result[-1] == y_sort[i][0] - 1:
        count += 1
        acc[result[-1]] += 1
    allNum[result[-1]] += 1
    i += 1

print(count)
print(count/len(y_sort))
print(allNum)
print(acc)


# 输出网络、输出偏置向量
###################################################################################################
filename = mat_path + '\\x_ave.mat'
x_ave = sio.loadmat(filename)['x_ave']
output = open('x_ave.txt', 'w')
for iW in x_ave:
    for iw in iW:
        output.write(str(iw))
        output.write(' ')
    output.write('\n')

output.close()
