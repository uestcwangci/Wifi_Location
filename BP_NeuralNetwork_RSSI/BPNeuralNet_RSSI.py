# -*- coding: utf-8 -*-

import math
import numpy as np
import scipy.io as sio
import os
import GlobalVarible.getter as glovar

MIN_AP = glovar.MIN_AP
MAX_AP = glovar.MAX_AP
# 获取文件夹路径
AP_path = os.path.abspath('..\\mat_data\\ForRssi')
cur_path = os.getcwd()
right_rate = []  # 保存所有AP，隐藏层及其对应的准确率
top_right = {'Input': 0, 'Hide': 0, 'Out': 0, 'AP': 0, 'Accuracy': 0.0, 'W1': [], 'W2': [], 'Hid_off': [], 'Out_off': []}


for iAP in range(MIN_AP, MAX_AP + 1):
    # 读入训练数据
    ################################################################################################
    # 读入特征值训练集
    filename = AP_path + '\\x_train_rRssi_AP' + str(iAP) + '.mat'
    sample = sio.loadmat(filename)
    sample = sample['x_train_rRssi_AP' + str(iAP)].tolist()
    # 特征向量归一化
    for iSample in sample:
        for count in range(len(iSample)):
            if count % 7 == 0:
                iSample[count] /= 100.0
            else:
                iSample[count] /= 255.0
    sample = np.array(sample)
    # 读入标签训练集
    filename = AP_path + '\\y_train_rRssi.mat'
    label = sio.loadmat(filename)
    label = label['y_train_rRssi'] - 1

    for hid_num in range(15, 25 + 1):   # 隐层节点数(经验公式) h=sqrt(m+n)+a m为输入结点数，n为输出结点数，a为1~10整数
        ##################################################################################################
        # 神经网络配置
        samp_num = len(label)  # 样本总数
        inp_num = len(sample[0])  # 输入层节点数
        out_num = 9  # 输出节点数
        w1 = 0.2 * np.random.random((inp_num, hid_num)) - 0.1  # 初始化输入层权矩阵
        w2 = 0.2 * np.random.random((hid_num, out_num)) - 0.1  # 初始化隐层权矩阵
        top_w1 = w1.copy()
        hid_offset = np.zeros(hid_num)  # 隐层偏置向量
        out_offset = np.zeros(out_num)  # 输出层偏置向量
        inp_lrate = 0.3  # 输入层权值学习率
        hid_lrate = 0.3  # 隐层学权值习率
        err_th = 0.01  # 学习误差门限

        ###################################################################################################

        # 必要函数定义
        ###################################################################################################
        def get_act(x):
            act_vec = []
            for iX in x:
                act_vec.append(1 / (1 + math.exp(-iX)))
            act_vec = np.array(act_vec)
            return act_vec


        def get_err(error):
            return 0.5*np.dot(error, error)


        ###################################################################################################

        # 训练——可使用err_th与get_err() 配合，提前结束训练过程
        ###################################################################################################

        for count in range(0, samp_num):

            t_label = np.zeros(out_num)
            t_label[label[count]] = 1
            # 前向过程
            hid_value = np.dot(sample[count], w1) + hid_offset       # 隐层值
            hid_act = get_act(hid_value)                # 隐层激活值
            out_value = np.dot(hid_act, w2) + out_offset             # 输出层值
            out_act = get_act(out_value)                # 输出层激活值

            # 后向过程
            e = t_label - out_act                          # 输出值与真值间的误差
            out_delta = e * out_act * (1-out_act)                                       # 输出层delta计算
            hid_delta = hid_act * (1-hid_act) * np.dot(w2, out_delta)  # 隐层delta计算
            for i in range(0, out_num):
                w2[:, i] += hid_lrate * out_delta[i] * hid_act   # 更新隐层到输出层权向量
            for i in range(0, hid_num):
                w1[:, i] += inp_lrate * hid_delta[i] * sample[count]      # 更新输出层到隐层的权向量

            out_offset += hid_lrate * out_delta                             # 输出层偏置更新
            hid_offset += inp_lrate * hid_delta

        ###################################################################################################

        # 测试网络
        ###################################################################################################
        # 保存不同AP，不同隐藏层平均准且率
        right_temp = []
        # 读入特征测试集
        filename = AP_path + '\\x_test_rRssi_AP' + str(iAP) + '.mat'  # raw_input() # 换成raw_input()可自由输入文件名
        test = sio.loadmat(filename)
        test_s = test['x_test_rRssi_AP' + str(iAP)].tolist()
        # 特征向量归一化
        for iTest in test_s:
            for count in range(len(iTest)):
                if count % 7 == 0:
                    iTest[count] /= 100.0
                else:
                    iTest[count] /= 255.0
        test_s = np.array(test_s)
        # 读入标签测试集
        filename = AP_path + '\\y_test_rRssi.mat'  # raw_input() # 换成raw_input()可自由输入文件名
        test_label = sio.loadmat(filename)
        test_l = test_label['y_test_rRssi'] - 1

        right = np.zeros(out_num)  # 对应位置准确率
        numbers = np.zeros(out_num)  # 存放对应位置label的个数
        #######################################################################

        # 统计测试数据中各个数字的数目
        for i in test_l:
            numbers[i] += 1

        for count in range(len(test_s)):
            hid_value = np.dot(test_s[count], w1) + hid_offset       # 隐层值
            hid_act = get_act(hid_value)                # 隐层激活值
            out_value = np.dot(hid_act, w2) + out_offset             # 输出层值
            out_act = get_act(out_value)                # 输出层激活值
            if np.argmax(out_act) == test_l[count]:
                right[test_l[count]] += 1
        print('\n隐藏层数为%2i, AP = %2i' % (hid_num, iAP))
        # print('对应位置准确个数: ')
        # print(right)
        # print('对应位置测试个数: ')
        # print(numbers)
        result = right/numbers
        print('对应位置准确率: ')
        print(result)
        sum_right = right.sum()
        print('准确率均值: ')
        average = sum_right/len(test_s)
        print(average)

        right_temp.append('Hide:%2s' % str(hid_num))
        right_temp.append('AP:%2s' % str(iAP))
        right_temp.append('Rate:' + str(average))
        right_rate.append(right_temp)
        right_temp = []

        if average > top_right['Accuracy']:
            top_right['Input'] = inp_num
            top_right['Hide'] = hid_num
            top_right['Out'] = out_num
            top_right['AP'] = iAP
            top_right['Accuracy'] = average
            top_right['W1'] = list(w1)
            top_right['W2'] = list(w2)
            top_right['Hid_off'] = hid_offset
            top_right['Out_off'] = out_offset

