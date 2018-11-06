# -*- coding: utf-8 -*-
import scipy.io as sio
import shutil
import os


def clean_dir(path):
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


cur_path = os.getcwd()
mat_path = os.path.abspath('..\\mat_data\\ForNewForm')
clean_dir(mat_path)
if os.path.exists('x_ave.mat'):
    shutil.move(cur_path + '\\x_ave.mat', mat_path)
if os.path.exists('y_mean.mat'):
    shutil.move(cur_path + '\\y_mean.mat', mat_path)
if os.path.exists('10m.mat'):
    shutil.move(cur_path + '\\10m.mat', mat_path)

print('Move Successfully')
print('########## 5 ##########')
