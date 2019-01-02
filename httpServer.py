#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse
from sys import argv
import socket

# 默认IP和端口号
hostIP = "192.168.1.1"
hostPort = 80

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


    if len(argv) == 2:
        hostPort = int(argv[1])
    # 获取本机IP
    hostIP = get_host_ip()
    print("hostIP: " + hostIP + " port: {:d}".format(hostPort))
    print ('Starting http server...')  

    run(hostPort)