print('##########################################################\n'
      '最大准确率:\nHide:%d, AP:%d, Accuracy:%0.3f\n'
      '##########################################################'
      % (top_right['Hide'], top_right['AP'], top_right['Accuracy']))


# 输出网络、输出偏置向量
###################################################################################################
def para_out(file):
    output = open(file, 'w')
    if 'w1_rssi.txt' == file:
        for iW in top_right['W1']:
            for iw in iW:
                output.write(str(iw))
                output.write(' ')
            output.write('\n')
    elif 'w2_rssi.txt' == file:
        for iW in top_right['W2']:
            for iw in iW:
                output.write(str(iw))
                output.write(' ')
            output.write('\n')
    elif 'hid_offset_rssi.txt' == file:
        for iSet in top_right['Hid_off']:
            output.write(str(iSet))
            output.write('\n')
    elif 'out_offset_rssi.txt' == file:
        for iSet in top_right['Out_off']:
            output.write(str(iSet))
            output.write('\n')
    output.close()
##################################################################################################


# 输出结果
###################################################################################################
Network = open("NetWork_rssi.txt", 'w')
for key, value in top_right.items():
    if 'W1' == key:
        Network.write('\nw1:')
        for i in value:
            Network.write('\n')
            for j in i:
                Network.write(str(j))
                Network.write(' ')
    elif 'W2' == key:
        Network.write('\nw2:')
        for i in top_right['W2']:
            Network.write('\n')
            for j in i:
                Network.write(str(j))
                Network.write(' ')
    elif 'Hid_off' == key or 'Out_off' == key:
        Network.write('\n')
        Network.write(key + ':\n')
        Network.write(str(top_right[key]))
    else:
        Network.write(key)
        Network.write(':')
        Network.write(str(value))
        Network.write(' | ')
Network.close()
###################################################################################################


para_out('w1_rssi.txt')
para_out('w2_rssi.txt')
para_out('hid_offset_rssi.txt')
para_out('out_offset_rssi.txt')

# 输出分布结果
###################################################################################################
Accuracy = open('AccuracyRate_rssi.txt', 'w')

for iRate in right_rate:
    string_rate = ' | '.join(iRate)
    Accuracy.write(string_rate)
    Accuracy.write('\n')

Accuracy.close()


