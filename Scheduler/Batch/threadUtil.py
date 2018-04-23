# -*- coding:utf-8 -*-
from common.timeUtil import jq_sy_time

__author__ = 'weikai'

import traceback
import datetime
import json
import threading

import gevent
from Scheduler.session import getSession
from request_cic.EntranceRenwal import cic_entrance_renwal
from request_pingan.entrance import is_pingan_renwal
from common.mongodb.mgdboperate import inser_user_renewal, query_user_renewal
from request_cjbx.start import cjbx_start
from Scheduler.settings import BATCH_CIC_QUEUE, BATCH_EPICC_QUEUE, BATCH_CICC_QUEUE, BATCH_PINGAN_QUEUE,BATCH_ANCHENG_QUEUE
from Scheduler.utils import send_batch_complete_flag


def batch_repair(onedata):
    plateNumber = onedata['plateNumber']
    sessiondt = ""
    sessiondt = getSession()
    requestcic = sessiondt['4']
    pingansession = sessiondt['1']

    carInfo = 0
    sql_carInfo = query_user_renewal(plateNumber)
    # print(sql_carInfo)
    if sql_carInfo != 0:
        onedata['vinNo'] = sql_carInfo['vinNo']
        onedata['endDate'] = sql_carInfo['endDate']
        onedata['preminuEndDate'] = sql_carInfo['endDate']
        onedata['custName'] = sql_carInfo['insuredName']
        onedata['carInfo'] = sql_carInfo
        return
    if sql_carInfo == 0:
        g1 = gevent.spawn(cic_entrance_renwal, requestcic, plateNumber)
        g2 = gevent.spawn(is_pingan_renwal, pingansession, plateNumber)
        # 通过行业协会进行查询
        g3 = gevent.spawn(cjbx_start, plateNumber)
        gevent.joinall([g1, g2, g3])
        cic_out = g1.value
        pingan_out = g2.value
        cjbx_out = g3.value
        # cjbx_out=0
        if cic_out != 0 or pingan_out != 0:
            if isinstance(cic_out, dict):
                carInfo = cic_out
                inser_user_renewal(carInfo)
                onedata['vinNo'] = carInfo['vinNo']
                onedata['endDate'] = carInfo['endDate']
                onedata['preminuEndDate'] = carInfo['endDate']
                onedata['identitCard'] = carInfo['identifyNumber']
                onedata['custName'] = carInfo['insuredName']
                onedata['phone'] = carInfo['mobile']
                onedata['engineNo'] = carInfo['engineNo']
                onedata['carInfo'] = cic_out
                return
            if isinstance(pingan_out, dict):
                carInfo = pingan_out
                inser_user_renewal(carInfo)
                onedata['vinNo'] = carInfo['vinNo']
                onedata['endDate'] = carInfo['endDate']
                onedata['preminuEndDate'] = carInfo['endDate']
                onedata['custName'] = carInfo['insuredName']
                onedata['engineNo'] = carInfo['engineNo']
                onedata['carInfo'] = pingan_out
                return
        epicc_out = query_user_renewal(plateNumber)
        if epicc_out != 0:
            carInfo = epicc_out
            onedata['vinNo'] = carInfo['vinNo']
            onedata['endDate'] = carInfo['endDate']
            onedata['preminuEndDate'] = carInfo['endDate']
            onedata['custName'] = carInfo['insuredName']
            onedata['engineNo'] = carInfo['engineNo']
            onedata['carInfo'] = epicc_out
            return
        if cjbx_out != 0:
            carInfo = cjbx_out
            onedata['vinNo'] = carInfo['vinNo']
            onedata['endDate'] = carInfo['endDate']
            onedata['preminuEndDate'] = carInfo['endDate']
            onedata['custName'] = carInfo['insuredName']
            onedata['engineNo'] = carInfo['engineNo']
            onedata['carInfo'] = cjbx_out
            return
    else:
        return


def threadpool(method, args=None):
    try:
        if len(args) <= 10:
            # 线程池
            threads = []
            print u"程序开始运行%s" % datetime.datetime.now()
            for arg in args:
                th = threading.Thread(target=method, args=(arg,))
                th.start()
                threads.append(th)
            for th in threads:
                th.join()
            print u"程序结束运行%s" % datetime.datetime.now()
        elif len(args) > 10:
            rang = (len(args) + 10 - 1) / 10
            for i in range(0, rang):
                if i < rang - 1:
                    threads = []
                    print u"程序开始运行%s" % datetime.datetime.now()
                    for arg in args[(i * 10):(10 * i + 10)]:
                        th = threading.Thread(target=method, args=(arg,))
                        th.start()
                        threads.append(th)
                    for th in threads:
                        th.join()
                    print u"程序结束运行%s" % datetime.datetime.now()
                else:
                    # 线程池
                    threads = []
                    print u"程序开始运行%s" % datetime.datetime.now()
                    for arg in args[(i * 10):len(args)]:
                        th = threading.Thread(target=method, args=(arg,))
                        th.start()
                        threads.append(th)
                    for th in threads:
                        th.join()
                    print u"程序结束运行%s" % datetime.datetime.now()
    except Exception, e:
        print(e)
        print(traceback.format_exc())


def batch_repair_thread(body, client=None):
    threadpool(batch_repair, body)
    # print(json.dumps(body,ensure_ascii=False))
    try:
        for i in body:
            if i.get("vinNo", "") == "":
                send_batch_complete_flag(client, i.get("plateNumber", ""), "0", "")
                body.remove(i)
            else:
                carinfo = i.get("carInfo", "")
                userId = i.get("userId", "")
                importBatchNumber = i.get("importBatchNumber", "")
                carinfo["importBatchNumber"] = importBatchNumber
                carinfo['userId'] = userId
                send_batch_complete_flag(client, i.get("plateNumber", ""), "1", carinfo)
                #前端使用未转化前的消息体,爬虫使用转化后的消息体
                jq_sy_out = jq_sy_time(carinfo)
                carinfo['insuranceTime'] = jq_sy_out
        print(u"发送队列消息")
        # client.send(body=json.dumps(body, ensure_ascii=False).encode(), destination=BATCH_CIC_QUEUE)
        # client.send(body=json.dumps(body, ensure_ascii=False).encode(), destination=BATCH_EPICC_QUEUE)
        # client.send(body=json.dumps(body, ensure_ascii=False).encode(), destination=BATCH_CICC_QUEUE)
        # client.send(body=json.dumps(body, ensure_ascii=False).encode(), destination=BATCH_PINGAN_QUEUE)
        client.send(body=json.dumps(body, ensure_ascii=False).encode(), destination=BATCH_ANCHENG_QUEUE)
        print(u"发送队列消息完成")
    except Exception as e:
        print(e)
        print(traceback.format_exc())
