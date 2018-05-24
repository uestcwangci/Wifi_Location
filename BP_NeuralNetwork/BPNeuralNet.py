# -*- coding: utf-8 -*-

import math
import numpy as np
import scipy.io as sio
import os

# 获取文件夹路径
AP_path = os.path.abspath('..\\AP_Filter\\')
cur_path = os.getcwd()

# 读入训练数据
################################################################################################
filename = AP_path + 'AP_train.mat'     # raw_input() # 换成raw_input()可自由输入文件名
sample = sio.loadmat(filename)
sample = sample["x_train"].tolist()
# 特征向量归一化
for iSample in sample:
    for count in range(len(iSample)):
        if count % 7 == 0:
            iSample[count] = (iSample[count] + 100) / 100
        else:
            iSample[count] = iSample[count] / 255

print(sample)
filename = AP_path + 'label_train.mat'   # raw_input() # 换成raw_input()可自由输入文件名
label = sio.loadmat(filename)
label = label["y_train"]

##################################################################################################


# 神经网络配置
##################################################################################################
samp_num = len(label)      # 样本总数
inp_num = len(sample[0])    # 输入层节点数
out_num = 69                # 输出节点数
hid_num = 15  # 隐层节点数(经验公式) h=sqrt(m+n)+a m为输入结点数，n为输出结点数，a为1~10整数
w1 = 0.2*np.random.random((inp_num, hid_num)) - 0.1   # 初始化输入层权矩阵
w2 = 0.2*np.random.random((hid_num, out_num)) - 0.1   # 初始化隐层权矩阵
hid_offset = np.zeros(hid_num)     # 隐层偏置向量
out_offset = np.zeros(out_num)     # 输出层偏置向量
inp_lrate = 0.3             # 输入层权值学习率
hid_lrate = 0.3             # 隐层学权值习率
err_th = 0.01                # 学习误差门限


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
    if count % 100 == 0:
        print(count)
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
    hid_delta = hid_act * (1-hid_act) * np.dot(w2, out_delta)                   # 隐层delta计算
    for i in range(0, out_num):
        w2[:, i] += hid_lrate * out_delta[i] * hid_act   # 更新隐层到输出层权向量
    for i in range(0, hid_num):
        w1[:, i] += inp_lrate * hid_delta[i] * sample[count]      # 更新输出层到隐层的权向量

    out_offset += hid_lrate * out_delta                             # 输出层偏置更新
    hid_offset += inp_lrate * hid_delta

###################################################################################################

# 测试网络
###################################################################################################
filename = AP_path + 'AP_test.mat'  # raw_input() # 换成raw_input()可自由输入文件名
test = sio.loadmat(filename)
test_s = test["x_test"].tolist()
# 特征向量归一化
for iTest in test_s:
    for count in range(len(iTest)):
        if count % 7 == 0:
            iTest[count] = (iTest[count] + 100) / 100
        else:
            iTest[count] = iTest[count] / 255

# 读入测试数据
######################################################################
filename = AP_path + 'label_test.mat'  # raw_input() # 换成raw_input()可自由输入文件名
test_label = sio.loadmat(filename)
test_l = test_label["y_test"]
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
print('对应位置准确个数: ' + right)
print('对应位置测试个数: ' + numbers)
result = right/numbers
print('对应位置准确率: ' + result)
sum_right = right.sum()
print('准确率均值: ' + sum_right/len(test_s))
###################################################################################################
# 输出网络
###################################################################################################
Network = open("MyNetWork.txt", 'w')
Network.write(str(inp_num))
Network.write('\n')
Network.write(str(hid_num))
Network.write('\n')
Network.write(str(out_num))
Network.write('\n')
for i in w1:
    for j in i:
        Network.write(str(j))
        Network.write(' ')
    Network.write('\n')
Network.write('\n')

for i in w2:
    for j in i:
        Network.write(str(j))
        Network.write(' ')
Network.write('\n')

Network.close()
