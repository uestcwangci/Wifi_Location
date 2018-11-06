# -*- coding: utf-8 -*-
# 读取所有存在的AP，把每个坐标RSSI填入AP表中
import csv
import sqlite3 as sq
import re
import numpy as np
import scipy.io as sio
import os.path


allAP = {}
csv_reader = csv.reader(open('allAP.csv', 'r'))
for row in csv_reader:
    allAP[row[1]] = row[2]

# 去掉表头
allAP.pop('MAC')
Max_AP = len(allAP)
init_x = {}
for key in allAP.keys():
    init_x[key] = 0

# 获取文件夹路径
Data_path = os.path.abspath('..\\DataBase')
DatabaseName = 'myTest5'

# Sqlite3连接
conn = sq.connect(Data_path + '\\' + DatabaseName + '.db')  # 连接数据库
cursor = conn.cursor()
# print('Open database successfully')
# x存储MAC以及RSSI    y存储label值
x_train = []
y_train = []
# 将AP1，AP2……拼接在一个字符串中
choose_AP = []
for num_AP in range(25):
    choose_AP.append('AP' + str(num_AP + 1))
AP_str = ','.join(choose_AP)

selected = cursor.execute('SELECT Id,' + AP_str + ',Date FROM main.stu_table')  # 读取数据库数据
# 正则初始化
MAC_regex = re.compile(r"MAC = '(\w+:\w+:\w+:\w+:\w+:\w+)'")  # 用于匹配MAC地址
RSSI_regex = re.compile(r"level = (-\d+)")  # 用于匹配RSSI
Loc_regex = re.compile(r'(\d+),(\d+)')  # 用于匹配id，对应坐标值
Date_regex = re.compile(r'(\d+-\d+-\d+)')  # 用于匹配日期
Name_regex = re.compile(r"Name = '(\w+)'")
#######################################################################
# 过滤数据
x_last = init_x.copy()
y_last = []
# 每次循环放入一行采样数据
for row in selected:
    # 循环开始时初始化列表
    x_temp = init_x.copy()
    x_withoutMac = list(x_temp.values())
    y_temp = []
    Location = Loc_regex.search(row[0])
    date = Date_regex.search(row[-1])
    # 能找到坐标，且过滤x为0的点,或首个RSSI为-100dBm的点
    if Location and Location.group(1) != '0' and RSSI_regex.search(row[1]).group(1) != '-100':
        y_temp.append(int(Location.group(1)))
        # 每次循环放入1个AP
        for i in range(25):
            MAC = MAC_regex.search(row[i + 1])
            RSSI = RSSI_regex.search(row[i + 1])
            # 当遍历到RSSI = -100dBm的AP时终止
            if RSSI and RSSI.group(1) == '-100':
                break
            if MAC and RSSI:
                mac = MAC.group(1)
                if mac in allAP.keys():
                    x_temp[mac] = int(RSSI.group(1))
            x_withoutMac = list(x_temp.values())

        # 当下一个坐标与上一个不同，MAC及RSSI与上一个相同时，过滤此次信息
        if y_temp != y_last and x_temp == x_last:
            pass
        else:
            x_last = x_temp.copy()
            y_last = y_temp.copy()
            # 根据标识符分类
            if Location.group(2) == '5':
                y_train.append(y_temp)
                x_train.append(x_withoutMac)

            # elif Location.group(2) == '1':
            #     y_test.append(y_temp)
            #     x_test.append(x_temp)
            #     x_temp = []
            #     y_temp = []
            else:
                pass

# 保存数据
######################################################
x_train_array = np.array(x_train)
sio.savemat('x_form_' + DatabaseName.lstrip('myTest_') + '.mat',
            {'x_form_' + DatabaseName.lstrip('myTest_'): x_train_array})
y_train_array = np.array(y_train)
sio.savemat('y_form_' + DatabaseName.lstrip('myTest_') + '.mat',
            {'y_form_' + DatabaseName.lstrip('myTest_'): y_train_array})

# print('Save set successfully')
# for rAP in reversed(range(MIN_AP, MAX_AP + 1)):
#     x_train_array = np.array(x_train)
#     sio.savemat(DatabaseName + '_Feature_AP' + str(rAP) + '.mat',
#                 {'x_set_' + DatabaseName.lstrip('myTest_') + '_AP' + str(rAP): x_train_array})
#
#     for iData in x_train:
#         del iData[-7:]
#     print('Save set successfully | File:%2i | AP:%2i |' % (num_file + 1, rAP))
##############################################################

cursor.close()
conn.close()
# print('Close file')
print('Arrange AP')
print('########## 2 ##########')
