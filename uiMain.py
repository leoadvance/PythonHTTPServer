# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
        self.lcdDisplaySlot("0:00:00")

        # 设置log文本框颜色 最大log行数
        self.logTextBrowser.setStyleSheet("color: rgb(118,214,255)")
        self.logTextBrowser.document().setMaximumBlockCount(100) 
        self.logRecevieSlot(
        '''
默认log以csv格式记录下在./log文件夹下，删除对应log文件后会自动重建。
点击"Start"后服务器正式启动。启停服务器不会删除之前保存的log。
        ''')
 

    # log接收槽
    def logRecevieSlot(self, str):
        self.logTextBrowser.append(str)

        # self.logTextBrowser.insertPlainText(str+'\n')
        # self.logTextBrowser.moveCursor(QTextCursor.Start)

        pass

       # LCD显示槽
    def lcdDisplaySlot(self, str):
        self.lcdRunningTime.display(str)
        pass 
    # IP显示
    def lineEditIPSlot(self, IP:str):
        self.lineEditIP.setText(IP)
        pass      
    # port显示
    def lineEditPortSlot(self, Port:str):
        self.lineEditPort.setText(Port)
        pass         