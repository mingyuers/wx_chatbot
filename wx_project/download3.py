# coding:utf-8
import requests
import threading
import os,sys
import time


class downloader:
    def __init__(self,url,num=10):
        self.url = url
        self.num = num
        self.name = "3.zip"
        r = requests.head(self.url)
        # 获取文件大小
        self.total = int(r.headers['Content-Length'])
        if self.total / 1024 <= 0:
            print '下载资源大小为：%s B ' % self.total
        elif self.total / 1024 / 1024 <= 0:
            print '下载资源大小为：%s KB ' % (self.total / 1024)
        else:
            print '下载资源大小为：%s MB ' % (self.total / 1024 / 1024)

    # 获取每个线程下载的区间
    def get_range(self):
        ranges = []
        offset = int(self.total / self.num)
        for i in range(self.num):
            if i == self.num - 1:
                ranges.append((i * offset, ''))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        return ranges  # [(0,100),(100,200),(200,"")]

    # 通过传入开始和结束位置来下载文件
    def download(self, start, end):
        headers = {'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'}
        res = requests.get(self.url, headers=headers)
        # per = os.path.getsize(self.name) * 100.00 / self.total
        # sys.stdout.write('\r下载进度：[%s%s] %.2f%%' % ('>' * int(per / 2), ' ' * int(50 - per / 2), per))
        # sys.stdout.flush()
        # print "%s-%s download success" % (start, end)
        # print "start%s end%s totle%s" %(start,end,self.total)
        # print "down--%f" %(per)
        # 将文件指针移动到传入区间开始的位置
        self.fd.seek(start)
        self.fd.write(res.content)

    def run(self):
        self.fd = open(self.name, "wb")

        thread_list = []
        n = 0

        for ran in self.get_range():
            # 获取每个线程下载的数据块
            start, end = ran
            n += 1
            thread = threading.Thread(target=self.download, args=(start, end))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            # 设置等待，避免上一个数据块还没写入，下一数据块对文件seek，会报错
            i.join()

        while True:
            # print os.path.getsize ( self.name ), ' ', self.total
            per = os.path.getsize(self.name) * 100.00 / self.total
            sys.stdout.write('\r下载进度：[%s%s] %.2f%%' % ('>' * int(per / 2), ' ' * int(50 - per / 2), per))
            sys.stdout.flush()
            # print '\r下载进度：%.2f%%' % per
            time.sleep(1)
            if per >= 100:
                print '\n下载完成'
                break

        self.fd.close()


if __name__ == "__main__":
    url = 'https://bbuseruploads.s3.amazonaws.com/fd96ed93-2b32-46a7-9d2b-ecbc0988516a/downloads/98d51451-997f-40e3-b9e6-a8e635dcdcb3/phantomjs-2.1.1-windows.zip?Signature=1IUCvjMiNA%2FBLomMkSTzWf5B4zw%3D&Expires=1501560386&AWSAccessKeyId=AKIAIQWXW6WLXMB5QZAQ&versionId=null&response-content-disposition=attachment%3B%20filename%3D%22phantomjs-2.1.1-windows.zip%22'
    d = downloader(url)
    d.run()
