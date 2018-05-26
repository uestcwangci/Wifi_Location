# -*- coding: utf-8 -*-
import sqlite3 as sq
import re
import numpy as np
import scipy.io as sio

MAX_AP = 15  # 采用最大AP数

# Sqlite3初始化
DatabaseName = 'myTest.db'  # 设置当前链接数据库名称
conn = sq.connect(DatabaseName)
print('Connected')
cursor = conn.cursor()
print('Open database successfully')
# 将AP1，AP2……拼接在一个字符串中
choose_AP = []
for num_AP in range(MAX_AP):
    choose_AP.append('AP' + str(num_AP + 1))
AP_str = ','.join(choose_AP)
AP_str.rstrip(',')

selected = cursor.execute('SELECT Id,' + AP_str + ' FROM stu_table')  # 读取数据库数据

# 正则初始化
pattern1 = re.compile(r"MAC2='(\d+):(\d+):(\d+):(\d+):(\d+):(\d+)'")  # 用于匹配MAC地址
pattern2 = re.compile(r"level2=(-\d+)")  # 用于匹配RSSI
pattern3 = re.compile(r'(\d+),(\d+),(\d+),(\d+)')  # 用于匹配id，对应坐标值

# x存储MAC以及RSSI    y存储label值
x_train = []
y_train = []
x_test = []
y_test = []


# 过滤数据
for row in selected:
    x_temp = []
    y_temp = []
    Location = pattern3.search(row[0])
    # 能找到坐标，且过滤不为0的点
    if Location and Location.group(1) != '0':
        y_temp.append(int(Location.group(1)))
        # 每次循环放入1个AP
        for i in range(MAX_AP):
            MAC = pattern1.search(row[i + 1])
            RSSI = pattern2.search(row[i + 1])
            if MAC and RSSI:
                x_temp.append(int(RSSI.group(1)))
                for j in range(len(MAC.groups())):
                    x_temp.append(int(MAC.group(j + 1)))
        # 纵坐标中0表示训练集，1表示测试集
        if Location.group(2) == '0':
            y_train.append(y_temp)
            x_train.append(x_temp)
            x_temp = []  # 清空列表
            y_temp = []
        elif Location.group(2) == '1':
            y_test.append(y_temp)
            x_test.append(x_temp)
            x_temp = []
            y_temp = []
        else:
            pass

# print(x_train)
# print(len(x_train))
# print(y_train)
# print(len(y_train))

# 根据本次数据是Train还是Test存入不同mat文件中
######################################################

x_train_array = np.array(x_train)
sio.savemat('AP_train.mat', {'x_train': x_train_array})
print('Save Training data successfully')
y_train_array = np.array(y_train)
sio.savemat('label_train.mat', {'y_train': y_train_array})
print('Save Training label successfully')


x_test_array = np.array(x_test)
sio.savemat('AP_test.mat', {'x_test': x_test_array})
print('Save Testing data successfully')
y_test_array = np.array(y_test)
sio.savemat('label_test.mat', {'y_test': y_test_array})
print('Save Testing label successfully')

##############################################################
cursor.close()
conn.close()
