## 使用说明

### 运行环境
```
Python3.x
```
### 功能
```
记录局域网内设备通过HTTP GET发过来的数据并解析保存成csv格式
如url="http://192.168.199.140:80/?deviceID=Test1&temp=123&humi=456&CO2=4234.23"
会解析成设备Test1传递来的temp，humi以及CO2数据
2019/01/06,20:23:12.574,Test1,temp,123,humi,456,CO2,4234.23
```

### 调用说明
```
python httpServer.py -p [port]
如：
python httpServer.py -p 8000
其中 端口号可选 不带端口号情况下默认端口是80
./log文件夹下会以CSV格式保存log
文件名为对应的设备名称
```