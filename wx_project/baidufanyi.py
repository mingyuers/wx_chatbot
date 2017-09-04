# coding=utf8

import httplib
import md5
import urllib
import random
import json
from urllib import urlencode

def bd_translate(q,fromLang,toLang):
    # print 'from:',q
    appid = '20170727000068655'
    secretKey = 'zw1O5eE708BSmuUfgO8c'

    httpClient = None
    myurl = '/api/trans/vip/translate'
    # q = q
    # fromLang = 'zh'
    # toLang = 'en'
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
        # print 'to:',result
        return result
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

# print bd_translate("""上海非常热，呆在室内吹吹冷气，吃吃冷饮吧。27℃~36℃ 多云 东南风微风 天气炎热，建议着短衫、短裙、短裤、薄型T恤衫等清凉夏季服装。""",'zh','en')