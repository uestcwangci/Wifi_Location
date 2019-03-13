#!/usr/bin/env python
# encoding: utf-8
"""
@Author: WangCi
@Contact: 420197925@qq.com
@Software: PyCharm
@File : showRssi.py
@Time: 2019/3/11 16:03
@Desc:直接读取ui文件，ui文件名为"QtShowRssi.ui"
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import sys
import sqlite3 as sq
import numpy as np
# matplotlib.use("Qt5Agg")  # 声明使用QT5

path = os.getcwd()
qtCreatorFile = path + os.sep + "ui" + os.sep + "QtShowRssi.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# _translate = QtCore.QCoreApplication.translate
# _translate = QtCore.QCoreApplication.translate 这个主要用于后期的UI界面文字字体以及颜色便捷的更改
# 创建一个对象，该对象就是你的整个窗体：

ap_list = []
mac_list = []
id_list = []
x_list = []
y_list = []
data_dict = {}


class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):
    # 这里的第一个变量是你该窗口的类型，第二个是该窗口对象。
    # 这里是主窗口类型。所以设置成当QtWidgets.QMainWindow。
    # 你的窗口是一个会话框时你需要设置成:QtWidgets.QDialog
    def __init__ (self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.initFrame()

    def initFrame (self):
        self.layout = QVBoxLayout(self.frame)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # index = self.comboBox.currentIndex()
        self.pic = MyMplCanvas(self.frame, index=0, loc='0,0', width=80, height=4, dpi=100)
        self.layout.addWidget(self.pic)


    def show_instruction(self):
        self.textBrowser.show()
#         self.textBrowser.setText(
#             """可视化AP数据库使用说明：
# 1.选择指定数据库
# 2.选择要使用的功能
#             """)

    def open_ap_list (self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                     "请选择SQLite文件", path,
                                                                     "DataBase (*.db)")  # 设置文件扩展名过滤,用;间隔
        # 注意用双分号间隔
        if len(file_name) == 0:
            return
        file_name = file_name.replace('/', "\\")  # windows下需要进行文件分隔符转换
        connection = sq.connect(file_name)
        cursor = connection.cursor()
        select = cursor.execute('select Name, Mac from main.ap_table_id ')
        for row in select:
            ap_list.append(row[0])
            mac_list.append(row[1])
        if len(ap_list) > 0:
            QtWidgets.QMessageBox.information(self,  # 使用infomation信息框
                                              "说明", "加载成功", QtWidgets.QMessageBox.Ok)
        self.tableWidgetAp.setHorizontalHeaderLabels(['Name', 'Mac'])  # 设置表格表头数据
        self.tableWidgetAp.setColumnCount(4)  # 设置表格的列数
        self.tableWidgetAp.setRowCount(len(ap_list)/2 + 1)  # 设置表格的行数
        self.tableWidgetAp.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)  # 表格设置成大小随内容改变
        self.tableWidgetAp.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格设置成只读
        self.tableWidgetAp.setAlternatingRowColors(True)  # 隔行改变颜色
        self.tableWidgetAp.clear()  # 表格清空，不清空的话会永远残留
        for i in range(len(ap_list)):
            if i % 2 == 0:
                self.tableWidgetAp.setItem(i/2, 0, QTableWidgetItem(ap_list[i]))  # 设置表格内容为字符串"content"
                self.tableWidgetAp.setItem(i/2, 1, QTableWidgetItem(mac_list[i]))  # 设置表格内容为字符串"content"
            else:
                self.tableWidgetAp.setItem(i/2, 2, QTableWidgetItem(ap_list[i]))  # 设置表格内容为字符串"content"
                self.tableWidgetAp.setItem(i/2, 3, QTableWidgetItem(mac_list[i]))  # 设置表格内容为字符串"content"
            self.comboBox.insertItem(i, ap_list[i])
        self.textBrowser.hide()

    def open_database (self):
        if len(ap_list) < 1:
            QtWidgets.QMessageBox.information(self,  # 使用infomation信息框
                                              "ERROR", "未读取到AP表单", QtWidgets.QMessageBox.Ok)
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                     "请选择SQLite文件", path,
                                                                     "DataBase (*.db)")  # 设置文件扩展名过滤,用;间隔
        if len(file_name) == 0:
            return
        file_name = file_name.replace('/', "\\")  # windows下需要进行文件分隔符转换
        connection = sq.connect(file_name)
        cursor = connection.cursor()
        select = cursor.execute('select * from main.wifi_table ')
        lastX = -1
        lastY = -1
        for row in select:
            data_list = []
            x = row[1]
            y = row[2]
            key = '%d,%d' % (x, y)
            for i in range(3, 3 + len(ap_list)):
                data_list.append(row[i])
            if lastX == x and lastY == y:
                data_dict[key] += [data_list]
            elif key in data_dict.keys():
                data_dict[key] += [data_list]
            else:
                data_dict[key] = [data_list]
            lastX = x
            lastY = y

        if len(data_dict) > 0:
            QtWidgets.QMessageBox.information(self,  # 使用infomation信息框
                                              "说明", "加载成功", QtWidgets.QMessageBox.Ok)
        COL_PER_PAGE = 10
        self.tableWidgetLoc.setColumnCount(COL_PER_PAGE)  # 设置表格的列数
        self.tableWidgetLoc.setRowCount(int(len(data_dict)/COL_PER_PAGE)+1)  # 设置表格的行数
        self.tableWidgetLoc.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)  # 表格设置成大小随内容改变
        self.tableWidgetLoc.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格设置成只读
        self.tableWidgetLoc.setAlternatingRowColors(True)  # 隔行改变颜色
        self.tableWidgetLoc.clear()  # 表格清空，不清空的话会永远残留
        col = 0
        row = 0
        for key in data_dict.keys():
            loc_list = key.split(',')
            x = int(loc_list[0])
            y = int(loc_list[1])
            self.tableWidgetLoc.setItem(row, col, QTableWidgetItem("%d,%d" % (x, y)))  # 设置表格内容为字符串"content"
            col += 1
            if col / COL_PER_PAGE > 1:
                col %= COL_PER_PAGE
                row += 1

    def show_time (self):
        x = self.spinBoxX.text()
        y = self.spinBoxY.text()
        loc = '%s,%s' % (x, y)
        if loc == '0,0':
            pass
        elif x != 0 and y != 0 and loc in data_dict.keys():
            pass
        else:
            QtWidgets.QMessageBox.information(self,  # 使用infomation信息框
                                              "ERROR", "不存在的数据", QtWidgets.QMessageBox.Ok)
            return
        index = self.comboBox.currentIndex()
        newPic = UpdateMplCanvas(self.frame, index, loc, width=80, height=4, dpi=100)
        self.layout.replaceWidget(self.pic, newPic)
        self.pic = newPic


