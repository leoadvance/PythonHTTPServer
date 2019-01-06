# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import time
# 时间
from datetime import datetime

# log目录名称
DIR_NAME = "./Log"

class buttonClass(QThread):

    # 启动和停止信号
    startSignal = pyqtSignal()
    stopSignal = pyqtSignal()

    # 声明写log和LCD显示信号
    writeLogSignal   = pyqtSignal(str)
    lcdDisplaySignal = pyqtSignal(str)


    def __init__(self, myWindow):
        QThread.__init__(self) 
        print("__init__", self)
        self.myWindow = myWindow
        self.Timer1s = QTimer() 
        self.Timer1s.setInterval(1000)
        self.Timer1s.timeout.connect(self.timeout)  # 定时超时事件绑定show_time这个函数          
         
        
    def __del__(self):
        print("__del__", self)

    def run(self):
        print('button Thread Start')
        while True:
            time.sleep(1)

        # self.HTTPServerThread = HTTPServerThread()
        # self.HTTPServerThread.
        # self.HTTPServerThread.start()         #定时器每一秒执行一次
    # 1s 时间戳
    def timeout(self):

        # 显示运行时间
        self.stopTimestamp = datetime.now()
        timestamp = self.stopTimestamp - self.startTimestamp
        # print("timestamp: ", timestamp, str(timestamp))
        self.lcdDisplaySignal.emit(str(timestamp)[:-7])
        pass

    def click(self):
        # print("click") 
        statusStr = self.myWindow.runButton.text()
        if (statusStr == "Start"):
            # 显示IP 启动时间记录
            
            self.myWindow.runButton.setText("Stop")
            print("启动服务器!")

            self.Timer1s.start()
            self.startTimestamp = datetime.now()
            self.lcdDisplaySignal.emit("0:00:00")

            # 每次启动时清空log区间
            self.myWindow.logTextBrowser.clear()
            self.writeLogSignal.emit("启动服务器!")
            self.startSignal.emit()

            
        else:
            # 清空显示
            self.myWindow.runButton.setText("Start")
            print("关闭服务器!")
            self.writeLogSignal.emit("关闭服务器!")
            self.stopSignal.emit()
            # 关闭定时器
            self.Timer1s.stop()
               
        pass    