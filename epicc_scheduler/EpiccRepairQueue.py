# -*- coding:utf-8 -*-
__author__ = 'weikai'
import traceback
from datetime import datetime
import json

from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync.client import Stomp

from Scheduler import  settings as se
from request_cic.login import *
from common.log import Logger
from  Scheduler.Batch.threadUtil import threadpool
from request_epicc_vpn.getDataNew import check

log=Logger()
'''
监听车牌号队列
'''
ERROR_QUEUE = '/queue/testConsumerError'
CONFIG = StompConfig(se.i_config.MQHOST)
EPICC_BATCH_REPAIR_QUEUE=se.EPICC_BATCH_REPAIR_QUEUE
log=Logger()

def runrealtime():
    try:
        client = Stomp(CONFIG)
        client.connect()
        #client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL})
        client.subscribe(EPICC_BATCH_REPAIR_QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_AUTO})
        while True:
            try:
                frame = client.receiveFrame()
                body=json.loads(frame.body.decode())
                #body=json.loads(frame.body.decode())
                #log.info('Got %s' % json.dumps(body,ensure_ascii=False))
                epicc_repair(body)
            except Exception,e:
                log.error(e)
                log.error(frame.body)
                log.error(traceback.format_exc())

    except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())


def epicc_repair(body):
    alist=[]
    for i in body:
       alist.append(i['plateNumber'])
    #plateNumber=onedata['plateNumber']
    threadpool(check,alist)


if __name__=="__main__":
    from multiprocessing import Process
    #方法运行
    process = []
    log.info(u"程序开始运行%s" % datetime.now())

    for arg in xrange(2):
        th = Process(target=runrealtime)
        th.start()
        process.append(th)
    try:
        for th in process:
            th.join()
    except Exception,e:
        log.error(e)
        log.error(traceback.format_exc())
    log.info(u"程序结束运行%s" % datetime.now())



