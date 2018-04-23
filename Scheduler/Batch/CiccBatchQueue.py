# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
import traceback
from datetime import datetime
from multiprocessing import Process

from stompest.async import Stomp
from stompest.async.listener import SubscriptionListener
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from twisted.internet import defer, reactor, threads

from Scheduler import settings as se
from Scheduler.session import getSession
from common.log import Logger
from request_cicc.cicc_standard_flow.flow_main import flow_main

'''
监听车牌号队列
'''
ERROR_QUEUE = '/queue/testConsumerError'
CONFIG = StompConfig(se.i_config.MQHOST)
BATCH_CICC_QUEUE = se.BATCH_CICC_QUEUE
log = Logger()


class Consumer(object):
    @defer.inlineCallbacks
    def runrealtime(self):
        try:
            client = Stomp(CONFIG)
            yield client.connect()
            headers = {
                StompSpec.ACK_HEADER: StompSpec.ACK_AUTO,
                'activemq.prefetchSize': '100',
            }
            client.subscribe(BATCH_CICC_QUEUE, headers,
                             listener=SubscriptionListener(self.consume))
        except Exception, e:
            log.error(e)
            log.error(traceback.format_exc())

    def consume(self, client, frame):
        try:
            sessiondt = getSession()
            session = sessiondt['5']
            body = json.loads(frame.body.decode())
            log.info(u'收到队列消息 开始执行')
            for data in body:
                data['client'] = client
                threads.deferToThread(flow_main, session, data)
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())


def main():
    try:
        reactor.suggestThreadPoolSize(5)  # 设置线程池的最大数量
        Consumer().runrealtime()

        reactor.run()
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


if __name__ == "__main__":

    # 方法运行
    process = []
    log.info(u"程序开始运行%s" % datetime.now())

    for arg in xrange(1):
        th = Process(target=main)
        th.start()
        process.append(th)
    try:
        for th in process:
            th.join()
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
    log.info(u"程序结束运行%s" % datetime.now())
