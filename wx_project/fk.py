# coding:utf-8
import requests,random,hashlib,time
from urllib import urlencode

url = 'https://openapi.youdao.com/api'
appKey = '366f3e8f7e44521a'
secret = 'iETuhQClSV30QoRZqYMo5AhfgY8bCvYo'
q='你好'
# salt = ''
# for i in range(16):
#     salt+=random.choice(str)
# print time.time()
t = int(time.time())
salt = str(t)
print salt
m2 = hashlib.md5()
m2.update(appKey+q+salt+secret)
sign = m2.hexdigest()
print sign
data = {
    'q':q,
    'from':'zh-CHS',
    'to':'EN',
    'appKey':appKey,
    'salt':salt,
    'sign':sign
}
# data =data.encode('utf-8')
r = requests.get(url,data=urlencode(data))
print r.text
