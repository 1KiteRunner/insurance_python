# coding:utf8
import codecs
import json
import pickle
import re
import traceback

from bs4 import BeautifulSoup
from stompest.config import StompConfig
from stompest.sync.client import Stomp

from Scheduler import settings
from common.MqSend import send_hebao_mq
from common.log import Logger
from common.mongodb.mongoUtils import mg_update_insert, mg_find
from common.redisUtil import CRedis
from request_ancheng.login import login_ancheng
from request_ancheng.request_data import query_hebao_data, query_hebao_reason

CONFIG = StompConfig(settings.i_config.MQHOST)
log = Logger()

r = CRedis()
appno_key = '12_APPNO'


def check_reason(session, appNo):
    ret = query_hebao_reason(session, appNo)

    baodan_trails_list = []

    if len(ret.text) > 300:
        ra = "DATA:\['(.*?)'\]"
        rb = re.compile(ra)

        trail_list = re.findall(rb, ret.text)

        if not trail_list:
            return None

        html = trail_list[0]
        soup = BeautifulSoup(html, 'html.parser')

        dataobj_list = soup.findAll('dataobj')

        for soup in dataobj_list:
            baodan_trails_dict = {}

            CAppNo = soup.findAll("attribute", attrs={"name": "CAppNo"})[0].get_text()  # 投保单号
            CPlyNo = soup.findAll("attribute", attrs={"name": "CPlyNo"})[0].get_text()  # 保单号
            CUndrCnm = soup.findAll("attribute", attrs={"name": "CUndrCnm"})[0].get_text()  # 操作人
            CUndrMrk = soup.findAll("attribute", attrs={"name": "CUndrMrk"})[0].get_text()  # 操作
            TUndrTm = soup.findAll("attribute", attrs={"name": "TUndrTm"})[0].get_text()  # 操作时间
            CUndrOpn = soup.findAll("attribute", attrs={"name": "CUndrOpn"})[0].get_text()  # 备注

            baodan_trails_dict['CAppNo'] = CAppNo
            baodan_trails_dict['CPlyNo'] = CPlyNo
            baodan_trails_dict['CUndrCnm'] = CUndrCnm
            baodan_trails_dict['CUndrMrk'] = CUndrMrk
            baodan_trails_dict['TUndrTm'] = TUndrTm
            baodan_trails_dict['CUndrOpn'] = CUndrOpn

            baodan_trails_list.append(baodan_trails_dict)

    if baodan_trails_list:
        baodan_trails_list = sorted(baodan_trails_list, key=lambda x: x['TUndrTm'], reverse=True)
        baodan_trail = baodan_trails_list[0]
        msg = {'CAppNo': baodan_trail['CAppNo'], 'CPlyNo': baodan_trail['CPlyNo'], 'CUndrCnm': baodan_trail['CUndrCnm'],
               'CUndrMrk': baodan_trail['CUndrMrk'], 'TUndrTm': baodan_trail['TUndrTm'],
               'CUndrOpn': baodan_trail['CUndrOpn']}
        msg = json.dumps(msg)

        query = {'BODY.appNo': appNo}
        BODY = mg_find('hebaoinfo', query)
        if not BODY:
            log.info(u'投保单号异常 - {0}'.format(appNo))
            return

        BODY['baodan_trails'] = baodan_trails_list

        mg_update_insert('hebaoinfo', query, BODY)
        log.info(u'保单错误信息更新数据库成功 - {0}'.format(appNo))
        return msg
    else:
        log.info(u'未查到保单轨迹')
        return ""


