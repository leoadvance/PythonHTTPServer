# coding=utf-8

# 图形界面
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui import *
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

# 创建or打开log文件 
def log_file_open(fileName):

    # print("fileName:", fileName)
    # 判断目录是否存在
    if os.path.isdir(DIR_NAME) == False:
        os.mkdir(DIR_NAME)
        print("目录不存在，创建目录:" + DIR_NAME)

    #print(time_str)
    # 追加的方式打开文件
    return(open(DIR_NAME + "/" + fileName+ ".csv", "a"))

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
        # 插入时间数据 年月日 时分秒
        log_date = datetime.now().strftime("%Y/%m/%d")
        log_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        listValues.insert(2, log_date) 
        listValues.insert(3, log_time) 
        # print(listValues)
        # start = datetime.now()
        log_file = log_file_open(listValues[1])
        wrtiteData = ','.join(listValues[2:]) + "\n"
        # print(wrtiteData)
        log_file.writelines(wrtiteData)   
        log_file.flush()
        log_file.close()      
        # end = datetime.now()

        # diff = end - start
        # print("写入文件耗时:", diff)
        self._set_response()
        self.wfile.write("<html><body><h1>HTTP GET Success!</h1></body></html>".encode())

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
        print("urlparse: ")
        o = urlparse(post_data).query
        print(o)
        
def run(port = 80):

    server_address = ("", port)
    httpd = HTTPServer(server_address, httpHandler)
    
    httpd.serve_forever()

def threadUI():
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
    # app.exec_()
# 服务器线程
def threadServer():
    # 获取系统参数
    getSysPara()
    # 获取本机IP
    hostIP = get_host_ip()
    print("hostIP: " + hostIP + " port: {:d}".format(hostPort))
    print ('Starting http server...')  

    run(hostPort)


class HTTPServerThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self._rest = rest

    def run(self):
        print('Qt HTTP server Thread Start')
        threadServer()
        self.finished_signal.emit('done')


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)  # 创建主界面对象
        Ui_MainWindow.__init__(self)#主界面对象初始化
        self.setupUi(self)  #配置主界面对象
        
        # 1s测试定时器
        self.testTimer = QTimer() 
        self.testTimer.timeout.connect(self.show_time)  # 定时超时事件绑定show_time这个函数          
        self.testTimer.start(1000) 
        
        self.HTTPServerThread = HTTPServerThread()
        self.HTTPServerThread.start()         #定时器每一秒执行一次

    def show_time(self):
        self.time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("time_now:", self.time_now)

if __name__ == "__main__":
      #创建一个线程ta，执行 threadfun()
    # tb = threading.Thread(target=threadServer)    #创建一个线程tb，执行threadfun()        #调用start()，运行线程
    # # 子线程随主线程退出而退出
    # tb.daemon = True
    # tb.start()  
    threadUI()

