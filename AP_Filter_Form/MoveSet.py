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
mat_path = os.path.abspath('..\\mat_data\\ForForm')
clean_dir(mat_path)
shutil.move(cur_path + '\\x_train_rForm.mat', mat_path)
shutil.move(cur_path + '\\x_test_rForm.mat', mat_path)
shutil.move(cur_path + '\\y_train_rForm.mat', mat_path)
shutil.move(cur_path + '\\y_test_rForm.mat', mat_path)
print('Move Successfully')
print('########## 5 ##########')
