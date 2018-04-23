# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
import traceback
from request_pingan.login import Login
from request_pingan.renewal import is_renewal, quickSearchVoucher
from request_pingan.DMVehicleInfo import queryDMVehicleInfoConfirm
from common.MqSend import send_mq
from common.log import Logger
from request_pingan.carModelQuery import query_carmodel, queryAutoModelType
from request_pingan.pingan_feebody import get_fee
from my_dbUtil.dbInsert import soupDb
from common.timeUtil import getlatedate
from request_pingan.pinganRequestBody import get_pingan_redis_body


# 续保返回用户信息 如果无 则放回0
def is_pingan_renwal(session, plateNumber, repet=0):
    log = Logger()

    try:
        if '-' not in plateNumber:
            plateNumber = plateNumber[:2] + "-" + plateNumber[2:]

        if session == '' or session is None:
            login = Login()
            session = login.login()
        try:
            repet = 0
            user_data = is_renewal(session, plateNumber)
        except Exception as e:
            if repet == 0:
                user_data = is_renewal(session, plateNumber)
                repet += 1

        # 续保用户
        if isinstance(user_data, dict):
            icorepnbs_session = user_data['request']
            quick_resp = quickSearchVoucher(icorepnbs_session, user_data)
            # 如果商业险的结束时间为空那么取交强险的结束时间作为保险时间
            str_date = quick_resp['vehicleTarget']['firstRegisterDate']
            insuranceType = quick_resp['insuranceType']
            endDate = user_data.get("sy_insuranceEndTime", "").split(" ")[0]
            if endDate == "":
                endDate = user_data.get("jq_insuranceEndTime", "").split(" ")[0]

            out = {
                "licenseNo": user_data['vehicleLicenceCode'].replace('-', ''),
                "vinNo": user_data['vehicleFrameNo'],
                "endDate": endDate,
                "CCardDetail": quick_resp['extendInfo'].get("ownerVehicleTypeCode",""),
                "brandName": quick_resp['vehicleTarget']['modifyAutoModelName'],
                "insuredName": user_data['ownerName'],
                "identifyNumber": quick_resp.get("insurantInfo", {}).get("certificateTypeNo", ""),
                "CUsageCde": "",
                "NNewPurchaseValue": "",
                "insuredAddress": "",
                "mobile": "",
                "enrollDate": str_date.split(" ")[0],  # str_date[:4]+"-"+str_date[4:6]+"-"+str_date[6:],
                "engineNo": user_data['engineNo'],
                "CModelCde": user_data['makerModel'],
                "NSeatNum": quick_resp['vehicleTarget']['vehicleSeats'],
                "COMPANY_ID": "1",
                "insuranceType": insuranceType,
                "insuranceTime": {'syEnd': user_data.get("sy_insuranceEndTime", ""),
                                  'syStart': user_data.get("sy_insuranceBeginTime", ""),
                                  'jqStart': user_data.get("jq_insuranceBeginTime", ""),
                                  'jqEnd': user_data.get("jq_insuranceEndTime", "")}
            }
            return out
        else:
            log.info(u"未查询到续信息%s", plateNumber)
            return 0
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0


