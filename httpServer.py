# coding=utf-8
# 允许带执行参数
import getopt
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse
import sys 
import socket

# 默认IP和端口号
hostIP = "192.168.1.1"
hostPort = 80


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
                else: 
                    print("arg:", hostPort)

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
        print("do_GET: ")
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
        o = urlparse(post_data)
        print(o)
        
def run(port = 80):
    server_address = ("", port)
    httpd = HTTPServer(server_address, httpHandler)
    
    httpd.serve_forever()

if __name__ == "__main__":

    # 获取系统参数
    getSysPara()
    # 获取本机IP
    hostIP = get_host_ip()
    print("hostIP: " + hostIP + " port: {:d}".format(hostPort))
    print ('Starting http server...')  

    run(hostPort)