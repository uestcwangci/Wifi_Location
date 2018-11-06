#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : tfBP.py 
@Time: 2018/10/24 22:11
@Desc:
"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys
import scipy.io as sio

# 生成与加载数据
# 构造满足一元二次方程的函数


def build_data():

    sample = sio.loadmat('10m.mat')
    # total = sample['total']

    x = (sample['x'] + 100.0) / 100.0
    y = (sample['y'] - 1).tolist()
    for j in range(len(y)):
        y[j] = y[j][0]

    # 把labels化为one_hot类型
    max_batch = max(y) + 1
    y = tf.one_hot(y, max_batch)
    # batch_size = tf.size(y)
    # labels = tf.expand_dims(y, 1)
    # indices = tf.expand_dims(tf.range(0, batch_size, 1), 1)
    # concated = tf.concat([indices, labels], 1)
    # onehot_labels = tf.sparse_to_dense(concated, tf.stack([batch_size, max_batch]), 1.0, 0.0)

    return x, y


# 构建网络模型
def add_layer(inputs, in_size, out_size, activation_function=None):
    # 构建权重 : in_size * out_size 大小的矩阵 权重w的初始值设定为标准差为0.1的标准截断的正态分布
    # weights = tf.Variable(tf.zeros([in_size, out_size]))
    weights = tf.Variable(tf.truncated_normal([in_size, out_size], stddev=0.1))
    # 构建偏置 : 1 * out_size 的矩阵
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    # 矩阵相乘
    Wx_plus_b = tf.matmul(inputs, weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)

    return outputs  # 得到输出数据


# 可视化tensor参数
def visualization(param):
    visuSess = tf.InteractiveSession()
    visuSess.run(tf.global_variables_initializer())
    print(visuSess.run(param))


input_size = 4    # 输入层结点数
hidden_layers = 9  # 隐藏层节点数
output_size = 9    # 输出层结点数

xs = tf.placeholder(tf.float32, [None, input_size])
ys = tf.placeholder(tf.float32, [None, output_size])

# 构建输入层到隐藏层,假设隐藏层有 hidden_layers 个神经元
h1 = add_layer(xs, input_size, hidden_layers, activation_function=tf.nn.relu)
# 构建隐藏层到隐藏层
# h2 = add_layer(h1, hidden_layers, hidden_layers, activation_function=tf.nn.sigmoid)
# 构建隐藏层到隐藏层
# h3 = add_layer(h2, hidden_layers, hidden_layers, activation_function=tf.nn.sigmoid)
# 构建隐藏层到输出层
prediction = add_layer(h1, hidden_layers, output_size, activation_function=None)

# 接下来构建损失函数: 计算输出层的预测值和真是值间的误差,对于两者差的平方求和,再取平均,得到损失函数.运用Adam算法,以0.1的效率最小化损失
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))

train_step = tf.train.AdadeltaOptimizer(0.2).minimize(loss)  # 优化算法选取SGD,随机梯度下降
correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(ys, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print('将计算图写入事件文件,在TensorBoard里查看')
# writer = tf.summary.FileWriter(logdir='logs/8_2_BP', graph=tf.get_default_graph())
# writer.close()

# 训练模型
x_data, y_data = build_data()

# 我们让TensorFlow训练10000次,每1000次输出训练的损失值:
loss_list, pre_list = [], []
init = tf.global_variables_initializer()
train_num = 10000
with tf.Session() as sess:
    sess.run(init)

    for i in range(train_num):
        sess.run(train_step, feed_dict={xs: x_data, ys: sess.run(y_data)})
        # sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
        if i % 100 == 0:
            loss_ = sess.run(loss, feed_dict={xs: x_data, ys: sess.run(y_data)})
            train_accuracy = accuracy.eval(feed_dict={xs: x_data, ys: sess.run(y_data)})
            print("step %d\naccuracy: %g, loss: %g" %
                  (i, train_accuracy, loss_))
            loss_list.append(loss_)
            pre_list.append(train_accuracy)

    print("test accuracy %g" % accuracy.eval(feed_dict={xs: x_data, ys: sess.run(y_data)}))

    i = np.arange(0, train_num, 100)
    plt.subplot(1, 2, 1)
    plt.plot(i, loss_list)
    plt.xlabel('train step')
    plt.ylabel('cost')
    plt.subplot(1, 2, 2)
    plt.plot(i, pre_list)
    plt.xlabel('train step')
    plt.ylabel('accuracy')
    plt.show()




