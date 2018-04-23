# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json, traceback
from request_pingan.utils import compare_time40
from common import config
from common.log import Logger
from request_huanong.hn_carInfo import get_carInof
from request_huanong.hn_getCarModel import get_car_model1
from  request_huanong.hn_getData import get_hn_premium
from my_dbUtil.dbInsert import soupDb
from common.MqSend import send_mq
from common.redisUtil import CRedis
from request_huanong.hn_insuranceType import get_hn_insurance_type

r = CRedis()


def hn_request(session, renewal_data_dt):
    log = Logger()
    try:

        alldata = {}
        insureCarId = renewal_data_dt.get('insureCarId', '')
        CPlateNo = renewal_data_dt.get('plateNumber', '')
        searchVin = renewal_data_dt.get('vinNo', '')
        client = renewal_data_dt.get('client', '')
        isPhone = renewal_data_dt['isPhone']
        sessionId = renewal_data_dt.get('sessionId', '')
        endDate = renewal_data_dt.get('endDate', '')
        insuranceType = renewal_data_dt.get("insuranceType", {})
        if isinstance(insuranceType, list):
            insureTypeGroupId = insuranceType[0].get("insuranceTypeGroupId", "")
            insuranceTypeGroup = insuranceType[0].get("insuranceTypeGroup", "")
        else:
            insureTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
            insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
            redisbody = r.get_vin(searchVin, "13")
            if redisbody != None:
                log.info(u"华农从缓存中查询出信息%s" , searchVin)
                try:
                    redisbody = json.loads(redisbody)
                    kinds = get_hn_insurance_type(insuranceType, float(redisbody['car']['actualValueOld']),
                                                  redisbody['vehicleJingyou']['seat'],
                                                  redisbody['car']['purchasePriceOld'])
                    redisbody['kinds'] = kinds
                    if insuranceType.get("compulsoryInsurance","1") == "0":
                        redisbody["tax"]={}
                    premium = get_hn_premium(session, body_org=redisbody)
                    _result_insert(premium, renewal_data_dt)
                    return
                except Exception as e:
                    log.error(e)
                    log.error(traceback.format_exc())
        '''
        if endDate != "":
            min_time = compare_time40(endDate)
            if min_time > config.days:
                log.error("华农保险查询在40天内的 保险结束时间为 %s" % endDate)
                send_mq(client, CPlateNo, "华农保险查询在40天内的 保险结束时间为 %s" % endDate, "2", "13", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return "华农保险查询在40天内的 保险结束时间为 %s" % endDate
        '''

        # 获取车管所信息
        carInfo = get_carInof(session, searchVin)

        if not isinstance(carInfo, dict):
            log.error(u"获取车管所信息失败")
            send_mq(client, CPlateNo, "%s 获取车管所信息失败" % CPlateNo, "2", "13", sessionId, isPhone, insureTypeGroupId,
                    insuranceTypeGroup)
            return
        # 获取车辆型号信息
        vehicleJingyou = get_car_model1(session, carInfo)
        if not isinstance(vehicleJingyou, dict):
            log.error(u"获取车辆信息失败")
            send_mq(client, CPlateNo, "%s 获取车辆信息失败" % CPlateNo, "2", "13", sessionId, isPhone, insureTypeGroupId,
                    insuranceTypeGroup)
            return
        alldata = {}
        alldata['car'] = carInfo
        alldata['vehicleJingyou'] = vehicleJingyou['vehicleJingyou']
        vehicleJingyou.pop('vehicleJingyou')
        alldata['other'] = vehicleJingyou
        alldata['carInfo'] = renewal_data_dt
        premium = get_hn_premium(session, alldata=alldata)
        _result_insert(premium, renewal_data_dt)

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        send_mq(client, CPlateNo, "%s 未知错误" % CPlateNo, "2", "13", sessionId, isPhone, insureTypeGroupId,
                insuranceTypeGroup)


def _result_insert(fee_resp, renewal_data_dt):
    log = Logger()
    insureCarId = renewal_data_dt.get('insureCarId', '')
    CPlateNo = renewal_data_dt.get('plateNumber', '')
    searchVin = renewal_data_dt.get('vinNo', '')
    client = renewal_data_dt.get('client', '')
    isPhone = renewal_data_dt['isPhone']
    sessionId = renewal_data_dt.get('sessionId', '')
    insuranceType = renewal_data_dt.get("insuranceType", {})
    if isinstance(insuranceType, list):
        insureTypeGroupId = insuranceType[0].get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType[0].get("insuranceTypeGroup", "")
    else:
        insureTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
    if isinstance(fee_resp, dict):
        data = []
        data.append(fee_resp['c01beginTime'])
        data.append(fee_resp['c01endTime'])
        data.append(fee_resp['vehicleSeats'])
        data.append(insureTypeGroupId)
        data.append(insureCarId)
        data.append("13")
        log.info(fee_resp['fee'])
        log.info(data)
        soupDb(fee_resp['fee'], data)
        log.info("华农入库成功 %s " % CPlateNo)
        send_mq(client, CPlateNo, "", "1", "13", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
    else:
        log.error(fee_resp)
        send_mq(client, CPlateNo, fee_resp, "2", "13", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
        return