def get_hebao(session, appNo):
    try:
        log.info(u'开始查询核保 - {0}'.format(appNo))
        query = {'BODY.appNo': appNo}
        BODY = mg_find('hebaoinfo', query)
        if not BODY:
            log.info(u'投保单号异常 - {0}'.format(appNo))
            return

        insuranceTypeGroupId = BODY['insuranceType']['insuranceTypeGroupId']
        insuranceTypeGroup = BODY['insuranceType']['insuranceTypeGroup']
        sessionId = BODY['sessionId']
        isPhone = BODY['isPhone']

        ret = query_hebao_data(session, appNo)

        ra = "DATA:\['(.*?)'\]"
        rb = re.compile(ra)

        hebao_list = re.findall(rb, ret.text)

        if not hebao_list:
            log.info(u'未查询到核保信息')
            return

        h = hebao_list[0]
        hebao_dict = {}
        soup = BeautifulSoup(h, 'html.parser')

        CAppNo = soup.findAll("attribute", attrs={"name": "CAppNo"})[0].get_text()  # 投保单号
        CProdNo = soup.findAll("attribute", attrs={"name": "CProdNo"})[0].get_text()  # 产品代码
        CProdNmeCn = soup.findAll("attribute", attrs={"name": "CProdNmeCn"})[0].get_text()  # 产品
        CAppNme = soup.findAll("attribute", attrs={"name": "CAppNme"})[0].get_text()  # 投保人名称
        CInsuredNme = soup.findAll("attribute", attrs={"name": "CInsuredNme"})[0].get_text()  # 被投保人名称
        CPlateNo = soup.findAll("attribute", attrs={"name": "CPlateNo"})[0].get_text()  # 车牌号码
        TAppTm = soup.findAll("attribute", attrs={"name": "TAppTm"})[0].get_text()  # 申请投保日期
        Status = soup.findAll("attribute", attrs={"name": "Status"})[0].get_text()  # 状态
        NPrm = soup.findAll("attribute", attrs={"name": "NPrm"})[0].get_text()  # 保费合计
        CDptCde = soup.findAll("attribute", attrs={"name": "CDptCde"})[0].get_text()  # 承保机构

        if Status == "已核待缴费":
            Status_Code = '1'
            r.srem(appno_key, appNo)
            send_hebao_mq(client, CPlateNo, "", "1", "12", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)

        elif Status == "已出保单":
            Status_Code = '1'
            r.srem(appno_key, appNo)
            send_hebao_mq(client, CPlateNo, "", "1", "12", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)

        elif Status == "核保退回":
            Status_Code = '0'
            r.srem(appno_key, appNo)
            msg = check_reason(session, appNo)  # 失败保单查看原因
            send_hebao_mq(client, CPlateNo, msg, "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                          insuranceTypeGroup)

        elif Status == "暂存":  # 暂存单有失败的有未处理的
            Status_Code = '0'
            msg = check_reason(session, appNo)
            if msg:
                r.srem(appno_key, appNo)
                send_hebao_mq(client, CPlateNo, msg, "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                              insuranceTypeGroup)

        else:
            Status_Code = ''

        hebao_dict['appNo'] = CAppNo
        hebao_dict['CProdNo'] = CProdNo
        hebao_dict['CProdNmeCn'] = CProdNmeCn
        hebao_dict['CAppNme'] = CAppNme
        hebao_dict['CInsuredNme'] = CInsuredNme
        hebao_dict['CPlateNo'] = CPlateNo
        hebao_dict['TAppTm'] = TAppTm
        hebao_dict['Status'] = Status
        hebao_dict['NPrm'] = NPrm
        hebao_dict['CDptCde'] = CDptCde
        hebao_dict['Status_Code'] = Status_Code

        BODY = dict(BODY, **hebao_dict)

        mg_update_insert('hebaoinfo', query, BODY)
        log.info(u'更新数据库成功 - {0}'.format(appNo))
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


if __name__ == "__main__":
    try:
        sessBase = r.get("12_COMPANY")
        if not sessBase:
            session = login_ancheng()
        else:
            session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))

        client = Stomp(CONFIG)
        client.connect()


        def hebao_job():
            appno_list = r.smembers(appno_key)
            for appno in appno_list:
                get_hebao(session, appno)


        import logging

        logging.basicConfig()
        from apscheduler.schedulers.blocking import BlockingScheduler

        sched = BlockingScheduler()
        sched.add_job(hebao_job, 'interval', seconds=60 * 10)
        sched.start()
    except Exception as e:
        print e
        print traceback.format_exc()
