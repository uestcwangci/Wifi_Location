# -*- coding: utf-8 -*-
import sqlite3 as sq
import re
import numpy as np
import scipy.io as sio

import os.path

# 获取文件夹路径
Data_path = os.path.abspath('..\\..\\DataBase')
mac_name_dic = {}
# 读取全部ap列表
connection = sq.connect(Data_path + '\\' + '4ESP8266AP.db')
cursor = connection.cursor()
select = cursor.execute('SELECT ID, Area, AreaNum, Name, Mac, Date FROM ap_table_id')
idAP_list = []
area_list = []
area_num_list = []
name_list = []
mac_list = []
date_list = []
for row in select:
    idAP_list.append(row[0])
    area_list.append(row[1])
    area_num_list.append(row[2])
    name_list.append(row[3])
    mac_list.append(row[4])
    name = row[3]
    mac = row[4]
    date_list.append(row[-1])
    mac_name_dic[mac] = name
ap_num = len(mac_name_dic)  # 总AP个数
a=1
# connection.close()
# cursor.close()
x_train = []
y_train = []
for file_num in range(1):
    if file_num == 0:
        databaseName = '10m.db'
    elif file_num == 1:
        databaseName = 'wifiInfo2.db'
    elif file_num == 2:
        databaseName = 'wifiInfo3.db'
    elif file_num == 3:
        databaseName = '1wifiInfo.db'
    connection = sq.connect(Data_path + '\\' + databaseName)
    cursor = connection.cursor()
    mac_str = ''
    for key in mac_name_dic.keys():
        mac_str += 'Mac_'
        mac_str += key.replace(':', '_')
        mac_str += ','
        mac_name_dic[key] = -100
    mac_str = mac_str.rstrip(',')
    # select = cursor.execute('SELECT Loc, Mark,' + mac_str + ' FROM wifi_table')
    select = cursor.execute('SELECT ID, Loc, Mark,' + mac_str + ' FROM wifi_table_id')
    x_temp = []
    y_temp = []
    for row in select:
        idWifi = row[0]
        loc = row[1]
        if loc != 0:
            y_temp.append(int(loc))
            mark = row[2]
            for i in range(ap_num):
                x_temp.append(int(row[i + 3]))
            date = row[-1]
            x_train.append(x_temp)
            y_train.append(y_temp)
            x_temp = []
            y_temp = []
    cursor.close()
    connection.close()

    # 保存数据
    ######################################################
    x_train_array = np.array(x_train)
    sio.savemat('x_set.mat', {'x_set': x_train_array})
    y_train_array = np.array(y_train)
    sio.savemat('y_set.mat', {'y_set': y_train_array})

    print('Save set successfully | File:%2i |' % (file_num + 1))


print('Database done')
print('########## 1 ##########')



# # 读取wifi功率
# FILE_NUM = 1  # 需要载入的数据库数量
# for num_file in range(FILE_NUM):
#     # 根据需要录入的文件总数读取数据库数据
#     if num_file == 0:
#         DatabaseName = '5Loc'
#     elif num_file == 1:
#         DatabaseName = 'myTest_180613_1'
#     else:
#         continue
#     # Sqlite3连接
#     conn = sq.connect(Data_path + '\\' + DatabaseName + '.db')  # 连接数据库
#     cursor = conn.cursor()
#     # print('Open database successfully')
#     # x存储MAC以及RSSI    y存储label值
#     x_train = []
#     y_train = []
#     # 将AP1，AP2……拼接在一个字符串中
#     choose_AP = []
#     for num_AP in range(TOTAL_AP):
#         choose_AP.append('AP' + str(num_AP + 1))
#     AP_str = ','.join(choose_AP)
#
#     selected = cursor.execute('SELECT Id,' + AP_str + ',Date FROM main.stu_table')  # 读取数据库数据
#     # 正则初始化
#     MAC_regex = re.compile(r"MAC = '(\w+:\w+:\w+:\w+:\w+:\w+)'")  # 用于匹配MAC地址
#     RSSI_regex = re.compile(r"level = (-\d+)")  # 用于匹配RSSI
#     Loc_regex = re.compile(r'(\d+),(\d+)')  # 用于匹配id，对应坐标值
#     Date_regex = re.compile(r'(\d+-\d+-\d+)')  # 用于匹配日期
#     Name_regex = re.compile(r"Name = '(\w+)'")
#     SSID_regex = re.compile(r'SSID')
#     #######################################################################
#     # 过滤数据
#     x_last = {}
#     y_last = []
#     for row in selected:
#         # 循环开始时初始化列表
#         myAP = {'dc:ef:09:0c:ea:f8': -100, 'dc:ef:09:0c:ea:fc': -100,
#                 '50:64:2b:9e:b0:4d': -100, '50:64:2b:9e:b0:4e': -100,
#                 '40:31:3c:1c:ca:29': -100, '40:31:3c:1c:ca:2a': -100,
#                 'e4:a7:c5:fd:b0:7c': -100, 'e4:a7:c5:fd:b0:80': -100,
#                 'a4:93:3f:ce:92:2c': -100, 'a4:93:3f:ce:92:30': -100}
#         y_temp = []
#         Location = Loc_regex.search(row[0])
#         date = Date_regex.search(row[-1])
#         SSID = SSID_regex.search(row[1])
#         # print(RSSI_regex.search(row[1]).group())
#         # print(Location.group())
#         # 能找到坐标，且过滤x为0的点,或首个RSSI为-100dBm的点
#         # if Location and Location.group(1) != '0' and RSSI_regex.search(row[1]).group(1) != '-100':
#         if Location and Location.group(1) != '0' and not SSID:
#             y_temp.append(int(Location.group(1)))
#             # 每次循环放入1个AP
#             for i in range(TOTAL_AP):
#                 MAC = MAC_regex.search(row[i + 1])
#                 RSSI = RSSI_regex.search(row[i + 1])
#                 if MAC and RSSI and (MAC.group(1) in APlist.keys()):
#                     myAP[MAC.group(1)] = int(RSSI.group(1))
#             flag = 0
#             for rssi in myAP.values():
#                 if rssi == -100:
#                     flag = 1
#                     break
#             if flag == 0:
#                 # 当下一个坐标与上一个不同，MAC及RSSI与上一个相同时，过滤此次信息
#                 if y_temp != y_last and myAP == x_last:
#                     pass
#                 else:
#                     x_last = myAP.copy()
#                     y_last = y_temp.copy()
#                     # 根据标识符分类
#                     if Location.group(2) == '7':  # 标识符
#                         y_train.append(y_temp)
#                         x_train.append(list(myAP.values()))
#
#                     # elif Location.group(2) == '1':
#                     #     y_test.append(y_temp)
#                     #     x_test.append(x_temp)
#                     #     x_temp = []
#                     #     y_temp = []
#                     else:
#                         pass
#
#     # 保存数据
#     ######################################################
#     x_train_array = np.array(x_train)
#     sio.savemat('x_set_' + DatabaseName + '.mat', {'x_set_' + DatabaseName: x_train_array})
#     y_train_array = np.array(y_train)
#     sio.savemat('y_set_' + DatabaseName + '.mat', {'y_set_' + DatabaseName: y_train_array})
#
#     print('Save set successfully | File:%2i |' % (num_file + 1))
#
#     cursor.close()
#     conn.close()
# print('Database done')
# print('########## 1 ##########')
