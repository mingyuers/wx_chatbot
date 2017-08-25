# coding: utf-8
# author: wangaq
# 2016/6/15 16:27:52

import requests
import threading
import os
import time
import argparse
import sys


class download(object):
    def __init__(self, uri, num=5):
        self.uri = uri
        self.num = num
        self.name = self.uri.split('/')[-1]
        self.total = self.get_uri_length()
        self.lock = threading.RLock()

    def get_uri_length(self):
        # head方法取得资源大小
        rsp = requests.head(self.uri)

        length = int(rsp.headers['Content-Length'])
        if length / 1024 <= 0:
            print '下载资源大小为：%s B ' % length
        elif length / 1024 / 1024 <= 0:
            print '下载资源大小为：%s KB ' % (length / 1024)
        else:
            print '下载资源大小为：%s MB ' % (length / 1024 / 1024)

        return length

    def get_range(self):
        ranges = []
        # 计算每个线程获取资源的偏移量
        offset = int(self.total / self.num)

        for i in range(0, self.num):
            if i == self.num - 1:
                ranges.append((i * offset, ''))
            else:
                ranges.append((i * offset, (i + 1) * offset - 1))

        # print ranges, ' ', self.total
        return ranges

    def down(self, no, start, end):

        headers = {'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'}
        rsp = requests.get(self.uri, headers=headers, stream=True)

        # print ' %s:%s download success ' % ( start, end )

        # 复制一个文件描述符用来写文件，避免多个线程使用一个文件描述符出错
        fd = os.dup(self.fd)

        # 将写位置移动到适当位置
        # os.lseek ( fd, start, os.SEEK_SET )

        ilen = 0
        for data in rsp.iter_content(512 * 1024):
            # print '[' + str ( no ) + ':' + str ( start + ilen ) + ':' + data + ']'
            self.lock.acquire()
            # 将写位置移动到适当位置
            os.lseek(fd, start + ilen, os.SEEK_SET)
            # 写文件并记录位置
            os.write(fd, data)
            self.lock.release()
            ilen += len(data)
        # os.fsync ( fd ) #不能加刷新缓冲区，会导致错位，及多余的空格

        os.close(fd)

    # print 'thread ' + str ( no ) + ' is end. write ' + str ( ilen ) + ' byetes. '


    def run(self):
        # 创建本地要保存的文件，windows下务必使用二进制方式创建文件
        self.fd = os.open(self.name, os.O_RDWR | os.O_CREAT | os.O_BINARY | os.O_TRUNC)

        thread_list = []

        n = 0
        for ran in self.get_range():
            start, end = ran
            # 创建线程
            th = threading.Thread(target=self.down, args=(n, start, end))
            # print 'thread %s start' % n
            n += 1
            # 启动线程
            th.start()
            thread_list.append(th)

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

        for th in thread_list:
            th.join()

        # 关闭文件描述符
        os.close(self.fd)


if __name__ == '__main__':
    # # 创建一个参数解析器
    # parser = argparse.ArgumentParser(description='download uri with multiple thread which you specify')
    # # 增加线程数量参数
    # parser.add_argument('-thread', '--thread_num', type=int, help='specify the number of thread')
    # # 增加定位参数，指定要下载的资源
    # parser.add_argument('uri', help='what you want to download')
    # args = parser.parse_args()
    # uri = args.uri
    # print uri
    uri = 'http://201606mp4.11bubu.com/20161111/shkd-718/1/xml/91_473c45683cbb407bf9cce9b6f0160ad5.mp4'
    num = 15
    # if args.thread_num:
    #     num = args.thread_num
    downloader = download(uri, num)
    downloader.run()