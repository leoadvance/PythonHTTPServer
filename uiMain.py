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
        
        # 1s测试定时器
        self.testTimer = QTimer() 
        self.testTimer.timeout.connect(self.show_time)  # 定时超时事件绑定show_time这个函数          
        self.testTimer.start(1000) 

        # 设定运行时间显示长度和显示模式
        self.lcdRunningTime.setDigitCount(24)
        self.lcdRunningTime.setMode(QLCDNumber.Dec)
        self.lcdRunningTime.setSegmentStyle(QLCDNumber.Flat)#Mac系统需要加上，否则下面的color不生效。
        self.lcdRunningTime.setStyleSheet("color: green")
        self.lcdRunningTime.display("0:00:00")
 
        
        # self.HTTPServerThread = HTTPServerThread()
        # self.HTTPServerThread.
        # self.HTTPServerThread.start()         #定时器每一秒执行一次

    def show_time(self):
        # self.time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print("time_now:", self.time_now)
        pass

    # 测试槽
    def testSlot(self, str):
        # print("testSlot: ", str)
        pass