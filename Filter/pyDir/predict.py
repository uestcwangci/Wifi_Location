#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : predict.py 
@Time: 2018/11/12 16:33
@Desc: 使用训练好的网络对在线数据进行预测
"""
import tensorflow as tf
import scipy.io as sio
import os
import sys

tf.reset_default_graph()

print('**************')
with tf.Session() as sess:
    saver = tf.train.Saver()
    print('----------------')
    sess.run(tf.global_variables_initializer())
    model_file = tf.train.latest_checkpoint('ckpt/')
    saver.restore(sess, model_file)
    a=1

#
# def build_data():
#     sample = sio.loadmat('afterGauss_2.mat')
#     x = (sample['rssi'] + 100.0) / 100.0
#     y = (sample['loc'] - 1).tolist()
#     for j in range(len(y)):
#         y[j] = y[j][0]
#
#     # 把labels化为one_hot类型
#     max_batch = max(y) + 1
#     y = tf.one_hot(y, max_batch)
#
#     return x, y





