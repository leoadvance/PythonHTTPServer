# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

# 时间
from datetime import datetime

# log目录名称
DIR_NAME = "./Log"

class buttonClass():

    def __init__(self, myWindow):
        print("__init__", self)
        self.myWindow = myWindow
        self.Timer1s = QTimer() 
        self.Timer1s.timeout.connect(self.timeout)  # 定时超时事件绑定show_time这个函数          
         
        
    def __del__(self):
        print("__del__", self)


        # self.HTTPServerThread = HTTPServerThread()
        # self.HTTPServerThread.
        # self.HTTPServerThread.start()         #定时器每一秒执行一次
    # 1s 时间戳
    def timeout(self):

        # 显示运行时间
        self.stopTimestamp = datetime.now()
        timestamp = self.stopTimestamp - self.startTimestamp
        # print("timestamp: ", timestamp, str(timestamp))
        self.myWindow.lcdRunningTime.display(str(timestamp))
        pass

    def click(self):
        # print("click") 
        statusStr = self.myWindow.runButton.text()
        if (statusStr == "Start"):
            # 显示IP 启动时间记录
            
            self.myWindow.runButton.setText("Stop")
            print("启动服务器!")

            self.Timer1s.start(1000)
            self.startTimestamp = datetime.now()
            

            
        else:
            # 清空显示
            self.myWindow.runButton.setText("Start")
            print("关闭服务器!")

            # 关闭定时器
            self.Timer1s.stop()
        self.myWindow.lcdRunningTime.display("0:00:00.000000")       
        pass    