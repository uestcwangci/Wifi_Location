# -*- coding: utf-8 -*-

import scipy.io as sio
import shutil
import os
import GlobalVarible.setter
import GlobalVarible.getter as glovar

MAX_AP = glovar.MAX_AP
MIN_AP = glovar.MIN_AP


def selectAP(data_set, data_name):
    for rAP in reversed(range(MIN_AP, MAX_AP + 1)):
        sio.savemat(data_name + '_AP' + str(rAP) + '.mat',
                    {data_name + '_AP' + str(rAP): data_set})

        for iData in data_set:
            del iData[-7:]
        print('Save ' + data_name + ' successfully | AP:%2i |' % rAP)


def clean_dir (path):
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则删除目录及其文件，重新创立一个新文件夹
        shutil.rmtree(path)
        # 创建目录操作函数
        os.makedirs(path)
        return False


for i in range(2):
    if i == 0:
        DataName = 'x_train'
        x_train = sio.loadmat(DataName + '.mat')[DataName].tolist()
        selectAP(x_train, DataName)
    elif i == 1:
        DataName = 'x_test'
        x_train = sio.loadmat(DataName + '.mat')[DataName].tolist()
        selectAP(x_train, DataName)

cur_path = os.getcwd()
mat_path = os.path.abspath('..\\mat_data')
clean_dir(mat_path)
for iAP in range(MIN_AP, MAX_AP + 1):
    shutil.move(cur_path + '\\x_train_AP' + str(iAP) + '.mat', mat_path)
    shutil.move(cur_path + '\\x_test_AP' + str(iAP) + '.mat', mat_path)
shutil.move(cur_path + '\\y_train.mat', mat_path)
shutil.move(cur_path + '\\y_test.mat', mat_path)
print('Move Successfully')
print('########## 5 ##########')