def pingan_request(session, renewal_data_dt):
    '''
    :param session:
    :param dt:
    :return:
    '''
    log = Logger()
    try:
        alldata = {}
        # insureCarId = renewal_data_dt.get('insureCarId', '')
        CPlateNo = renewal_data_dt.get('plateNumber', '')
        searchVin = renewal_data_dt.get('vinNo', '')
        client = renewal_data_dt.get('client', '')
        isPhone = renewal_data_dt['isPhone']
        sessionId = renewal_data_dt.get('sessionId', '')
        #endDate = renewal_data_dt.get('endDate', '')
        insuranceType = renewal_data_dt.get("insuranceType", {})
        if isinstance(insuranceType, list):
            insureTypeGroupId = insuranceType[0].get("insuranceTypeGroupId", "")
            insuranceTypeGroup = insuranceType[0].get("insuranceTypeGroup", "")
        else:
            insureTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
            insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
        '''
        if endDate != "":
            min_time = compare_time40(endDate)
            if min_time > config.days:
                log.error("平安保险查询在40天内的 保险结束时间为 %s", endDate)
                send_mq(client, CPlateNo, "平安保险查询在40天内的 保险结束时间为 %s" % endDate, "2", "1", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return "平安保险查询在40天内的 保险结束时间为 %s" % endDate
            if min_time < 0:
                endDate = getlatedate(1)
        '''
        if not isinstance(insuranceType, list):
            # 使用redis缓存进行查询
            re_out = get_pingan_redis_body(session, renewal_data_dt)
            if re_out == 1:
                return

        if '-' not in CPlateNo:
            plateNumber = CPlateNo[:2] + "-" + CPlateNo[2:]

        if session == '' or session is None:
            login = Login()
            session = login.login()

        # 判断是否为续保用户 直接从续保信息中取用户信息 然后交换域名跳转的session
        user_data = is_renewal(session, plateNumber=plateNumber)
        if isinstance(user_data, dict):

            sy_insuranceEndTime = user_data.get("sy_insuranceEndTime", "")
            jq_insuranceEndTime = user_data.get("jq_insuranceEndTime", "")
            if sy_insuranceEndTime == "" and jq_insuranceEndTime != "":
                sy_insuranceEndTime = jq_insuranceEndTime
            if sy_insuranceEndTime != "" and jq_insuranceEndTime == "":
                jq_insuranceEndTime = sy_insuranceEndTime

            icorepnbs_session = user_data['request']
            quick_resp = quickSearchVoucher(icorepnbs_session, user_data)

            # 获取车管所信息
            session = quick_resp['request']
            vehicleFrameNo = quick_resp['vehicleTarget']['vehicleFrameNo']

            queryDMVehicleInfoConfirm_json = queryDMVehicleInfoConfirm(session, vehicleFrameNo, carMark="")
            if not isinstance(queryDMVehicleInfoConfirm_json, dict):
                send_mq(client, CPlateNo, queryDMVehicleInfoConfirm_json, "2", "1", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return
            # 查询车辆具体型号
            model = query_carmodel(session, vehicleFrameNo)
            if model == 0:
                model = queryAutoModelType(session, queryDMVehicleInfoConfirm_json['vehicleModel'])
            # 型号最后一位小写
            if model == 0:
                model = queryAutoModelType(session, queryDMVehicleInfoConfirm_json['vehicleModel'][0:-1] +
                                           queryDMVehicleInfoConfirm_json['vehicleModel'][-1].lower())
                log.info(model)
            alldata['sy_insuranceEndTime'] = sy_insuranceEndTime
            alldata['jq_insuranceEndTime'] = jq_insuranceEndTime

            alldata['insurantInfo'] = quick_resp['insurantInfo']
            alldata['vehicleTarget'] = quick_resp['vehicleTarget']
            alldata['autoModelType'] = quick_resp['autoModelType']
            alldata['DMVehicleInfo'] = queryDMVehicleInfoConfirm_json
            alldata['model'] = model
            alldata["insuranceType"] = insuranceType

            if isinstance(insuranceType, list):
                for itype in insuranceType:
                    alldata['insuranceType'] = itype
                    fee_resp = get_fee(session, alldata)
                    _result_insert(fee_resp, renewal_data_dt)
            else:
                fee_resp = get_fee(session, alldata)
                _result_insert(fee_resp, renewal_data_dt)
        else:
            if searchVin != "":

                sy_insuranceEndTime = renewal_data_dt.get("insuranceTime", {}).get("syStart", getlatedate(1))
                jq_insuranceEndTime = renewal_data_dt.get("insuranceTime", {}).get("jqStart", getlatedate(1))
                session = user_data
                vehicleFrameNo = searchVin
                # 使用redis缓存进行查询
                re_out = get_pingan_redis_body(session, renewal_data_dt)
                if re_out == 1:
                    return
                # 请求车管所
                queryDMVehicleInfoConfirm_json = queryDMVehicleInfoConfirm(session, vehicleFrameNo, carMark="")
                # log.info(json.dumps(queryDMVehicleInfoConfirm_json,ensure_ascii=False))
                if not isinstance(queryDMVehicleInfoConfirm_json, dict):
                    send_mq(client, CPlateNo, queryDMVehicleInfoConfirm_json, "2", "1", sessionId, isPhone,
                            insureTypeGroupId, insuranceTypeGroup)
                    return
                # 通过车架号查询车辆类型
                model = query_carmodel(session, vehicleFrameNo)
                # 通过车辆编码查询车辆类型
                if model == 0:
                    model = queryAutoModelType(session, queryDMVehicleInfoConfirm_json['vehicleModel'])
                # 型号最后一位小写
                if model == 0:
                    log.info(u"通过最后一位字母小写查询")
                    model = queryAutoModelType(session, queryDMVehicleInfoConfirm_json['vehicleModel'][0:-1] +
                                               queryDMVehicleInfoConfirm_json['vehicleModel'][-1].lower())
                    # log.info(model)
                # 编码查询不到使用续保信息中的车辆名字进行查询
                if model == 0 and renewal_data_dt.get("vehicleBrand", "") != "":
                    model = queryAutoModelType(session, renewal_data_dt['vehicleBrand'])
                alldata['DMVehicleInfo'] = queryDMVehicleInfoConfirm_json
                alldata['model'] = model
                alldata['sy_insuranceEndTime'] = sy_insuranceEndTime
                alldata['jq_insuranceEndTime'] = jq_insuranceEndTime
                alldata["insuranceType"] = insuranceType
                if isinstance(insuranceType, list):
                    for itype in insuranceType:
                        alldata['insuranceType'] = itype
                        fee_resp = get_fee(session, alldata)
                        _result_insert(fee_resp, renewal_data_dt)
                else:
                    fee_resp = get_fee(session, alldata)
                    _result_insert(fee_resp, renewal_data_dt)
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
        send_mq(client, CPlateNo, "%s 未知错误" % CPlateNo, "2", "1", sessionId, isPhone, insureTypeGroupId,
                insuranceTypeGroup)


def _result_insert(fee_resp, renewal_data_dt):
    log = Logger()
    insureCarId = renewal_data_dt.get('insureCarId', '')
    CPlateNo = renewal_data_dt.get('plateNumber', '')
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
        data.append("1")
        # log.info("平安开始入库 %s" % CPlateNo)
        soupDb(fee_resp['fee'], data)
        log.info("平安入库成功 %s ", CPlateNo)
        send_mq(client, CPlateNo, "", "1", "1", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
    else:
        if isinstance(fee_resp, list):
            fee_resp = json.dumps(fee_resp, encoding=False)
            log.error(fee_resp)
        else:
            log.error(fee_resp)
            send_mq(client, CPlateNo, fee_resp, "2", "1", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
