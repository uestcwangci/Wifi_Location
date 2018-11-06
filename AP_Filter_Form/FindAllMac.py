# -*- coding: utf-8 -*-
# 根据数据库找到区域内所有AP的name及RSSI
import sqlite3 as sq
import re
import csv
import numpy as np
import scipy.io as sio

import os.path

# 获取文件夹路径
Data_path = os.path.abspath('..\\DataBase')

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
    # 初始化字典 key存储SSID value存储MAC
    allAP = {}
    name = ''
    mac = ''
    # 初始化Mac列表
    MacList = []

    # 将AP1，AP2……AP25拼接在一个字符串中,数据库能采集到最大AP25
    choose_AP = []
    for num_AP in range(25):
        choose_AP.append('AP' + str(num_AP + 1))
    AP_str = ','.join(choose_AP)
    selected = cursor.execute('SELECT Id,' + AP_str + ',Date FROM stu_table')  # 读取数据库数据
    # 正则初始化
    MAC_regex = re.compile(r"MAC = '(\w+:\w+:\w+:\w+:\w+:\w+)'")  # 用于匹配MAC地址
    RSSI_regex = re.compile(r"level = (-\d+)")  # 用于匹配RSSI
    Loc_regex = re.compile(r'(\d+),(\d+)')  # 用于匹配id，对应坐标值
    Date_regex = re.compile(r'(\d+-\d+-\d+)')  # 用于匹配日期
    Name_regex = re.compile(r"Name = '(\w+)'")
    #######################################################################
    # 过滤数据
    # 每次遍历放入的是一行采样数据
    for row in selected:
        Location = Loc_regex.search(row[0])
        # 能找到坐标，且过滤x为0的点,或首个RSSI为-100dBm的点,只选取标识符为5的点
        if Location and Location.group(1) != '0' and Location.group(2) == '5' \
                and RSSI_regex.search(row[1]).group(1) != '-100':
            # 每次循环放入1个AP
            for i in range(25):
                MAC = MAC_regex.search(row[i + 1])
                RSSI = RSSI_regex.search(row[i + 1])
                SSID = SSID_regex.search(row[i + 1])
                DATE = Date_regex.search(row[-1])
                # 当遍历到RSSI = -100dBm的AP时终止
                if RSSI and RSSI.group(1) == '-100':
                    break
                if SSID and MAC:
                    mac = MAC.group(1)
                    name = SSID.group(1)
                    # date = DATE.group(1)

                    if mac not in allAP.keys():
                        allAP[mac] = name
    for iMac in allAP.keys():
        iMac = iMac.replace(':', ' ')
        # iMacList = iMac.split(':')
        MacList.append(iMac)
    # print(MacList)
    # print(allAP)

    ######################################################
    # 功能：将一字典写入到csv文件中
    # 输入：文件名称，数据字典
    def createDictCSV (filename="", datadict=None):
        if datadict is None:
            datadict = {}
        idd = 1
        with open(filename, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(['ID', 'MAC', 'Name'])
            for k, v in datadict.items():
                csvWriter.writerow([idd, k, v])
                idd += 1
            csvFile.close()

    ######################################################
    # 将MAC按照125 44 128 1 54 99的格式按行写入txt文件中
    # input：文件名，数据列表
    def creatListTxt(filename='', datalist=None):
        if datalist is None:
            datalist = []
        file = open(filename, 'w')
        for data in datalist:
            file.write(data)
            file.write('\n')
        file.close()


    createDictCSV('allAP.csv', allAP)
    creatListTxt('allMac.txt', MacList)
    print('Save set successfully | File:%2i |' % (num_file + 1))

    cursor.close()
    conn.close()
    # print('Close file')
print('Find all SSID')
print('########## 1 ##########')
