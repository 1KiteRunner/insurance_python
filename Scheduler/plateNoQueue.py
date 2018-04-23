# -*- coding:utf-8 -*-
__author__ = 'weikai'
from twisted.internet import defer, reactor, threads
from request_ancheng.renewal import is_ancheng_renewal
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.async import Stomp
import traceback
import json
from utils import send_complete_flag
import settings as se
from datetime import datetime
from common.log import Logger

from session import getSession
from request_cic.EntranceRenwal import cic_entrance_renwal

from realtimeThread import plateNo_getSource
from request_pingan.entrance import is_pingan_renwal
from request_pingan.utils import compare_time40
from gevent import monkey
from common.MqSend import send_mq
from common.mongodb.mgdboperate import inser_user_renewal, query_user_renewal, query_user_permium_time
from common import config
from stompest.async.listener import SubscriptionListener
import gevent
import time
from twisted.python import log as twisted_log

monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_all()

'''
监听车牌号队列
'''
ERROR_QUEUE = '/queue/testConsumerError'
CONFIG = StompConfig(se.i_config.MQHOST)
QUEUE = se.COMPLETE_PLATE_NUMBER
EPICC = se.EPICC_PLATE_NUMBER
CJBX = se.CJBX_PLATE_NUMBER
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
            client.subscribe(QUEUE, headers,
                             listener=SubscriptionListener(self.consume))
        except Exception, e:
            log.error(e)
            log.error(traceback.format_exc())

    def consume(self, client, frame):

        d = threads.deferToThread(is_renwal_all, client, frame)
        d.addErrback(twisted_log.err)


def is_renwal_all(client, frame):
    data = json.loads(frame.body.decode())[0]
    insuranceType = data.get("insuranceType", [])[0]
    data['insuranceType'] = insuranceType
    client.send(body=json.dumps(data, ensure_ascii=False).encode(), destination=CJBX)
    companyId = data.get('companyId', [])
    # 货车暂时只做了人保的 如果是货车 或者挂车 只爬取人保
    licenseType = data.get('licenseType', "02")
        # 保险公司选择
    if len(companyId) == 0 or "2" in companyId:
        client.send(body=json.dumps(data, ensure_ascii=False).encode(), destination=EPICC)

    log.info('Got %s' % json.dumps(data, ensure_ascii=False))

    sessiondt = ""
    sessiondt = getSession()
    requestcic = sessiondt['4']
    loginRes = sessiondt['5']
    pingansession = sessiondt['1']
    ancheng_session = sessiondt['12']
    hn_session = sessiondt['13']

    plateNumber = data['plateNumber']
    if len(plateNumber) != 7:
        log.error(u'plateNumber len != 7')
        return
    insureCarId = data['insureCarId']
    sessionId = data['sessionId']
    isPhone = data['isPhone']
    insuranceType = data['insuranceType']
    # insureTypeGroupId=data.get("insureTypeGroupId","9999")

    carInfo = 0
    sql_carInfo = query_user_renewal(plateNumber)
    if sql_carInfo == 0:
        g1 = gevent.spawn(cic_entrance_renwal, requestcic, plateNumber)
        g2 = gevent.spawn(is_pingan_renwal, pingansession, plateNumber)
        g3 = gevent.spawn(is_ancheng_renewal, ancheng_session, plateNumber)
        gevent.joinall([g1, g2, g3])
        cic_out = g1.value
        pingan_out = g2.value
        ancheng_out = g3.value

        if cic_out != 0 or pingan_out != 0 or ancheng_out != 0:
            if isinstance(cic_out, dict):
                carInfo = cic_out
                log.info(u"通过中华联合获取到续保信息")
                inser_user_renewal(carInfo)
            if isinstance(pingan_out, dict):
                carInfo = pingan_out
                log.info(u"通过平安获取到续保信息")
                inser_user_renewal(carInfo)
            if isinstance(ancheng_out, dict):
                carInfo = ancheng_out
                log.info(u"通过安诚获取到续保信息")
                inser_user_renewal(carInfo)

                # 通过行业协会进行查询
        if carInfo == 0:
            carInfo = query_user_permium_time(plateNumber)
            if carInfo != 0:
                # log.info(carInfo)
                log.info(u"通过行业协会取到续保信息")
                carInfo['insuredAddress'] = ""
                carInfo['mobile'] = ""

        if cic_out == 0 and pingan_out == 0 and carInfo == 0:
            carInfo = query_user_renewal(plateNumber)
            if carInfo == 0:
                time.sleep(2)
                carInfo = query_user_renewal(plateNumber)
        # 通过行业协会进行查询
        if carInfo == 0:
            carInfo = query_user_permium_time(plateNumber)
            if carInfo != 0:
                carInfo['insuredAddress'] = ""
                carInfo['mobile'] = ""
        if carInfo == 0:
            # 不是续保用户
            # 添加队列
            send_complete_flag(client, plateNumber, "0", isPhone, sessionId)
            log.info("plateNumber %s = 0" % plateNumber)
    else:
        carInfo = sql_carInfo

    # 如果是续保用户
    if carInfo != 0:
        send_complete_flag(client, plateNumber, "1", isPhone, sessionId, carInfo)
        carInfo['4'] = requestcic
        carInfo['5'] = loginRes
        carInfo['1'] = sessiondt['1']
        carInfo['12'] = sessiondt['12']
        carInfo['13'] = sessiondt['13']
        # 添加client
        carInfo['insureCarId'] = insureCarId
        carInfo['client'] = client
        carInfo['sessionId'] = sessionId
        carInfo['isPhone'] = isPhone
        carInfo['companyId'] = data.get('companyId', [])
        carInfo['insuranceType'] = insuranceType
        carInfo['licenseType'] = licenseType
        plateNo_getSource(carInfo)
        # 爬取


def main():
    try:
        reactor.suggestThreadPoolSize(5)
        Consumer().runrealtime()

        reactor.run()
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


'''
#方法运行
threads = []
log.info(u"程序开始运行%s" % datetime.now())

for arg in xrange(10):
    th = threading.Thread(target=runrealtime)
    th.start()
    threads.append(th)
try:
    for th in threads:
        th.join()
except Exception,e:
    log.error(e)
    log.error(traceback.format_exc())
log.info(u"程序结束运行%s" % datetime.now())
'''
if __name__ == "__main__":
    from multiprocessing import Process

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
