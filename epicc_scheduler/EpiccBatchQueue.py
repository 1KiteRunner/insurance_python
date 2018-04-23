# -*- coding:utf-8 -*-
__author__ = 'weikai'
import traceback
from datetime import datetime
import json

from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync.client import Stomp

import Scheduler.settings as se
from request_cic.login import *
from common.log import Logger
from Scheduler.Batch.threadUtil import threadpool
from request_epicc_vpn.standard_flow.standard_main import standard_main

log=Logger()
'''
监听车牌号队列
'''
ERROR_QUEUE = '/queue/testConsumerError'
CONFIG = StompConfig(se.i_config.MQHOST)
BATCH_EPICC_QUEUE=se.BATCH_EPICC_QUEUE
log=Logger()

def runrealtime():
    try:
        client = Stomp(CONFIG)
        client.connect()
        #client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL})
        client.subscribe(BATCH_EPICC_QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_AUTO})
        while True:
            try:
                frame = client.receiveFrame()
                body=json.loads(frame.body)
                log.info('Got %s' % json.dumps(body,ensure_ascii=False))
                epicc_batch(body,client)
            except Exception,e:
                log.error(e)
                log.error(frame.body)
                log.error(traceback.format_exc())

    except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())


def epicc_batch(body,client):
    for i in body:
        i['client']=client
    threadpool(standard_main,body)



if __name__=="__main__":
    from multiprocessing import Process
    #方法运行
    process = []
    log.info(u"程序开始运行%s" % datetime.now())

    for arg in xrange(1):
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