class MyMplCanvas(FigureCanvas):  # 创建一个matplot对象
    """这是一个窗口部件，即QWidget（当然也是FigureCanvasAgg）"""

    def __init__(self, parent=None, index=0, loc='0,0', width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(121)
        self.axes1 = fig.add_subplot(122)
        # 每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
        self.axes.grid('on')
        self.axes.set_title('Timing Diagram')
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("RSSI")

        self.axes1.grid('off')
        self.axes1.set_title('Probability Map')
        self.axes1.set_xlabel("RSSI")
        self.axes1.set_ylabel("Ratio")
        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.compute_initial_figure(index, loc)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self, index, loc):
        pass


class UpdateMplCanvas(MyMplCanvas):
    """静态画布：一条正弦线"""

    def compute_initial_figure(self, index, loc):
        # ap = np.array()
        if loc == '0,0':
            temp = []
            for value in data_dict.values():
                temp += value
            ap = np.array(temp)[:, 0]
        else:
            ap = np.array(data_dict[loc])[:, index]

        sort_tuple = np.unique(ap, return_counts=True)
        n = len(ap)
        self.axes.plot(range(n), ap)
        self.axes1.bar(sort_tuple[0], sort_tuple[1] / n, color='g')
        self.draw()





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainUi()  # 创建窗体对象
    window.show()  # 窗体显示
    sys.exit(app.exec_())
