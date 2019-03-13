# -*- coding: utf-8 -*-
import sqlite3 as sq
import numpy as np
import scipy.io as sio
import os.path

MAX_LOC = 7
FILE_NUM = 1
# 获取文件夹路径
Data_path = os.path.abspath('..\\..\\DataBase')
data_name = 'online4'
mac_name_dic = {}
# 读取全部ap列表
# connection = sq.connect(Data_path + '\\' + data_name + 'AP.db')
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

total_train = []
for file_num in range(FILE_NUM):
    if file_num == 0:
        # databaseName = data_name + 'WiFi.db'
        databaseName = data_name + '.db'
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
    rssi_temp = []
    total_temp = []
    for row in select:
        idWifi = row[0]
        for i in range(ap_num):
            rssi_temp.append(float(row[i + 3]))
        date = row[-1]
        x_temp = float(row[1])
        y_temp = float(row[2])
        total_temp = rssi_temp
        total_temp.append(x_temp)
        total_temp.append(y_temp)
        # total_temp.append((x_temp-1)*MAX_LOC + y_temp)
        total_train.append(total_temp)
        rssi_temp = []
        total_temp = []

    cursor.close()
    connection.close()


    # 保存数据
    ######################################################
    total_array = np.array(total_train)
    sio.savemat(data_name + '.mat', {'total': total_array})

    print('Save set successfully | File:%2i |' % (file_num + 1))


print('Database done')
print('########## 1 ##########')


# # # 获取列表的最后一个元素
# def takeLastData(elem):
#     return elem[-1]
#
#
# total = sio.loadmat(data_name + '.mat')['total'].tolist()
# afterSort = []
#
# total.sort(key=takeLastData)
# total_array = np.array(total)[:, 0:-1]
# sio.savemat(data_name + '.mat', {'total': total_array})
#
#
# print('Sort done')
# print('########## 2 ##########')

