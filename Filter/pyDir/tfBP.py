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
import scipy.io as sio

# 生成与加载数据
# 构造满足一元二次方程的函数

# 训练True，测试False
isTrain = True

NN = 3
def some_fun(pre_data):
    n = len(pre_data)
    where, zhi = [], []
    for i in range(n):
        where.append(np.argsort(pre_data[i, :])[-NN:] + 1)  # 找到值最大3个位置
        zhi.append(np.sort(pre_data[i, :])[-NN:])  # 找到值最大的3个值
    for i in range(n):
        tt = []
        for j in range(NN):
            temp = []
            y1 = where[i][j] % 3
            if y1 == 0:
                y1 = 3
            x1 = (where[i][j] - y1) / 3 + 1


            temp.append(x1)
            temp.append(y1)
            tt.append(np.array(temp))
        where[i] = tt
    result = []
    for i in range(n):
        temp = [0, 0]
        for j in range(NN):
            temp = temp + zhi[i][j] * where[i][j]
        result.append(temp)
    return np.array(result)





def build_data():
    sample = sio.loadmat('zhuanli.mat')
    # sample = sio.loadmat('zhuanliGauss.mat')
    # total = sample['total']
    x = (sample['rssi'] + 100.0) / 100.0
    y = (sample['loc'][:, -1] - 1).tolist()
    # for j in range(len(y)):
    #     y[j] = y[j][0]

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
    weights = tf.Variable(tf.truncated_normal([in_size, out_size], stddev=0.1))
    # 构建偏置 : 1 * out_size 的矩阵
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    # 矩阵相乘
    Wx_plus_b = tf.matmul(inputs, weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)

    return weights, biases, outputs  # 得到输出数据


input_size = 4    # 输入层结点数
hidden_layers = 7  # 隐藏层节点数
output_size = 9    # 输出层结点数
# 训练模型
x_data, y_data = build_data()

data_size = len(x_data)

xs = tf.placeholder(tf.float32, [data_size, input_size])
ys = tf.placeholder(tf.float32, [data_size, output_size])


# 构建输入层到隐藏层,假设隐藏层有 hidden_layers 个神经元
w1, b1, h1 = add_layer(xs, input_size, hidden_layers, activation_function=tf.nn.relu)
# 构建隐藏层到隐藏层
# h2 = add_layer(h1, hidden_layers, hidden_layers, activation_function=tf.nn.sigmoid)
# 构建隐藏层到隐藏层
# h3 = add_layer(h2, hidden_layers, hidden_layers, activation_function=tf.nn.sigmoid)
# 构建隐藏层到输出层
w2, b2, prediction = add_layer(h1, hidden_layers, output_size, activation_function=None)
prediction = tf.nn.softmax(prediction)

weights = [w1, w2]
biases = [b1, b2]

# 接下来构建损失函数: 计算输出层的预测值和真是值间的误差,对于两者差的平方求和,再取平均,得到损失函数.运用Adam算法,以0.1的效率最小化损失
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))

train_step = tf.train.AdadeltaOptimizer(0.2).minimize(loss)  # 优化算法选取SGD,随机梯度下降
correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(ys, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print('将计算图写入事件文件,在TensorBoard里查看')
# writer = tf.summary.FileWriter(logdir='logs/8_2_BP', graph=tf.get_default_graph())
# writer.close()


# 我们让TensorFlow训练10000次,每1000次输出训练的损失值:
loss_list, acc_list, pre_list = [], [], []
saver = tf.train.Saver()
# f = open('w.txt', 'w')
init = tf.global_variables_initializer()
train_num = 5000
with tf.Session() as sess:
    if isTrain:
        # 训练阶段
        sess.run(init)
        for i in range(train_num):
            sess.run(train_step, feed_dict={xs: x_data, ys: sess.run(y_data)})
            # sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
            if i % 100 == 0:
                loss_ = sess.run(loss, feed_dict={xs: x_data, ys: sess.run(y_data)})
                train_accuracy = accuracy.eval(feed_dict={xs: x_data, ys: sess.run(y_data)})
                print("step %d\naccuracy: %g, loss: %g" % (i, train_accuracy, loss_))
                loss_list.append(loss_)
                acc_list.append(train_accuracy)
        # 把最后一次训练的数据也保存下来
        loss_list.append(sess.run(loss, feed_dict={xs: x_data, ys: sess.run(y_data)}))
        acc_list.append(accuracy.eval(feed_dict={xs: x_data, ys: sess.run(y_data)}))
        pre = sess.run(prediction, feed_dict={xs: x_data, ys: sess.run(y_data)})

        pre_loc = some_fun(pre)
        error = []
        p = 0
        q = 0
        for i in range(9000):
            if i % 3000 == 0:
                p += 1
                q = 0
            if i % 1000 == 0:
                q += 1
            error.append(np.sqrt(np.sum(np.power(pre_loc[i, :] - np.array([p, q]), 2))))


        error_max = np.max(error)
        error_mean = np.mean(error)

        w1 = sess.run(weights[0])
        w2 = sess.run(weights[1])
        b1 = sess.run(biases[0])
        b2 = sess.run(biases[1])

        sio.savemat('w1nofilter', {'w1': w1})
        sio.savemat('w2nofilter', {'w2': w2})
        sio.savemat('b1nofilter', {'b1': b1})
        sio.savemat('b2nofilter', {'b2': b2})
        sio.savemat('prenofilter', {'pre': pre})
        sio.savemat('pre_locnofilter', {'pre_loc': pre_loc})



        # print(w1)

        # print(sess.run(prediction, feed_dict={xs: x_data}))
        # saver.save(sess, 'ckpt\\model.ckpt')

        i = np.arange(0, train_num + 100, 100)
        plt.plot(i, loss_list)
        plt.xlabel('train step')
        plt.ylabel('loss')
        plt.grid()
        plt.figure()
        plt.axis([0, train_num, 0, 1])
        plt.plot(i, acc_list)
        plt.xlabel('train step')
        plt.ylabel('accuracy')
        plt.ylim(0, 1)
        plt.plot(train_num, acc_list[-1], 'ro')
        plt.text(train_num, acc_list[-1] - 0.1, float('%0.2f' % acc_list[-1]))
        plt.grid()
        plt.show()

        plt.figure()
        for i in range(9):
            for j in range(20):
                plt.plot(pre_loc[i*1000+400 + j*10][0],pre_loc[i*1000+300 + j*10][1],'r+')
        cankao = []
        for i in range(3):
            temp = []
            for j in range(3):
                temp.append(i + 1)
                temp.append(j + 1)
                cankao.append(temp)
                temp = []
        cankao = np.array(cankao)
        plt.plot(cankao[:, 0], cankao[:, 1], 'go')
        plt.text(0.2, 3.7, str('mean error:%2.2fm' % error_mean))
        plt.text(0.2, 3.4, str('max  error:%2.2fm' % error_max))
        plt.axis([0,4,0,4])
        plt.show()

    else:
        saver.restore(sess, 'ckpt\\model.ckpt')
        pr = sess.run(prediction, feed_dict={xs: x_data})
        sio.savemat('pre_kalman.mat', {'pre_kalman': pr})

        print(pr)






