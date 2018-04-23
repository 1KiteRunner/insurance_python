# -*- coding:utf-8 -*-
__author__ = 'weikai'
from twisted.internet import defer, reactor
import traceback
import datetime
import json
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync.client import Stomp
import settings as se
from realtimeThread import getSource
from common.log import Logger

ERROR_QUEUE = '/queue/testConsumerError'
CONFIG = StompConfig(se.i_config.MQHOST)
QUEUE = se.REAL_TIME_QUEUE
EPICC = se.EPICC_PLATE_NUMBER
log = Logger()


def runrealtime():
    try:
        client = Stomp(CONFIG)
        client.connect()
        # client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL})
        client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_AUTO})
        while True:
            try:
                frame = client.receiveFrame()
                # body=json.dumps(frame.body)
                body = json.loads(frame.body.decode())[0]
                insuranceType = body.get("insuranceType", [])[0]
                body['insuranceType'] = insuranceType
                companyId = body.get('companyId', [])
                #保险公司选择
                if len(companyId) == 0 or "2" in companyId:
                    client.send(body=json.dumps(body, ensure_ascii=False).encode(), destination=EPICC)
                log.info('Got %s' % json.dumps(body, ensure_ascii=False))
                # client.ack(frame)
                body['client'] = client
                getSource(body)
            except Exception as e:
                log.error(e)
                log.error(frame.body)
                log.error(traceback.format_exc())

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


'''
threads = []
log.info(u"程序开始运行%s" % datetime.datetime.now())

for arg in xrange(10):
    th = threading.Thread(target=runrealtime)
    th.start()
    threads.append(th)
try:
    for th in threads:
        th.join()
except Exception as e:
    log.error(e)
    log.error(traceback.format_exc())


log.info(u"程序结束运行%s" % datetime.datetime.now())
'''
if __name__ == "__main__":
    from multiprocessing import Process
    # 方法运行
    process = []
    log.info(u"程序开始运行%s" % datetime.datetime.now())

    for arg in xrange(10):
        th = Process(target=runrealtime)
        th.start()
        process.append(th)
    try:
        for th in process:
            th.join()
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
    log.info(u"程序结束运行%s" % datetime.datetime.now())
