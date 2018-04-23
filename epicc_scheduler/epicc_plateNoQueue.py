# -*- coding:utf-8 -*-
from common.MqSend import send_mq
from request_epicc_vpn.standard_flow.standard_main import standard_main

__author__ = 'weikai'
from twisted.internet import defer, reactor
from request_epicc_vpn.MyAdapter import MyAdapter
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync.client import Stomp
import traceback
import  threading
import json
from Scheduler.utils import send_complete_flag
import Scheduler.settings as se
from datetime import datetime
from request_cic.login import *
from Scheduler.insert_session import get_session
from Scheduler.session import getSession
from common.log import Logger
from request_epicc_vpn.getDataNew import check
from request_epicc_vpn.getDataNew import strat
from request_epicc_vpn.getDataNew import compare_time40
# from  request_epicc_vpn.getRenewl import xubao
from gevent import monkey
from common.mongodb.mgdboperate import query_user_permium_time,query_user_renewal,inser_user_renewal
import gevent
import time
monkey.patch_socket()
monkey.patch_ssl()
log=Logger()
'''
监听车牌号队列
'''
ERROR_QUEUE = '/queue/testConsumerError'
CONFIG = StompConfig(se.i_config.MQHOST)
QUEUE = se.EPICC_PLATE_NUMBER

def runrealtime():
    try:
        client = Stomp(CONFIG)
        client.connect()
        #client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL})
        client.subscribe(QUEUE, {StompSpec.ACK_HEADER: StompSpec.ACK_AUTO})
        while True:
            try:
                frame = client.receiveFrame()
                body=json.loads(frame.body.decode())
                #body=json.loads(frame.body.decode())
                log.info('Got %s' % json.dumps(body,ensure_ascii=False))
                #client.ack(frame)
                is_renwal_all(body,client=client)
            except Exception,e:
                log.error(e)
                log.error(frame.body)
                log.error(traceback.format_exc())

    except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())

def is_renwal_all(data,client=None):
    # base64strdt = get_session(['2'])
    # if len(base64strdt) != 0:
    #     sessiondt = getSession(base64strdt)
    #     epiccsession = sessiondt['2']
    epiccsession =""
    plateNumber=data['plateNumber']
    if len(plateNumber)!=7:
        log.error(u'plateNumber len != 7')
        return
    insureCarId=data['insureCarId']
    sessionId=data['sessionId']
    isPhone=data['isPhone']
    insuranceType=data.get("insuranceType","")
    insuranceTypeGroupId=insuranceType.get("insuranceTypeGroupId","9999")
    insuranceTypeGroup = insuranceType.get("insuranceTypeGroup","0")
    if data.get('preInsureEndDate',"")!="":
        dayGap = compare_time40(data['preInsureEndDate'])
        if dayGap>40:
            log.info(u'续保超过了40天不可以续保')
            send_mq(client, plateNumber, "续保超过了40天不可以询价", "2", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return
        #如果是续保用户
    if data.get("vinNo","") !="":
        try:
            errMsg = standard_main(data,data['preInsureEndDate'])
            if errMsg is None:
                send_mq(client, plateNumber, "", "1", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
                return
            else:
                log.error(u"查询失败,%s" % errMsg)
                send_mq(client, plateNumber, errMsg, "2", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
                return
        except:
            log.error(traceback.format_exc())
            send_mq(client, plateNumber, '未知错误', "2", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return
    try:
        epicc_out=check(plateNumber)
    except:
        log.error(traceback.format_exc())
        send_mq(client, plateNumber, '未知错误', "2", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
        return
    if epicc_out==0:
        res = query_user_renewal(plateNumber)
        if res==0:
            time.sleep(5)
            res = query_user_renewal(plateNumber)
        if res == 0:
        # 通过行业协会进行查询
            res = query_user_permium_time(plateNumber)
            if res != 0:
                res['insuredAddress'] = ""
                res['mobile'] = ""
        if res == 0 and data.get("vinNo","") =="":
            log.error(u"续保查不到车辆，需要补全信息")
            # send_complete_flag(client, plateNumber, "0", isPhone, sessionId)
            return
        else:
            if res!=0:
                data['vinNo'] = res['vinNo']
        errMsg = standard_main(data,data['preInsureEndDate'])
        if errMsg is None:
            send_mq(client, plateNumber, "", "1", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
        else:
            log.error(u"查询失败,%s" % errMsg)
            send_mq(client, plateNumber, errMsg, "2", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
        log.info("plateNumber %s = 0" % plateNumber)
    else:
        dayGap = compare_time40(epicc_out['endDate'])

        if dayGap < 0:
            epicc_out['endDate'] = ""
        elif dayGap>40:
            log.info(u'续保超过了40天不可以续保')
            send_mq(client, plateNumber, "续保超过了40天不可以询价", "2", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return
        #是续保用户发送队列
        # send_complete_flag(client,plateNumber,"1",isPhone,sessionId,epicc_out)
        log.info("plateNumber %s = 1" % plateNumber)
        data['vinNo'] = epicc_out['vinNo']
        errMsg = standard_main(data,data['preInsureEndDate'])
        if errMsg is None:
            send_mq(client, plateNumber, "", "1", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
        else:
            log.error(u"查询失败,%s" % errMsg)
            send_mq(client, plateNumber, errMsg, "2", "2", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)

def __compare_date(str_date1,str_date2):
    str_date1=datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2=datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date()>=str_date2.date():
        return True
    else:
        return False


#方法运行
threads = []
log.info("程序开始运行%s" % datetime.now())

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
log.info("程序结束运行%s" % datetime.now())

