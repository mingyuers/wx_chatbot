# coding=utf8

import httplib
import md5
import urllib
import random
import json
from urllib import urlencode

def fanyi(q):
    print 'fanyi:',q
    appid = '20170727000068655'
    secretKey = 'zw1O5eE708BSmuUfgO8c'

    httpClient = None
    myurl = '/api/trans/vip/translate'
    # q = q
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        # print response.read()
        j = json.loads(response.read())
        result = j['trans_result'][0]['dst']
        print 'result:',result
        return result
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

# print fanyi('早上好啊，吃过了吗？')