# -*- coding: utf-8 -*-
import sqlite3 as sq
import re
import numpy as np
import scipy.io as sio
import GlobalVarible.setter
import GlobalVarible.getter as glovar
import os.path

# 获取文件夹路径
Data_path = os.path.abspath('..\\DataBase')

MIN_AP = glovar.MIN_AP  # 采用最小AP数
MAX_AP = glovar.MAX_AP  # 采用最大AP数
FILE_NUM = 1  # 需要载入的数据库数量
for num_file in range(FILE_NUM):
    # 根据需要录入的文件总数读取数据库数据
    if num_file == 0:
        DatabaseName = 'myTest5'
    elif num_file == 1:
        DatabaseName = 'myTest_180613_1'
    else:
        continue
    # Sqlite3连接
    conn = sq.connect(Data_path + '\\' + DatabaseName + '.db')  # 连接数据库
    cursor = conn.cursor()
    # print('Open database successfully')
    # x存储MAC以及RSSI    y存储label值
    x_train = []
    y_train = []
    # 将AP1，AP2……拼接在一个字符串中
    choose_AP = []
    for num_AP in range(MAX_AP):
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
    x_last = []
    y_last = []
    for row in selected:
        # 循环开始时初始化列表
        x_temp = []
        y_temp = []
        Location = Loc_regex.search(row[0])
        date = Date_regex.search(row[-1])
        # 能找到坐标，且过滤x为0的点,或首个RSSI为-100dBm的点
        if Location and Location.group(1) != '0' and RSSI_regex.search(row[1]).group(1) != '-100':
            y_temp.append(int(Location.group(1)))
            # 每次循环放入1个AP
            for i in range(MAX_AP):
                MAC = MAC_regex.search(row[i + 1])
                RSSI = RSSI_regex.search(row[i + 1])
                if MAC and RSSI:
                    x_temp.append(int(RSSI.group(1)))
                    for j in range(len(MAC.groups())):
                        x_temp.append(int(MAC.group(j + 1)))

            # 当下一个坐标与上一个不同，MAC及RSSI与上一个相同时，过滤此次信息
            if y_temp != y_last and x_temp == x_last:
                pass
            else:
                x_last = x_temp.copy()
                y_last = y_temp.copy()
                # 根据标识符分类
                if Location.group(2) == '5':
                    y_train.append(y_temp)
                    x_train.append(x_temp)

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
    sio.savemat('x_set_' + DatabaseName.lstrip('myTest_') + '.mat',
                {'x_set_' + DatabaseName.lstrip('myTest_'): x_train_array})
    y_train_array = np.array(y_train)
    sio.savemat('y_set_' + DatabaseName.lstrip('myTest_') + '.mat',
                {'y_set_' + DatabaseName.lstrip('myTest_'): y_train_array})

    print('Save set successfully | File:%2i |' % (num_file + 1))
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
print('Database out')
print('########## 1 ##########')

