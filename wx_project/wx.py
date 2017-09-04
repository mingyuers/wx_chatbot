# coding:utf-8
from wxpy import Bot, Message
from wxpy import *
import xiaoi.ibotcloud
import requests, json, time, random, hashlib
import MySQLdb
from baidufanyi import bd_translate
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# from utils import xiaoi_chatbot

# group_name = unicode(sys.argv[1],'gb2312')
# print group_name


group_name = u'哈哈'
db = MySQLdb.connect(host='localhost', user='root', passwd='199358fgm', db='wxchatbot', charset='utf8')


def main():
    bot = Bot(cache_path=True,console_qr=2)
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
            # print msg
            username = msg.member.name
            en_from = msg.text.encode('utf-8')
            print '收到消息:', en_from
            if not isCN(en_from):
                cn_from = bd_translate(en_from, 'en', 'zh')
                cn_chatbot = xiaoi_chatbot(cn_from, username)
                cn_chatbot = cn_chatbot.replace('\n', ' ')
                en_chatbot = bd_translate(cn_chatbot, 'zh', 'en')
                # print '翻译结果:', en_chatbot
                save_record(username, en_from, cn_from, cn_chatbot, en_chatbot)
                return en_chatbot + '\n' + '(翻译:' + cn_chatbot + ')'

    bot.join()


def save_record(username, en_from, cn_from, cn_chatbot, en_chatbot):
    cursor = db.cursor()
    sql = 'insert into wx_history (groupname,username,en_from,cn_from,cn_chatbot,en_chatbot,chattime) values (%s,%s,%s,%s,%s,%s,now())'
    values = (group_name, username, en_from, cn_from, cn_chatbot, en_chatbot)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()


def xiaoi_chatbot(question, username='abc'):
    m2 = hashlib.md5()
    m2.update(username)
    userid = m2.hexdigest()
    # print question, userid
    # print '编码:', chardet.detect(question)
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
    result = result.encode('utf-8')
    # print 'chatbot结果：',result
    return result


def isCN(str):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    str = unicode(str, 'utf-8')
    match = zhPattern.search(str)
    if match:
        return True
    else:
        return False


main()
