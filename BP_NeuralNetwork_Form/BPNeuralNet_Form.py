# -*- coding: utf-8 -*-

import math
import numpy as np
import scipy.io as sio
import os

# 获取文件夹路径
mat_path = os.path.abspath('..\\mat_data\\ForForm')
cur_path = os.getcwd()


# 读入训练数据
################################################################################################
# 读入特征值训练集
filename = mat_path + '\\x_train_rForm.mat'
sample = sio.loadmat(filename)
sample = sample['x_train_rForm'].astype('float32')
# 特征向量归一化
sample /= 100.0
# sample = np.array(sample)
# 读入标签训练集
filename = mat_path + '\\y_train_rForm.mat'
label = sio.loadmat(filename)
label = label['y_train_rForm'] - 1
# 保存数据结点数,隐藏结点，输出节点数，最大准确率,权值矩阵，偏置向量
top_right = {'Input': 0, 'Hide': 0, 'Out': 0, 'Accuracy': 0.0, 'W1': [], 'W2': [], 'Hid_off': [], 'Out_off': []}
right_rate = []  # 保存所有AP，隐藏层及其对应的准确率


for hid_num in range(10, 30):   # 隐层节点数(经验公式) h=sqrt(m+n)+a m为输入结点数，n为输出结点数，a为1~10整数
    ##################################################################################################
    # 神经网络配置
    samp_num = len(label)  # 样本总数
    inp_num = len(sample[0])  # 输入层节点数
    out_num = 9  # 输出节点数
    w1 = 0.2 * np.random.random((inp_num, hid_num)) - 0.1  # 初始化输入层权矩阵
    w2 = 0.2 * np.random.random((hid_num, out_num)) - 0.1  # 初始化隐层权矩阵
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
        # if count % 10000 == 0 and count != 0:
        #     print(count)
        t_label = np.zeros(out_num)
        t_label[label[count]] = 1
        # 前向过程
        hid_value = np.dot(sample[count], w1) + hid_offset       # 隐层值
        hid_act = get_act(hid_value)                # 隐层激活值
        out_value = np.dot(hid_act, w2) + out_offset             # 输出层值
        out_act = get_act(out_value)                # 输出层激活值

        # 后向过程
        e = t_label - out_act                          # 输出值与真值间的误差
        # if err_th > get_err(e):
        #     print(count)
        #     break
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
    # 保存不同隐藏层平均准且率
    right_temp = []
    # 读入特征测试集
    filename = mat_path + '\\x_test_rForm.mat'  # raw_input() # 换成raw_input()可自由输入文件名
    test = sio.loadmat(filename)
    test_s = test['x_test_rForm'].astype('float32')
    # 特征向量归一化
    test_s /= 100.0
    # test_s = np.array(test_s)
    # 读入标签测试集
    filename = mat_path + '\\y_test_rForm.mat'  # raw_input() # 换成raw_input()可自由输入文件名
    test_label = sio.loadmat(filename)
    test_l = test_label['y_test_rForm'] - 1

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
    result = right / numbers
    sum_right = right.sum()
    average = sum_right/len(test_s)
    print('\n隐藏层数为%2i' % hid_num)
    print('对应位置准确个数: ')
    print(right)
    print('对应位置测试个数: ')
    print(numbers)
    print('对应位置准确率: ')
    print(result)
    print('准确率均值: ' + str(average))
    # print(average)

    right_temp.append('Hide:%2s' % str(hid_num))
    right_temp.append('Rate:' + str(average))
    right_rate.append(right_temp)
    right_temp = []

    if average > top_right['Accuracy']:
        top_right['Input'] = inp_num
        top_right['Hide'] = hid_num
        top_right['Out'] = out_num
        top_right['Accuracy'] = average
        top_right['W1'] = list(w1)
        top_right['W2'] = list(w2)
        top_right['Hid_off'] = hid_offset
        top_right['Out_off'] = out_offset


# 输出网络、输出偏置向量
###################################################################################################
def para_out(file):
    output = open(file, 'w')
    if 'w1_form.txt' == file:
        for iW in top_right['W1']:
            for iw in iW:
                output.write(str(iw))
                output.write(' ')
            output.write('\n')
    elif 'w2_form.txt' == file:
        for iW in top_right['W2']:
            for iw in iW:
                output.write(str(iw))
                output.write(' ')
            output.write('\n')
    elif 'hid_offset_form.txt' == file:
        for iSet in top_right['Hid_off']:
            output.write(str(iSet))
            output.write('\n')
    elif 'out_offset_form.txt' == file:
        for iSet in top_right['Out_off']:
            output.write(str(iSet))
            output.write('\n')
    output.close()
##################################################################################################


# # 输出偏置向量
# ###################################################################################################
# def offset_out(file):
#     offset = open(file, 'w')
#     if 'hid_offset.txt' == file:
#         for iSet in hid_offset:
#             offset.write(iSet)
#             offset.write('\n')
#     elif 'out_offset.txt' == file:
#         for iSet in out_offset:
#             offset.write(iSet)
#             offset.write('\n')
#     offset.close()
# ##################################################################################################


# 输出结果
###################################################################################################
Network = open("NetWork_form.txt", 'w')
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
para_out('w1_form.txt')
para_out('w2_form.txt')
para_out('hid_offset_form.txt')
para_out('out_offset_form.txt')


# 输出分布结果
###################################################################################################
Accuracy = open('AccuracyRate_form.txt', 'w')

for iRate in right_rate:
    string_rate = ' | '.join(iRate)
    Accuracy.write(string_rate)
    Accuracy.write('\n')

Accuracy.close()
print('Hide: %d, Accuracy %0.3f' % (top_right['Hide'], top_right['Accuracy']))




