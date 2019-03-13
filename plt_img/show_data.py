#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : show_data.py 
@Time: 2018/12/4 12:24
@Desc:
"""

import sqlite3 as sq
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum, unique


connection = sq.connect('maiwaidi.db')
cursor = connection.cursor()
select = cursor.execute('select * from main.wifi_table')
id_list = []
x_list = []
y_list = []
esp1_list = []
esp2_list = []
esp3_list = []
esp4_list = []
esp5_list = []
m1_list = []
m15g_list = []
h1_list = []
h15g_list = []
h2_list = []
h25g_list = []
kb240_list = []
kb240ac_list = []
# date_list = []
for row in select:
    id_list.append(row[0])
    x_list.append(row[1])
    y_list.append(row[2])
    esp1_list.append(int(row[3]))
    esp2_list.append(int(row[4]))
    esp3_list.append(int(row[5]))
    esp4_list.append(int(row[6]))
    esp5_list.append(int(row[7]))
    # m1_list.append(int(row[7]))
    m15g_list.append(int(row[8]))
    # h1_list.append(int(row[9]))
    # h15g_list.append(int(row[10]))
    # h2_list.append(int(row[11]))
    # h25g_list.append(int(row[12]))
    kb240_list.append(int(row[-3]))
    kb240ac_list.append(int(row[-2]))

    # date_list.append(row[-1])

cursor.close()
connection.close()


# @unique
# class AP(Enum):
#     esp1 = esp1_list
#     esp2 = esp2_list
#     esp3 = esp3_list
#     esp4 = esp4_list
#     esp5 = esp5_list
#     m1 = m1_list
#     m15g = m15g_list
#     h1 = h1_list
#     h15g = h15g_list
#     h2 = h2_list
#     h25g = h25g_list
#     kb240 = kb240_list
#     kb240ac = kb240ac_list


def visualize(ap):
    sort_tuple = np.unique(ap, return_counts=True)
    n = len(ap)
    plt.rcParams['savefig.dpi'] = 300  # 图片像素
    plt.rcParams['figure.dpi'] = 300  # 分辨率
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.bar(sort_tuple[0], sort_tuple[1]/n, color='g')
    plt.xlabel(u'RSSI')
    plt.ylabel(u'Ratio')
    plt.text(sort_tuple[0][0], np.max(sort_tuple[1]/n), "var:%2.2f" % np.array(ap).var())
    if sort_tuple[0][0] == -100:
        plt.text(-100, float(sort_tuple[1][0])/n*1.0, '%.4f' % (float(sort_tuple[1][0])/n))
    # plt.title(str(AP(ap)))
    plt.subplot(1, 2, 2)
    x = np.linspace(0, n, n)
    plt.plot(x, ap, '.')
    # plt.title(str(AP(ap)))
    plt.xlabel('Time')
    plt.ylabel('Rssi')
    plt.show()


visualize(esp1_list)
visualize(esp2_list)
visualize(esp3_list)
visualize(esp4_list)
visualize(esp5_list)
# visualize(m1_list)
visualize(m15g_list)
# visualize(h1_list)
# visualize(h15g_list)
# visualize(h2_list)
# visualize(h25g_list)
visualize(kb240_list)
visualize(kb240ac_list)




