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
import time
# 时间
from datetime import datetime
from socketserver import ThreadingMixIn

# 默认端口号
hostPort = 80

class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

class httpHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        # print("_set_response: ")
        self.send_response(200)
        self.send_header('Content-type'.encode(), 'text/html'.encode())
        self.end_headers()

    def do_GET(self):
        # print("do_GET: ",self.path)
        # print ("self:" ,self)
        # 过滤数据，必须以/?起始
        strPATH = str(self.path)
        if (strPATH[1] != "?"):
            return
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

        logClass.log_file_write(wrtiteData)

        self._set_response()
        self.wfile.write("<html><body><h1>HTTP GET Success!</h1></body></html>".encode())
        
        # 显示log 并省略最后换行符号
        global httpServer
        httpServer.logSignal.emit(wrtiteData[:-1])   
        # time.sleep(10)
        # print("do_GET: end")
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

class HTTPServerClass(QThread):

    # log信号
    logSignal      = pyqtSignal(str)
    hostIPSignal   = pyqtSignal(str)
    hostPortSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.getSysPara()
        self.Port = hostPort

        # self._rest = rest
    def __del__(self):
        print("__del__", self)

    def run(self):
        self.hostIP = self.get_host_ip()
        print("hostIP: " + self.hostIP + " port: {:d}".format(self.Port))
        print ('Starting http server...') 



        server_address = ("", self.Port)
        #self.httpd = HTTPServer(server_address, httpHandler)
        self.httpd = ThreadingHttpServer(server_address, httpHandler)

        self.hostIPSignal.emit(self.hostIP)
        self.hostPortSignal.emit(str(self.Port))
        
        # self.logSignal.emit("testSignal run")
        self.httpd.serve_forever() 
    

    def startServer(self):
        print("startServer!")
        self.start()  
 

    # 停止服务器    
    def stopServer(self):
        # self.logSignal.emit("testSignal run")
        print("stopServer!")
        self.httpd.server_close()
        self.terminate() 
        self.hostIPSignal.emit("")
        self.hostPortSignal.emit("")

    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


    # 参数使用说明
    def usage(self):
        print("-p   Server Port number Default value is 80")

    # 获取系统参数并解析
    def getSysPara(self):
        argv = sys.argv[1:]
        # print("argv:", argv)
        try:
            # 获取参数 带:表明必须带参数 如p: -p xx
            Para, args = getopt.getopt(argv, "hp:", ["help"])
            # print('Para   :', Para)
            for o, arg in Para:
                if o in ("-h", "--help"):
                    # 打印使用说明
                    self.usage()
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

if __name__ == "__main__":

    app = QApplication(sys.argv)
    myWin = MyWindow()
    buttonHandle = buttonClass(myWin)
    buttonHandle.start()
    global httpServer
    httpServer = HTTPServerClass()
    
    
    
    # 绑定信号和槽
    httpServer.logSignal.connect(myWin.logRecevieSlot)
    httpServer.hostIPSignal.connect(myWin.lineEditIPSlot)
    httpServer.hostPortSignal.connect(myWin.lineEditPortSlot)
    myWin.runButton.clicked.connect(buttonHandle.click)
    buttonHandle.writeLogSignal.connect(myWin.logRecevieSlot)
    buttonHandle.lcdDisplaySignal.connect(myWin.lcdDisplaySlot)
    buttonHandle.startSignal.connect(httpServer.startServer)
    buttonHandle.stopSignal.connect(httpServer.stopServer)
    myWin.show()
    sys.exit(app.exec_())

