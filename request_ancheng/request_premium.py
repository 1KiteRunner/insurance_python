# coding:utf8

# 查询车辆
import codecs
import json
import pickle
import re
import sys
import time
import traceback

import jsonpath

from common.MqSend import send_mq
from common.MqSend import send_mq
from common.config import HEBAO_KEY
from common.log import Logger
from common.mongodb.mongoUtils import mg_insert
from common.redisUtil import CRedis
from my_dbUtil.dbInsert import soupDb
from request_ancheng.get_car_data import query_car_info, get_premium_request
from request_ancheng.login import login_ancheng
from request_ancheng.request_data import get_premium_data, he_bao2, save_premium
from request_cic import utils

reload(sys)
sys.setdefaultencoding('utf-8')

log = Logger()

def cut(num, c):
    c = 10 ** (-c)
    return (num // c) * c

def get_premium(session, data):
    if not session:
        session = login_ancheng()

    if not session:
        log.info(u'安诚登录失败')
        return

    searchVin = data['vinNo']
    insureCarId = data['insureCarId']
    isPhone = data['isPhone']
    sessionId = data['sessionId']
    client = data['client']
    CPlateNo = data['plateNumber']

    insuranceType = data.get("insuranceType", {})
    insuranceType_list = []
    if isinstance(insuranceType, list):
        insuranceType_list = insuranceType
    else:
        insuranceType_list.append(insuranceType)

    insuranceTypeGroupId = insuranceType_list[0].get("insuranceTypeGroupId", "")
    insuranceTypeGroup = insuranceType_list[0].get("insuranceTypeGroup", "")

    try:
        insuranceTime = data.get("insuranceTime", None)
        if insuranceTime:
            jqStart = insuranceTime.get("jqStart")
            syStart = insuranceTime.get("syStart")
        else:
            jqStart, syStart = utils.getlatedate(1), utils.getlatedate(1)

        # 查询redis中是否有信息
        r = CRedis()
        car_info = r.get_vin(searchVin, "12")
        if not car_info:
            car_info = query_car_info(session, data, syStart, CPlateNo, searchVin)
        else:
            car_info = eval(car_info)

        if not car_info:
            log.error(u'查询车辆信息失败')
            send_mq(client, CPlateNo, "查询车辆信息失败", "2", "12", sessionId, isPhone,
                    insuranceTypeGroupId, insuranceTypeGroup)
            return

        for insuranceType in insuranceType_list:

            # 车辆信息中塞入 licenseType
            car_info['licenseType'] = data.get("licenseType", "02")
            DW_DATA, Base_CProdNo, Vhl_NNewPurchaseValue = get_premium_request(session, jqStart, syStart, CPlateNo,
                                                                               searchVin, insuranceType, car_info)

            ret = get_premium_data(session, DW_DATA)
            ratio, jq_ratio = '0', '0'
            try:
                if '计算完毕' not in ret.json()['RESULT_MSG'] and '重复投保' in ret.json()['RESULT_MSG']:
                    log.info(u'重复投保，重新获取终保日期')

                    sy_end_date, jq_end_date, = None, None
                    if Base_CProdNo == "0336" or Base_CProdNo == "0335":
                        if '计算完毕' not in ret.json()['RESULT_MSG'] and '商业' in ret.json()['RESULT_MSG']:

                            ra = "\\\\n终保日期：(.+?)\\\\n"
                            rb = re.compile(ra)
                            rc = re.findall(rb, ret.content)
                            if rc and 'null' not in rc:
                                sy_end_date = rc[0][:4] + '-' + rc[0][4:6] + '-' + rc[0][6:8]

                                log.info(u'商业险终保日期 - {0}'.format(sy_end_date))

                    if Base_CProdNo == "0330":
                        ra = "\d{4}-\d{2}-\d{2}"
                        rb = re.compile(ra)

                        rc = re.findall(rb, ret.json()['RESULT_MSG'])
                        if rc and 'null' not in rc:

                            if len(rc) == 2:
                                jq_end_date = rc[1] if rc[1] > rc[0] else rc[0]
                            else:
                                jq_end_date = rc[0]

                                log.info(u'交强险终保日期 - {0}'.format(jq_end_date))

                    if Base_CProdNo == "0336_0330" or Base_CProdNo == "0335_0330":

                        if '计算完毕' not in ret.json()['RESULT_MSG'] and '商业' in ret.json()['RESULT_MSG']:

                            ra = "\\\\n终保日期：(.+?)\\\\n"
                            rb = re.compile(ra)
                            rc = re.findall(rb, ret.content)
                            if rc and 'null' not in rc:
                                end_date = rc[0][:4] + '-' + rc[0][4:6] + '-' + rc[0][6:8]

                                if 'E51' in ret.json()['RESULT_MSG']:
                                    jq_end_date = end_date
                                    log.info(u'交强险终保日期 - {0}'.format(jq_end_date))
                                else:
                                    sy_end_date = end_date
                                    log.info(u'商业险终保日期 - {0}'.format(sy_end_date))

                        elif '计算完毕' not in ret.json()['RESULT_MSG'] and '商业' not in ret.json()['RESULT_MSG']:
                            ra = "\d{4}-\d{2}-\d{2}"
                            rb = re.compile(ra)

                            rc = re.findall(rb, ret.json()['RESULT_MSG'])
                            if rc and 'null' not in rc:

                                if len(rc) == 2:
                                    end_date = rc[1] if rc[1] > rc[0] else rc[0]
                                else:
                                    end_date = rc[0]

                                if 'E51' in ret.json()['RESULT_MSG']:
                                    jq_end_date = end_date
                                    log.info(u'交强险终保日期 - {0}'.format(jq_end_date))
                                else:
                                    sy_end_date = end_date
                                    log.info(u'商业险终保日期 - {0}'.format(sy_end_date))

                    if sy_end_date or jq_end_date:

                        if jq_end_date:
                            jqStart = jq_end_date
                        if sy_end_date:
                            syStart = sy_end_date

                        # car_info['endDate'] = endDate
                        # 当是重复投保，取终保日期重新发送获取保费请求
                        DW_DATA, Base_CProdNo, Vhl_NNewPurchaseValue = get_premium_request(session, jqStart, syStart,
                                                                                           CPlateNo, searchVin,
                                                                                           insuranceType, car_info)
                        ret = get_premium_data(session, DW_DATA)

                        # 将交强险的终保日期替换后还是重复投保
                        if '终保日期' in ret.json()['RESULT_MSG'] and '重复投保' in ret.json()['RESULT_MSG']:
                            log.info(u'将交强险的终保日期替换后还是重复投保')
                            if '商业' in json.dumps(ret.json(), ensure_ascii=False):

                                ra = "\\\\n终保日期：(.+?)\\\\n"
                                rb = re.compile(ra)
                                rc = re.findall(rb, ret.content)
                                if rc and 'null' not in rc:
                                    sy_end_date = rc[0][:4] + '-' + rc[0][4:6] + '-' + rc[0][6:8]

                                    log.info(u'商业险终保日期 - {0}'.format(sy_end_date))

                                if sy_end_date:
                                    syStart = sy_end_date
                                    DW_DATA, Base_CProdNo, Vhl_NNewPurchaseValue = get_premium_request(session, jqStart,
                                                                                                       syStart,
                                                                                                       CPlateNo,
                                                                                                       searchVin,
                                                                                                       insuranceType,
                                                                                                       car_info)
                                    ret = get_premium_data(session, DW_DATA)

                        if '计算完毕' not in ret.json()['RESULT_MSG'] and '重复投保' in ret.json()['RESULT_MSG']:
                            log.info(u'重复投保，获取终保日期还是重复投保')
                            send_mq(client, CPlateNo, "重复投保，获取终保日期还是重复投保", "2", "12", sessionId, isPhone,
                                    insuranceTypeGroupId, insuranceTypeGroup)
                            return

                    else:
                        log.info(u'重复投保，无法获取终保日期，程序结束')
                        send_mq(client, CPlateNo, "重复投保，无法获取终保日期", "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                                insuranceTypeGroup)
                        return

                if len(ret.json()['WEB_DATA']) > 0:
                    response_body_1 = json.loads(ret.text)
                    PrmCoef_DW = \
                        jsonpath.jsonpath(response_body_1, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.PrmCoef_DW')]")[0]
                    PrmCoef_DW_dataObjVoList = jsonpath.jsonpath(PrmCoef_DW, "$.dataObjVoList")
                    PrmCoef_DW_dict = PrmCoef_DW_dataObjVoList[0][0]['attributeVoList']

                    SY_PrmCoef_NResvNum1, PrmCoef_NTrafficVi = None, None
                    if PrmCoef_DW_dict["SY_PrmCoef.NResvNum1"]["value"]:
                        SY_PrmCoef_NResvNum1 = float(PrmCoef_DW_dict["SY_PrmCoef.NResvNum1"]["value"])  # 无忧赔款优待系数

                    if PrmCoef_DW_dict["PrmCoef.NTrafficVi"]["value"]:
                        PrmCoef_NTrafficVi = float(PrmCoef_DW_dict["PrmCoef.NTrafficVi"]["value"])  # 交通违法调整系数

                    if SY_PrmCoef_NResvNum1 and PrmCoef_NTrafficVi:
                        PrmCoef_NExpectTotal = float(SY_PrmCoef_NResvNum1) * float(
                            PrmCoef_NTrafficVi) * 0.85 * 0.85  # 整单期望折扣

                        # 带上整单期望折扣重新发送请求
                        DW_DATA, Base_CProdNo, Vhl_NNewPurchaseValue = get_premium_request(session, jqStart, syStart,
                                                                                           CPlateNo, searchVin,
                                                                                           insuranceType,
                                                                                           car_info,
                                                                                           PrmCoef_NExpectTotal=str(
                                                                                               PrmCoef_NExpectTotal))
                        ret = get_premium_data(session, DW_DATA)
                    VsTax_NAggTax = None
                    if len(ret.json()['WEB_DATA']) > 0:

                        response_body_2 = json.loads(ret.text)

                        PrmCoef_DW = \
                            jsonpath.jsonpath(response_body_2, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.PrmCoef_DW')]")[0]
                        PrmCoef_DW_dataObjVoList = jsonpath.jsonpath(PrmCoef_DW, "$.dataObjVoList")
                        PrmCoef_DW_dict = PrmCoef_DW_dataObjVoList[0][0]['attributeVoList']

                        # 获取商业险系数

                        if PrmCoef_DW_dict["SY_PrmCoef.NTotDisc"]["value"]:
                            ratio = float(PrmCoef_DW_dict["SY_PrmCoef.NTotDisc"]["value"])  # 商业险系数
                        if PrmCoef_DW_dict["JQ_PrmCoef.NTotDisc"]["value"]:
                            jq_ratio = float(PrmCoef_DW_dict["JQ_PrmCoef.NTotDisc"]["value"]) / 100  # 交强险系数

                        VsTax_DW = \
                            jsonpath.jsonpath(response_body_2, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.VsTax_DW')]")[0]
                        VsTax_DW_dataObjVoList = jsonpath.jsonpath(VsTax_DW, "$.dataObjVoList")
                        if VsTax_DW_dataObjVoList[0]:
                            VsTax_DW_dict = VsTax_DW_dataObjVoList[0][0]['attributeVoList']

                            VsTax_NAggTax = float(VsTax_DW_dict["VsTax.NAggTax"]["value"])  # 车船税
                            log.info('车船税 - {0}'.format(VsTax_NAggTax))

                        Cvrg_DW = jsonpath.jsonpath(response_body_2, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Cvrg_DW')]")[
                            0]
                        Cvrg_DW_dataObjVoList = jsonpath.jsonpath(Cvrg_DW, "$.dataObjVoList")

                        attrs = Cvrg_DW_dataObjVoList[0]

                    else:
                        msg = ret.json()['RESULT_MSG'].replace("\n", "")

                        if '期望折扣' in msg:

                            ra = "[0-9]*\.?[0-9]+"
                            rb = re.compile(ra)

                            msg_list = re.findall(rb, msg)

                            PrmCoef_NExpectTotal = float(msg_list[0])
                            # 返回期望折扣错误重新发送请求
                            DW_DATA, Base_CProdNo, Vhl_NNewPurchaseValue = get_premium_request(session, jqStart,
                                                                                               syStart, CPlateNo,
                                                                                               searchVin,
                                                                                               insuranceType, car_info,
                                                                                               PrmCoef_NExpectTotal=str(
                                                                                                   PrmCoef_NExpectTotal))
                            ret = get_premium_data(session, DW_DATA)
                            if len(ret.json()['WEB_DATA']) > 0:
                                response_body_2 = json.loads(ret.text)

                                PrmCoef_DW = \
                                    jsonpath.jsonpath(response_body_2,
                                                      "$.WEB_DATA[?(@.dwName=='prodDef.vhl.PrmCoef_DW')]")[0]
                                PrmCoef_DW_dataObjVoList = jsonpath.jsonpath(PrmCoef_DW, "$.dataObjVoList")
                                PrmCoef_DW_dict = PrmCoef_DW_dataObjVoList[0][0]['attributeVoList']

                                # 获取商业险系数
                                if PrmCoef_DW_dict["SY_PrmCoef.NTotDisc"]["value"]:
                                    ratio = float(PrmCoef_DW_dict["SY_PrmCoef.NTotDisc"]["value"])  # 商业险系数
                                if PrmCoef_DW_dict["JQ_PrmCoef.NTotDisc"]["value"]:
                                    jq_ratio = float(PrmCoef_DW_dict["JQ_PrmCoef.NTotDisc"]["value"]) / 100  # 交强险系数

                                VsTax_DW = \
                                    jsonpath.jsonpath(response_body_2,
                                                      "$.WEB_DATA[?(@.dwName=='prodDef.vhl.VsTax_DW')]")[0]
                                VsTax_DW_dataObjVoList = jsonpath.jsonpath(VsTax_DW, "$.dataObjVoList")

                                if VsTax_DW_dataObjVoList[0]:
                                    VsTax_DW_dict = VsTax_DW_dataObjVoList[0][0]['attributeVoList']

                                    VsTax_NAggTax = float(VsTax_DW_dict["VsTax.NAggTax"]["value"])  # 车船税
                                    log.info('车船税 - {0}'.format(VsTax_NAggTax))

                                Cvrg_DW = \
                                    jsonpath.jsonpath(response_body_2,
                                                      "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Cvrg_DW')]")[
                                        0]
                                Cvrg_DW_dataObjVoList = jsonpath.jsonpath(Cvrg_DW, "$.dataObjVoList")

                                attrs = Cvrg_DW_dataObjVoList[0]

                            else:
                                msg = ret.json()['RESULT_MSG'].replace("\n", "")
                                if '无法加载模板缓存' in msg:
                                    log.info(u'无法加载模板缓存, 重新请求')
                                    return get_premium(session, data)
                                log.error(msg)
                                send_mq(client, CPlateNo, msg, "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                                        insuranceTypeGroup)
                                return

                        else:
                            if '无法加载模板缓存' in msg:
                                log.info(u'无法加载模板缓存, 重新请求')
                                return get_premium(session, data)
                            log.error(msg)
                            send_mq(client, CPlateNo, msg, "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                                    insuranceTypeGroup)
                            return
                else:
                    msg = ret.json()['RESULT_MSG'].replace("\n", "")
                    if '无法加载模板缓存' in msg:
                        log.info(u'无法加载模板缓存, 重新请求')
                        return get_premium(session, data)
                    log.error(msg)
                    send_mq(client, CPlateNo, msg, "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                            insuranceTypeGroup)
                    return

            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
                send_mq(client, CPlateNo, "未知异常", "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                        insuranceTypeGroup)
                return

            Premium = {}
            MarkPremium = {}
            hebao_premium = {}
            total_money = 0
            total_mark_money = 0

            # 计算保费
            for i, k in enumerate(attrs):
                num = int(k["attributeVoList"]["Cvrg.NSeqNo"]["value"])
                if num == 15:
                    # otherHurtPremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 三者险
                    otherHurtPremium = float(k["attributeVoList"]["Cvrg.NCalcAnnPrm"]["value"])  # 三者险
                    total_money += otherHurtPremium
                    log.info(str(otherHurtPremium) + u' 三者险')
                    Premium['otherHurtPremium'] = round(otherHurtPremium, 2)
                    hebao_premium['otherHurtPremium'] = otherHurtPremium


                    otherHurtBenchMarkPremium = otherHurtPremium * 0.15  # 三者险不计免赔
                    total_mark_money += otherHurtBenchMarkPremium
                    MarkPremium['otherHurtBenchMarkPremium'] = round(otherHurtBenchMarkPremium, 2)

                elif num == 20:
                    # carDamagePremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 车损险应缴保费
                    carDamagePremium = float(k["attributeVoList"]["Cvrg.NCalcAnnPrm"]["value"])  # 车损险应缴保费
                    total_money += carDamagePremium
                    log.info(str(carDamagePremium) + u' 车损险应缴保费')
                    Premium['carDamagePremium'] = round(carDamagePremium, 2)
                    hebao_premium['carDamagePremium'] = carDamagePremium

                    carDamageBenchMarkPremium = carDamagePremium * 0.15  # 车损险不计免赔
                    total_mark_money += carDamageBenchMarkPremium
                    MarkPremium['carDamageBenchMarkPremium'] = round(carDamageBenchMarkPremium, 2)

                elif num == 13:
                    driverDutyPremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 车上人员险（司机）
                    total_money += driverDutyPremium
                    log.info(str(driverDutyPremium) + u' 车上人员险（司机）')
                    Premium['driverDutyPremium'] = round(driverDutyPremium, 2)
                    hebao_premium['driverDutyPremium'] = driverDutyPremium

                    driverDutyBenchMarkPremium = driverDutyPremium * 0.15  # 车上人员险（司机）不计免赔
                    total_mark_money += driverDutyBenchMarkPremium
                    MarkPremium['driverDutyBenchMarkPremium'] = round(driverDutyBenchMarkPremium, 2)

                elif num == 14:
                    passengerDutyPremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 车上人员险（乘客）
                    total_money += passengerDutyPremium
                    log.info(str(passengerDutyPremium) + u' 车上人员险（乘客）')
                    Premium['passengerDutyPremium'] = round(passengerDutyPremium, 2)
                    hebao_premium['passengerDutyPremium'] = passengerDutyPremium

                    passengerBenchMarkPremium = passengerDutyPremium * 0.15  # 车上人员险（乘客）不计免赔
                    total_mark_money += passengerBenchMarkPremium
                    MarkPremium['passengerBenchMarkPremium'] = round(passengerBenchMarkPremium, 2)

                elif num == 18:
                    carTheftPremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 盗抢险
                    total_money += carTheftPremium
                    log.info(str(carTheftPremium) + u' 盗抢险')
                    Premium['carTheftPremium'] = round(carTheftPremium, 2)
                    hebao_premium['carTheftPremium'] = carTheftPremium

                    carTheftBenchMarkPremium = carTheftPremium * 0.20  # 盗抢险不计免赔
                    total_mark_money += carTheftBenchMarkPremium
                    MarkPremium['carTheftBenchMarkPremium'] = round(carTheftBenchMarkPremium, 2)

                elif num == 19:
                    carNickPremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 划痕险
                    total_money += carNickPremium
                    log.info(str(carNickPremium) + u' 划痕险')
                    Premium['carNickPremium'] = round(carNickPremium, 2)
                    hebao_premium['carNickPremium'] = carNickPremium

                    carNickBenchMarkPremium = carNickPremium * 0.15  # 划痕险不计免赔
                    total_mark_money += carNickBenchMarkPremium
                    MarkPremium['carNickBenchMarkPremium'] = round(carNickBenchMarkPremium, 2)

                elif num == 8:
                    glassBrokenPremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 玻璃破碎险
                    total_money += glassBrokenPremium
                    log.info(str(glassBrokenPremium) + u' 玻璃破碎险')
                    Premium['glassBrokenPremium'] = round(glassBrokenPremium, 2)
                    hebao_premium['glassBrokenPremium'] = glassBrokenPremium

                    glassBrokenMarkPremium = glassBrokenPremium * 0.20  # 玻璃破碎险不计免赔
                    total_mark_money += glassBrokenMarkPremium
                    MarkPremium['glassBrokenMarkPremium'] = round(glassBrokenMarkPremium, 2)

                elif num == 5:
                    carFirePremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 自燃险
                    total_money += carFirePremium
                    log.info(str(carFirePremium) + u' 自燃险')
                    Premium['carFirePremium'] = round(carFirePremium, 2)
                    hebao_premium['carFirePremium'] = carFirePremium

                    carFireMarkPremium = carFirePremium * 0.20  # 自燃险不计免赔
                    total_mark_money += carFireMarkPremium
                    MarkPremium['carFireMarkPremium'] = round(carFireMarkPremium, 2)

                elif num == 10:
                    engineWadingPremium = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * ratio  # 涉水险
                    total_money += engineWadingPremium
                    log.info(str(engineWadingPremium) + u' 涉水险')
                    Premium['engineWadingPremium'] = round(engineWadingPremium, 2)
                    hebao_premium['engineWadingPremium'] = engineWadingPremium

                    engineWadingMarkPremium = engineWadingPremium * 0.15  # 涉水险不计免赔
                    total_mark_money += engineWadingMarkPremium
                    MarkPremium['engineWadingMarkPremium'] = round(engineWadingMarkPremium, 2)

                elif num == 1:
                    compulsory_insurance = float(k["attributeVoList"]["Cvrg.NBefPrm"]["value"]) * jq_ratio  # 交强险
                    log.info(str(compulsory_insurance) + u' 交强险')
                    Premium['compulsory_insurance'] = round(compulsory_insurance, 2)
                    hebao_premium['compulsory_insurance'] = compulsory_insurance

                if VsTax_NAggTax:
                    Premium['NAggTax'] = round(VsTax_NAggTax, 2)
                    hebao_premium['NAggTax'] = VsTax_NAggTax

            total_premium = total_money + total_mark_money

            log.info(u'商业险应缴保费总额 - {0}'.format(total_money))
            log.info(u'应缴保费不计免赔总额 - {0}'.format(total_mark_money))
            log.info(u'应缴保费总额 - {0}'.format(total_premium))

            # hebao_premium = Premium
            hebao_premium['total_mark_premium'] = total_mark_money
            hebao_premium['total_premium'] = total_premium

            BaoE = {}

            _driverDutyPremium = insuranceType.get("driverDutyPremium", None)
            _carDamagePremium = insuranceType.get("carDamagePremium", "0")
            _otherHurtPremium = insuranceType.get("otherHurtPremium", None)
            _passengerDutyPremium = insuranceType.get("passengerDutyPremium", None)
            _carTheftPremium = insuranceType.get("carTheftPremium", "0")
            _carFireBrokenBenchMarkPremium = insuranceType.get("carFirePremium", "0")
            _engineWadingBenchMarkPremium = insuranceType.get("engineWadingPremium", "0")
            _carNickPremium = insuranceType.get("carNickPremium", None)  # 划痕险

            Vhl_NNewPurchaseValue = car_info['Vhl_NNewPurchaseValue']
            seats = car_info.get('seats', 5)

            otherHurtBaoE = float(_otherHurtPremium.get("Amount")) if _otherHurtPremium and int(
                _otherHurtPremium.get("isCheck"), 0) and int(_otherHurtPremium.get("Amount"), 0) else None  # 三者险保额
            if otherHurtBaoE:
                BaoE['otherHurtBaoE'] = round(otherHurtBaoE, 2)

            carDamageBaoE = float(Vhl_NNewPurchaseValue) if int(_carDamagePremium) else None  # 车损险保额
            if carDamageBaoE:
                BaoE['carDamageBaoE'] = round(carDamageBaoE, 2)

            driverDutyBaoE = float(_driverDutyPremium.get("Amount")) if _driverDutyPremium and int(
                _driverDutyPremium.get("isCheck"), 0) and int(_driverDutyPremium.get("Amount"), 0) else None  # 驾驶人责任险
            if driverDutyBaoE:
                BaoE['driverDutyBaoE'] = round(driverDutyBaoE, 2)

            passengerDutyBaoE = float(_passengerDutyPremium.get("Amount")) * (
                seats - 1) if _passengerDutyPremium and int(_passengerDutyPremium.get("isCheck"), 0) and int(
                _passengerDutyPremium.get("Amount"), 0) else None  # 乘客责任险
            if passengerDutyBaoE:
                BaoE['passengerDutyBaoe'] = round(passengerDutyBaoE, 2)

            carTheftBaoE = float(Vhl_NNewPurchaseValue) if int(_carTheftPremium) else None  # 车盗险保额
            if carTheftBaoE:
                BaoE['carTheftBaoE'] = round(carTheftBaoE, 2)

            carNickBaoE = float(_carNickPremium.get("Amount")) if _carNickPremium and int(
                _carNickPremium.get("isCheck"),
                0) and int(
                _carNickPremium.get("Amount"), 0) else None  # 划痕险保额
            if carNickBaoE:
                BaoE['carNickBaoE'] = round(carNickBaoE, 2)

            engineWadingBaoE = float(Vhl_NNewPurchaseValue) if int(_engineWadingBenchMarkPremium) else None  # 涉水险保额
            if engineWadingBaoE:
                BaoE['engineWadingBaoE'] = round(engineWadingBaoE, 2)

            carFireBaoE = float(Vhl_NNewPurchaseValue) if int(_carFireBrokenBenchMarkPremium) else None  # 自燃险保额
            if carFireBaoE:
                BaoE['carFireBaoE'] = round(carFireBaoE, 2)

            disCount = {
                "sy_disCount": ratio,
                "jq_disCount": jq_ratio
            }

            PremiumInfo = [Premium, BaoE, MarkPremium, disCount]

            log.info(PremiumInfo)

            soupDb(PremiumInfo,
                   [utils.getlatedate(1) + ' 00:00:00', utils.getlatedate(365) + " 23:59:59", seats,
                    insuranceTypeGroupId,
                    insureCarId, "12"])

            send_mq(client, CPlateNo, "", "1", "12", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            log.info(u"安城入库成功:%s|%s" % (CPlateNo, searchVin))

            if HEBAO_KEY and car_info.get("licenseType", "02") != "02":
                r = CRedis()
                try:
                    DW_DATA, Base_CProdNo, Vhl_NNewPurchaseValue = get_premium_request(session, jqStart, syStart,
                                                                                       CPlateNo, searchVin,
                                                                                       insuranceType, car_info,
                                                                                       hebao_premium=hebao_premium)

                    ret = save_premium(session, DW_DATA)

                    WEB_DATA = ret.json()['WEB_DATA']

                    sy_appno, jq_appno = '', ''
                    for data in WEB_DATA:
                        if data['dataObjVoList']:
                            if 'SY_Base.CAppNo' in data['dataObjVoList'][0]['attributeVoList']:
                                sy_appno = data['dataObjVoList'][0]['attributeVoList']['SY_Base.CAppNo']['value']
                            if 'JQ_Base.CAppNo' in data['dataObjVoList'][0]['attributeVoList']:
                                jq_appno = data['dataObjVoList'][0]['attributeVoList']['JQ_Base.CAppNo']['value']

                    if sy_appno:
                        log.info(u'商业险投保单号 - {0}'.format(sy_appno))
                        ret = he_bao2(session, sy_appno)
                        RESULT_TYPE = ret.json()["RESULT_TYPE"]
                        RESULT_MSG = ret.json()["RESULT_MSG"].replace("\n", "")
                        log.info(u'核保状态 - {0} - {1}'.format(RESULT_TYPE, RESULT_MSG))

                        SY_PremiumInfo = PremiumInfo
                        if 'compulsory_insurance' in SY_PremiumInfo[0]:
                            SY_PremiumInfo[0].pop('compulsory_insurance')
                        if 'jq_disCount' in SY_PremiumInfo[3]:
                            SY_PremiumInfo[3].pop('jq_disCount')

                        if RESULT_TYPE == "SUCCESS":
                            data = {
                                'appNo': sy_appno,
                                'PremiumInfo': SY_PremiumInfo,
                                'insuranceType': insuranceType,
                                'create_date': time.strftime('%Y-%m-%d %X', time.localtime(time.time())),
                                'companyId': '12',
                                'Status_Code': '0',
                                'CPlateNo': CPlateNo,
                                'sessionId': sessionId,
                                'isphone': isPhone
                            }

                            mg_insert('hebaoinfo', data)
                            r.set_appno(sy_appno, '12')
                            log.info(u'商业险投保单号 - {0} - 入库成功'.format(sy_appno))
                            send_mq(client, CPlateNo, "", "1", "12", sessionId, isPhone, insuranceTypeGroupId,
                                    insuranceTypeGroup, licenseType=car_info.get("VEHICLE_TYPE", '02'),
                                    vehicle_style=car_info.get("VEHICLE_STYLE", "K33"))
                        else:
                            send_mq(client, CPlateNo, "", "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                                    insuranceTypeGroup, licenseType=car_info.get("VEHICLE_TYPE", '02'),
                                    vehicle_style=car_info.get("VEHICLE_STYLE", "K33"))

                    if jq_appno:
                        log.info(u'交强险投保单号 - {0}'.format(jq_appno))
                        ret = he_bao2(session, jq_appno)
                        RESULT_TYPE = ret.json()["RESULT_TYPE"]
                        RESULT_MSG = ret.json()["RESULT_MSG"].replace("\n", "")
                        log.info(u'核保状态 - {0} - {1}'.format(RESULT_TYPE, RESULT_MSG))

                        JQ_PremiumInfo = [{'compulsory_insurance': compulsory_insurance}, {}, {},
                                          {'jq_disCount': jq_ratio}]

                        if RESULT_TYPE == "SUCCESS":
                            data = {
                                'appNo': jq_appno,
                                'PremiumInfo': JQ_PremiumInfo,
                                'insuranceType': insuranceType,
                                'create_date': time.strftime('%Y-%m-%d %X', time.localtime(time.time())),
                                'companyId': '12',
                                'Status_Code': '0',
                                'CPlateNo': CPlateNo,
                                'sessionId': sessionId,
                                'isphone': isPhone
                            }

                            mg_insert('hebaoinfo', data)
                            log.info(u'交强险投保单号 - {0} - 入库成功'.format(jq_appno))

                    else:
                        send_mq(client, CPlateNo, "", "2", "12", sessionId, isPhone, insuranceTypeGroupId,
                                insuranceTypeGroup, licenseType=car_info.get("VEHICLE_TYPE", '02'),
                                vehicle_style=car_info.get("VEHICLE_STYLE", "K33"))

                except Exception as e:
                    log.error(e)
                    log.error(traceback.format_exc())
        return

    except Exception as e:
        log.error(traceback.format_exc())
        send_mq(client, CPlateNo, "未知异常", "2", "12", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
        return 0


if __name__ == "__main__":

    data1 = {'insureCarId': 3797, 'firstRegister': u'', 'cityCode': '32010000', 'vinNo': u'LGXC16DF1A0069957',
             'plateNumber': u'苏AHY589', 'vehicleBrand': u'', 'companyId': ['12'], 'licenseType': '02',
             'custName': u'\u9648\u7fe0\u7ea2', 'insuranceType': [{u'carDamageBenchMarkPremium': u'1',  # 车损险不计免赔
                                                                   u'carDamagePremium': u'1',  # 车损险

                                                                   u'driverDutyPremium': {u'Amount': u'0',
                                                                                          u'isCheck': u'0'},
                                                                   # 车上人员险（司机）
                                                                   u'driverDutyBenchMarkPremium': u'0',
                                                                   # 车上人员险（司机）不计免赔

                                                                   u'passengerDutyPremium': {u'Amount': u'0',
                                                                                             u'isCheck': u'0'},
                                                                   # 车上人员险（乘客）
                                                                   u'passengerBenchMarkPremium': u'0',
                                                                   # 车上人员险（乘客）不计免赔

                                                                   u'carFirePremium': u'0',  # 自燃险
                                                                   u'carFireBrokenBenchMarkPremium': u'0',  # 自燃险不计免赔

                                                                   u'carTheftPremium': u'0',  # 盗抢险
                                                                   u'carTheftBenchMarkPremium': u'0',  # 盗抢险不计免赔

                                                                   u'otherHurtPremium': {u'Amount': u'0',
                                                                                         u'isCheck': u'0'},  # 三者险
                                                                   u'otherHurtBenchMarkPremium': u'1',  # 三者险不计免赔

                                                                   u'engineWadingPremium': u'0',  # 涉水险
                                                                   u'engineWadingBenchMarkPremium': u'0',  # 涉水险不计免赔

                                                                   u'carNickPremium': {u'Amount': u'0',
                                                                                       u'isCheck': u'0'},  # 划痕险
                                                                   u'carNickBenchMarkPremium': u'0',  # 划痕险不计免赔

                                                                   u'nAggTax': u'0',

                                                                   u'insuranceTypeGroupId': u'183',

                                                                   u'glassBrokenPremium': u'0',  # 玻璃破碎险
                                                                   u'compulsoryInsurance': u'1',
                                                                   u'insuranceTypeGroup': u'1_11_110_12_2_20_3_30_4_5_50_6_8_20000_80_9'}, ],
             'sessionId': u'2bbcd99cd95d9b8fdf98b29e163686f6bca30736', 'engineNo': u'0651004', 'NSeatNum': u'5',
             'identitCard': u'320121197607280023', 'endDate': u'2017-04-7', 'isPhone': u'1'}

    datas = [data1]
    for data in datas:
        # 获取session
        r = CRedis()
        sessBase = r.get('12_COMPANY')
        if not sessBase:
            session = login_ancheng()
        else:
            session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))

        get_premium(session, data)
