# coding=utf-8

# 图形界面
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui import *
from logFile import *
from buttonHandler import *
from uiMain import *
# 允许带执行参数
import getopt
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse
import urllib
import sys 
import socket
import numpy as np
# 时间
from datetime import datetime

import threading

# 默认IP和端口号
hostIP = "192.168.1.1"
hostPort = 80

DIR_NAME = "./Log"



# 参数使用说明
def usage():
    print("-p   Server Port number Default value is 80")


# 获取系统参数并解析
def getSysPara():
    argv = sys.argv[1:]
    # print("argv:", argv)
    try:
        # 获取参数 带:表明必须带参数 如p: -p xx
        Para, args = getopt.getopt(argv, "hp:", ["help"])
        # print('Para   :', Para)
        for o, arg in Para:
            if o in ("-h", "--help"):
                # 打印使用说明
                usage()
                sys.exit(0)
            # 提取端口号
            if o in ("-p"):
                
                # 声明host是全局变量
                global hostPort 
                hostPort = int(arg)
                # 防止越界
                if hostPort < 0 or hostPort > 65536:
                    print(" ERROR ! The port number must be between 0 and 65535!")
                    sys.exit(1)
                # else: 
                    # print("arg:", hostPort)

    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(1)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

class httpHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        print("_set_response: ")
        self.send_response(200)
        self.send_header('Content-type'.encode(), 'text/html'.encode())
        self.end_headers()

    def do_GET(self):
        # print("do_GET: ",self.path)
        
        # print("Path: : " + str(self.path))
        # print("Headers: " + str(self.headers))

        # 提取有效数据并转化成np array
        b = urllib.parse.parse_qsl(urlparse(self.path).query)
        values = np.array(b)
        # print(b)
        # print("array.size:", values.size, " array.shape:", values.shape)

        # 遍历数组 并且把二维转成1维
        listValues = []
        [rows, cols] = values.shape
        # print(rows, cols)
        for i in range(rows):
            for j in range(cols):
                # print(a)
                listValues.append(str(values[i][j]))
   
        # start = datetime.now()
        # 声明log 实例
        logClass = LOGClass(str(listValues[1]))
        # 插入时间数据 年月日 时分秒
        log_date = datetime.now().strftime("%Y/%m/%d")
        log_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        wrtiteData = log_date + "," + log_time + "," + ','.join(listValues[1:]) + "\n"
        # print(wrtiteData)
        # log_file.writelines(wrtiteData)   
        # log_file.flush()
        # log_file.close() 
        logClass.log_file_write(wrtiteData)

        self._set_response()
        self.wfile.write("<html><body><h1>HTTP GET Success!</h1></body></html>".encode())
        
        # 显示log 并省略最后换行符号
        global myWin
        myWin.HTTPServerThread.logSignal.emit(wrtiteData[:-1])   
        # end = datetime.now()
        # diff = end - start
        # print("写入文件耗时:", diff)

    def do_HEAD(self):
        print("do_HEAD: ")
        self._set_response()
        
    def do_POST(self):

        # 获取内容长度并读取
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        
        print("POST request: " )
        print("Path: : " + str(self.path))
        print("Headers: " + str(self.headers))
        print("Body: " + post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        # print("urlparse: ")
        # o = urlparse(post_data).query
        # print(o)
        
def run(self, port = 80):

    server_address = ("", port)
    httpd = HTTPServer(server_address, httpHandler)
    self.logSignal.emit("testSignal run")
    httpd.serve_forever() 
    # app.exec_()
# 服务器线程
def threadServer(self):
    # 获取系统参数
    getSysPara()
    # 获取本机IP
    hostIP = get_host_ip()
    print("hostIP: " + hostIP + " port: {:d}".format(hostPort))
    print ('Starting http server...')  
    self.logSignal.emit("testSignal threadServer")

    # 显示IP和端口号
    # global myWin
    # myWin.lineEditIP.setText(hostIP)
    # myWin.lineEditPort.setText(str(hostPort))

    run(self, hostPort)


class HTTPServerThread(QThread):

    # 创建finish信号量 参数字符串
    finished_signal = pyqtSignal(str)

    # log信号
    logSignal = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        # self._rest = rest

    def run(self):
        print('Qt HTTP server Thread Start')
        threadServer(self)
        self.finished_signal.emit('done')



if __name__ == "__main__":

    app = QApplication(sys.argv)
    global myWin
    myWin = MyWindow()
    buttonHandle = buttonClass(myWin)
    myWin.HTTPServerThread = HTTPServerThread()
    myWin.HTTPServerThread.logSignal.connect(myWin.logRecevieSlot)
    myWin.HTTPServerThread.start()  
    myWin.runButton.clicked.connect(buttonHandle.click)
    myWin.show()
    sys.exit(app.exec_())

