# -*- coding: utf-8 -*-
import sqlite3 as sq
import re
import numpy as np
import scipy.io as sio

MAX_AP = 15  # 采用最大AP数

# Sqlite3初始化
conn = sq.connect('myTest.db')
print('Connected')
cursor = conn.cursor()
print('Open database successfully')
selected = cursor.execute('SELECT Id,AP1,AP2,AP3,AP4,AP5,AP6,'
                          'ap7,AP8,AP9,AP10,AP11,AP12,AP13,AP14,AP15 FROM stu_table')

# 正则初始化
pattern1 = re.compile(r"MAC2='(\d+):(\d+):(\d+):(\d+):(\d+):(\d+)'")  # 用于匹配MAC地址
pattern2 = re.compile(r"level2=(-\d+)")  # 用于匹配RSSI
pattern3 = re.compile(r'(\d+),(\d+),(\d+),(\d+)')  # 用于匹配id，对应坐标值

x_label = []  # 存储MAC以及RSSI
y_label = []  # 存储label值

# 过滤数据
for row in selected:
    x_temp = []
    y_temp = []
    Location = pattern3.search(row[0])
    # 能找到坐标，且过滤坐标为（0,0）的点
    if Location and Location.group(1) != '0':
        y_temp.append(int(Location.group(1)))
        y_label.append(y_temp)
        # 每次循环放入1个AP
        for i in range(MAX_AP):
            MAC = pattern1.search(row[i + 1])
            RSSI = pattern2.search(row[i + 1])
            if MAC and RSSI:
                x_temp.append(int(RSSI.group(1)))
                for j in range(len(MAC.groups())):
                    x_temp.append(int(MAC.group(j + 1)))
            # --------Debug Here----------
            # if MAC:
            #     print('MAC address: ', end='')
            #     for k in range(len(MAC.groups())):
            #         print(MAC.group(k + 1), end='|')
            # if RSSI:
            #     print(RSSI.group(1))
            # if Location:
            #     print("Location: ", end='')
            #     print('(', Location.group(1), ',', Location.group(2), ')')
        x_label.append(x_temp)
        x_temp = []  # 清空列表

# print(x_label)
# print(len(x_label))
# print(y_label)
print(len(y_label))

filename = 'AP_train.mat'
x_array = np.array(x_label)
sio.savemat(filename, {'x_train': x_array})
print('Save data to .mat File successfully')
filename = 'label_train.mat'
y_array = np.array(y_label)
sio.savemat(filename, {'y_train': y_array})
print('Save label to .mat File successfully')

cursor.close()
conn.close()
