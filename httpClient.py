import urllib

import urllib.request
HOSTIP = "192.168.199.140"
HOSTPORT= "80"

url="/?deviceID=Test1&temp=123&humi=456&CO2=4234.23"

 
full_url="http://"+ HOSTIP+ ":" + HOSTPORT + url
 
data=urllib.request.urlopen(full_url).read()
z_data=data.decode('UTF-8')
print(z_data)