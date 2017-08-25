#coding:utf-8

import xiaoi.ibotcloud

def xiaoi_chatbot(question,userid='abc'):
    print question,userid
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
    print ret_ask.http_body
    return ret_ask.http_body


def chatbot_tuling(text):
    url = 'http://www.tuling123.com/openapi/api'
    key = '21e7880ff1434b87ba5acf38c0d4cc26'
    data = {
        'key': key,
        'info': text
    }
    r = requests.post(url, data=data)
    res = json.loads(r.text)
    return res['result']