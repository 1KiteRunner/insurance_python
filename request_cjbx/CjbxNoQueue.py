# -*- coding:utf-8 -*-
__author__ = 'weikai'
from twisted.internet import defer, reactor
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync.client import Stomp
import traceback
import threading
import json
import Scheduler.settings as se
from datetime import datetime
from request_cic.login import *
from request_cic.EntranceRenwal import cic_entrance_renwal
from gevent import monkey
import gevent
import time
from start import cjbx_start

monkey.patch_socket()
monkey.patch_ssl()
log = Logger()
'''
监听车牌号队列
'''
ERROR_QUEUE = '/queue/testConsumerError'
CONFIG = StompConfig(se.i_config.MQHOST)
QUEUE = se.CJBX_PLATE_NUMBER
QUEUE = "CJBX_PLATE_NUMBER"


def runrealtime():
    try:
        client = Stomp(CONFIG)
        client.connect()
        client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_AUTO})
        log = Logger()
        while True:
            try:
                frame = client.receiveFrame()
                body = json.loads(frame.body.decode())
                plateNumber = body['plateNumber']
                # log.info('Got %s' % json.dumps(body,ensure_ascii=False))
                log.info('Got %s' % plateNumber)
                licenseType = body.get('licenseType', "02")
                log.info('Got licenseType %s' % licenseType)
                log.info("start ..............")
                cjbx_start(plateNumber, licenseType)
                log.info("end ..............")
            except Exception, e:
                log.error(e)
                log.error(frame.body)
                log.error(traceback.format_exc())

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


# 方法运行
threads = []
log.info(u"程序开始运行%s" % datetime.now())
for arg in xrange(10):
    th = threading.Thread(target=runrealtime)
    th.start()
    threads.append(th)
try:
    for th in threads:
        th.join()
except Exception, e:
    log.error(e)
    log.error(traceback.format_exc())
log.info(u"程序结束运行%s" % datetime.now())
