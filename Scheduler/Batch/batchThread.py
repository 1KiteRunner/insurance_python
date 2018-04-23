# -*- coding:utf-8 -*-
__author__ = 'weikai'
import datetime
import thread,threading
import traceback

def batchthreadpool(method,args,session):
    try:
        if len(args) <=10:
            #线程池
            threads = []
            print u"程序开始运行%s" % datetime.datetime.now()
            for arg in args:
                th = threading.Thread(target=method, args=(session,arg))
                th.start()
                threads.append(th)
            for th in threads:
                th.join()
            print u"程序结束运行%s" % datetime.datetime.now()
        elif len(args)>10:
            rang = (len(args)+10-1)/10
            for i in range(0,rang):
                if i < rang-1:
                    threads = []
                    print u"程序开始运行%s" % datetime.datetime.now()
                    for arg in args[(i*10):(10*i+10)]:
                        th = threading.Thread(target=method, args=(session,arg))
                        th.start()
                        threads.append(th)
                    for th in threads:
                        th.join()
                    print u"程序结束运行%s" % datetime.datetime.now()
                else:
                        # 线程池
                    threads = []
                    print u"程序开始运行%s" % datetime.datetime.now()
                    for arg in args[(i*10):len(args)]:
                        th = threading.Thread(target=method, args=(session,arg))
                        th.start()
                        threads.append(th)
                    for th in threads:
                        th.join()
                    print u"程序结束运行%s" % datetime.datetime.now()
    except Exception,e:
        print(e)
        print(traceback.format_exc())