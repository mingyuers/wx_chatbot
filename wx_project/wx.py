# coding:utf-8
from wxpy import Bot, Message
from wxpy import *
import xiaoi.ibotcloud
import requests, json, time, random, hashlib
import sys
from baidufanyi import fanyi

# from utils import xiaoi_chatbot

# group_name = unicode(sys.argv[1],'gb2312')
# print group_name


group_name = u'哈哈'


def main():
    print 'main'
    bot = Bot(cache_path=True)
    bot.enable_puid('wxpy_puid.pkl')
    # 在 Web 微信中把自己加为好友
    # bot.self.add()
    # bot.self.accept()
    mygroup = bot.groups().search(group_name)[0]
    myfriend = bot.friends().search(u'明月')[0]

    @bot.register(mygroup)
    def print_group(msg):
        # msg.forward(myfriend)
        if msg.type == TEXT:
            # return u'啊'
            print msg.text
            result = fanyi(msg.text)
            print result
            return unicode(result,'gb2312')

    embed()


# xiaoi_chatbot('你好','30c8b457')

# v5kf_chatbot('hello')


def xiaoi_chatbot(question, userid='abc'):
    print question, userid
    # please input your key/sec
    test_key = "NhEe6NJ2mX7a"
    test_sec = "Qpvtxsu1BriOymw7Mq9g"
    signature_ask = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                                  app_sec=test_sec,
                                                  uri="/ask.do",
                                                  http_method="POST")
    params_ask = xiaoi.ibotcloud.AskParams(platform="custom",
                                           user_id=userid,
                                           url="http://nlp.xiaoi.com/ask.do",
                                           response_format="xml")
    ask_session = xiaoi.ibotcloud.AskSession(signature_ask, params_ask)
    ret_ask = ask_session.get_answer(question)
    result = ret_ask.http_body
    print result
    return result.encode('utf-8')


main()