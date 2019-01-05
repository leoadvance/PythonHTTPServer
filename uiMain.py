# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
from ui import *

# 时间
from datetime import datetime


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)  # 创建主界面对象
        Ui_MainWindow.__init__(self)#主界面对象初始化
        self.setupUi(self)  #配置主界面对象
        


        # 设定运行时间显示长度和显示模式
        self.lcdRunningTime.setDigitCount(24)
        self.lcdRunningTime.setMode(QLCDNumber.Dec)
        self.lcdRunningTime.setSegmentStyle(QLCDNumber.Flat)#Mac系统需要加上，否则下面的color不生效。
        self.lcdRunningTime.setStyleSheet("color: green")
        self.lcdRunningTime.display("0:00:00")

        # 设置log文本框颜色 最大log行数
        self.logTextBrowser.setStyleSheet("color: rgb(118,214,255)")
        self.logTextBrowser.document().setMaximumBlockCount(100) 

    # log接收槽
    def logRecevieSlot(self, str):
        # print("testSlot: ", str)
        self.logTextBrowser.append(str)
        pass