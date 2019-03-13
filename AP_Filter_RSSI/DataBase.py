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
        DatabaseName = '5m'
    elif num_file == 1:
        DatabaseName = 'myTest_180613_1'
    else:
        continue
    # Sqlite3连接
    # conn = sq.connect(Data_path + '\\' + DatabaseName + '.db')  # 连接数据库
    conn = sq.connect('5m.db')
    cursor = conn.cursor()
    print('Open database successfully')
    # x存储MAC以及RSSI    y存储label值
    x_train = []
    y_train = []
    # 将AP1，AP2……拼接在一个字符串中
    choose_AP = []
    for num_AP in range(MAX_AP):
        choose_AP.append('AP' + str(num_AP + 1))
    AP_str = ','.join(choose_AP)
    AP_str.rstrip(',')

    selected = cursor.execute('SELECT Id,' + AP_str + ' FROM wifi_table')  # 读取数据库数据

    # 正则初始化
    # pattern1 = re.compile(r"MAC='(\d+):(\d+):(\d+):(\d+):(\d+):(\d+)'")  # 用于匹配MAC地址
    pattern1 = re.compile(r"MAC='134:243:235:174:194:240'")  # 用于匹配MAC地址
    pattern2 = re.compile(r"level=(-\d+)")  # 用于匹配RSSI
    pattern3 = re.compile(r'(\d+),(\d+)')  # 用于匹配id，对应坐标值

    # 过滤数据
    for row in selected:
        x_temp = []
        y_temp = []
        Location = pattern3.search(row[0])
        # 能找到坐标，且过滤x为0的点
        if Location.group(1) == '11':
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
            if Location.group(2) == '5':
                y_train.append(y_temp)
                x_train.append(x_temp[0])
                x_temp = []  # 清空列表
                y_temp = []

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
    print('Close file')
print('########## 1 ##########')
