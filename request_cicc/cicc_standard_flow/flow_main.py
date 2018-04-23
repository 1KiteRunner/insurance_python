# -*- coding:utf-8 -*-
import sys

from common import redisUtil
from common.MqSend import send_mq
from common.timeUtil import jq_sy_time
from request_cic.getCarModel import get_car_model

reload(sys)
sys.setdefaultencoding('utf-8')
import json
from my_dbUtil.dbInsert import soupDb
from get_check_img import get_check_img
from post_checkAnswer import post_checkAnswer
from check_car_info import check_car_info
from calculate_premium import calculate_premium
from dt_init import init_dt
import traceback
from jsonpath import jsonpath
from common.log import Logger
from request_cicc.interface import translate
import re
from common.dama.damaUtil import dama
from datetime import timedelta
from datetime import datetime
import time
r=redisUtil.CRedis()
log=Logger()
global null, false, true
null = None
false = False
true = True




def compare_time40(endtime="2017-04-03 23:59:59"):
    try:
        if " " not in endtime:
            endtime=endtime+" 23:59:59"

        currnt_time=int(time.time())
        endtime=conver_timestamp(endtime)
        out=(endtime-currnt_time)/86400
        return out
    except:
        return 10#如果有异常随便给个小于40的

def conver_timestamp(dt="2016-05-05 20:28:54"):
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)

def compare_date(str_date1, str_date2):
    str_date1 = str_date1.split(" ")[0]
    str_date2 = str_date2.split(" ")[0]
    str_date1 = datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2 = datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date() >= str_date2.date():
        return str_date2.date()
    else:
        return str_date2.date()

def flow_main(loginRes,data):
    try:
        req_session = loginRes[0]
        userId = loginRes[1]
        redis_dt = r.get_vin(data['vinNo'], "5")
        if redis_dt is not None:
            try:
                log.info(u"%s，可以从redis中获取信息" % data['vinNo'])
                dt = eval(redis_dt)
                #log.info(dt)
                dt['insuranceType'] = data['insuranceType']
                dt['req_session'] = req_session
                log.info(dt['endDate'])
                dt['endDate'] = datetime.strptime(dt['endDate'], "%Y-%m-%d").date()
                client = data['client']
                sessionId = data['sessionId']
                isPhone = data['isPhone']
                insuranceType = dt['insuranceType']  # 保险组合类型
                if isinstance(insuranceType,list):
                    insuranceTypes = insuranceType
                    for insuranceType in insuranceTypes:
                        try:
                            dt['insuranceType'] = insuranceType
                            groupId = insuranceType['insuranceTypeGroupId']
                            insuranceTypeGroup = insuranceType['insuranceTypeGroup']
                            INSURE_CAR_ID = data['insureCarId']
                            premuim_dic = calculate_premium(dt)
                            premuim_result = jsonpath(premuim_dic, "$.result")
                            if premuim_result:
                                calculateErrMeg = premuim_result[0][0].get('insuranceApplication.calculateErrMeg', None)
                                if calculateErrMeg is not None:
                                    send_mq(client, dt['licenseNo'], calculateErrMeg, "2", "5", sessionId, isPhone, groupId,insuranceTypeGroup)
                                    return calculateErrMeg
                            PremiumInfo = translate.getPriumeInf(premuim_dic, dt['insuranceType'])
                            dataDic = {
                                'startData': str(dt['endDate']),
                                'endData': str(datetime.strptime((str(dt['endDate'].year + 1) + '-' + str(dt['endDate'].month) + '-' + str(dt['endDate'].day)), "%Y-%m-%d").date())
                            }
                            data = [dataDic['startData'], dataDic['endData'], dt['seatCount'], groupId, INSURE_CAR_ID, "5"]
                            soupDb(PremiumInfo, data)
                            log.info(u"大地入库成功，%s" % dt['licenseNo'])
                            send_mq(client, dt['licenseNo'], "", "1", "5", sessionId, isPhone, groupId, insuranceTypeGroup)
                        except Exception, e:
                            log.info(u"%s，根据redis获取的信息查询保费时报正在重试正常流程" % data['vinNo'])
                            log.error(traceback.format_exc())
                            return
                    return u"大地入库成功，%s" % dt['licenseNo']
                groupId = insuranceType['insuranceTypeGroupId']
                insuranceTypeGroup = insuranceType['insuranceTypeGroup']
                INSURE_CAR_ID = data['insureCarId']
                premuim_dic = calculate_premium(dt)
                premuim_result = jsonpath(premuim_dic, "$.result")
                if premuim_result:
                    calculateErrMeg = premuim_result[0][0].get('insuranceApplication.calculateErrMeg', None)
                    if calculateErrMeg is not None:
                        send_mq(client, dt['licenseNo'], calculateErrMeg, "2", "5",sessionId, isPhone, groupId, insuranceTypeGroup)
                        return calculateErrMeg
                PremiumInfo = translate.getPriumeInf(premuim_dic, dt['insuranceType'])
                dataDic = {
                    'startData': str(dt['endDate']),
                    'endData': str(datetime.strptime((str(dt['endDate'].year + 1) + '-' + str(dt['endDate'].month) + '-' + str(dt['endDate'].day)), "%Y-%m-%d").date())
                }
                data = [dataDic['startData'], dataDic['endData'], dt['seatCount'], groupId, INSURE_CAR_ID, "5"]
                soupDb(PremiumInfo, data)
                log.info(u"大地入库成功，%s" % dt['licenseNo'])
                send_mq(client, dt['licenseNo'], "", "1", "5", sessionId , isPhone, groupId, insuranceTypeGroup)
                return u"大地入库成功，%s" % dt['licenseNo']
            except Exception,e:
                log.info(u"%s，根据redis获取的信息查询保费时报正在重试正常流程" % data['vinNo'])
                log.error(traceback.format_exc())

        dt = init_dt()
        if userId !="":
            dt['salesChannelCode'] = userId
        dt['req_session'] = req_session
        dt['vinNo'] = data['vinNo']


        dt['licenseNo'] = data['plateNumber']
        if data['firstRegister']!="":
            dt['enrollDate'] = data['firstRegister']
        dt['driverName'] = data['custName']
        dt['insuranceType'] = data['insuranceType']
        dt['client'] = data['client']
        client = data['client']
        sessionId = data['sessionId']
        isPhone = data['isPhone']

        insuranceTypeList = ""

        insuranceType = dt['insuranceType']  # 保险组合类型
        if isinstance(insuranceType,list):
            insuranceTypeList = insuranceType[1:]
            dt['insuranceType'] = insuranceType[0]
            insuranceType = insuranceType[0]
        groupId = insuranceType.get('insuranceTypeGroupId')
        insuranceTypeGroup = insuranceType['insuranceTypeGroup']
        INSURE_CAR_ID = data['insureCarId']
        data['endDate'] = jq_sy_time(data)['syStart']


        # if data['endDate']!="":
        #     dayGap = compare_time40(data['endDate'])
        #     if dayGap>40:
        #         log.error(u"上期保单截止时间超过四十天，大地不可询价。上期保单截止时间：%s" % data['endDate'])
        #         send_mq(client, dt['licenseNo'], "上期保单截止时间超过四十天，不可询价。上期保单截止时间：%s" % data['endDate'], "2", "5", sessionId, isPhone, groupId,insuranceTypeGroup)
        #         return u"上期保单截止时间超过四十天，大地不可询价。上期保单截止时间：%s" % data['endDate']
        #     elif dayGap<0:
        #         pass
        #     else:
        #         dt['endDate'] = datetime.strptime(data['endDate'], "%Y-%m-%d").date()


        #通过车架号获取校验码
        DVM_res = get_check_img(dt)
        DVM_res_items = jsonpath(DVM_res, "$.result.items")
        if DVM_res_items:
            if len(DVM_res_items)>0:
                log.info(u"车架号 %s，请求车管所完成" % dt['vinNo'])
                dt['jsCheckCode'] = DVM_res_items[0][0].get('jsCheckCode',None)
                dt['jsCheckNo'] = DVM_res_items[0][0].get('jsCheckNo',None)
                #dt['checkAnswer'] = request_cicc.util.pic2Str(base64.b64decode(dt['jsCheckCode']))
                dt['checkAnswer'] = dama("3",dt['jsCheckCode'])
                log.info(dt['checkAnswer'])

                #上报打码结果获取车管所返回信息
                post_checkAnswer_res = post_checkAnswer(dt)
                post_checkAnswer_res_items = jsonpath(post_checkAnswer_res, "$.result.items")
                count = 0

                log.info(u"上报验证码完成")
                log.info(dt['vinNo'])
                #检验返回信息中是否有校验码错误信息，校验码错误会自动重发5次
                while post_checkAnswer_res['err'] is not None:
                    log.info(post_checkAnswer_res['err'])
                    if count > 3:
                        log.error(u"打码失败")
                        send_mq(client, dt['licenseNo'], "打码失败", "2", "5", sessionId, isPhone, groupId,
                                insuranceTypeGroup)
                        return "打码失败"
                    #
                    # if (post_checkAnswer_res['err'] is None) and (post_checkAnswer_res_items[0][0].get('replacementValue') is None):
                    #     log.info(u"大地无法通过车架号获取车辆型号，正在调用中华联合接口重新尝试获取车辆型号")
                    #
                    #     car_model = get_car_model(dt['vinNo'])
                    #     gCIndustryModelName = car_model['gCIndustryModelName']
                    #     dt['gCIndustryModelName'] = gCIndustryModelName
                    #     post_checkAnswer_res = post_checkAnswer(dt)
                    #     post_checkAnswer_res_items = jsonpath(post_checkAnswer_res, "$.result.items")
                    #     count = count + 1
                    #     break
                    elif '校验码有误' in  post_checkAnswer_res.get('err','没有错误信息'):
                        dt['cacheableFlag'] = 0
                        DVM_res = get_check_img(dt)
                        dt['cacheableFlag'] = 1
                        DVM_res_items = jsonpath(DVM_res, "$.result.items")
                        dt['jsCheckCode'] = DVM_res_items[0][0].get('jsCheckCode', None)
                        dt['jsCheckNo'] = DVM_res_items[0][0].get('jsCheckNo', None)
                        #dt['checkAnswer'] = request_cicc.util.pic2Str(base64.b64decode(dt['jsCheckCode']))
                        dt['checkAnswer'] = dama("3",dt['jsCheckCode'])
                        log.info(dt['checkAnswer'])
                        post_checkAnswer_res = post_checkAnswer(dt)
                        post_checkAnswer_res_items = jsonpath(post_checkAnswer_res, "$.result.items")
                        count = count + 1
                        log.error("校验码不正确，正在重试")
                    elif '车辆型号' in post_checkAnswer_res.get('err', '没有错误信息'):

                        #调用中华联合接口获取车辆型号
                        log.info(u"大地无法通过车架号获取车辆型号，正在调用中华联合接口重新尝试获取车辆型号")

                        car_model = get_car_model(dt['vinNo'])
                        if car_model is None:
                            log.error(u'大地，车型无法获取')
                            send_mq(client, dt['licenseNo'], "大地，无法获取车型信息", "2", "5", sessionId, isPhone, groupId,insuranceTypeGroup)
                            return "大地无法获取该车型"
                        else:
                            gCIndustryModelName = car_model['gCIndustryModelName']
                            log.info(u"调用中华联合查询车辆信息结束，车辆型号为：%s" % gCIndustryModelName)
                            dt['gCIndustryModelName'] = gCIndustryModelName
                            post_checkAnswer_res = post_checkAnswer(dt)
                            post_checkAnswer_res_items = jsonpath(post_checkAnswer_res, "$.result.items")
                            count = count + 1
                    else:
                        count = count + 1

                #开始取车管所返回列表中的信息去大地系统校验获取准确的车辆信息
                if post_checkAnswer_res_items:
                    if len(post_checkAnswer_res_items)>0:
                        log.info(u"车架号 %s，提交验证码完成" % dt['vinNo'])
                        # 按照价格排序
                        car_info_list = post_checkAnswer_res_items[0]
                        car_info_list.sort(key=lambda obj: float(obj.get('replacementValue')))
                        car_info = car_info_list[0]
                        dt['modelCode'] = car_info['modelCode']

                        #获取完成准确的车辆信息
                        check_car_info_res = check_car_info(dt)
                        if check_car_info_res['err'] is None:
                           try:
                               car_dt = check_car_info_res['result']
                               dt['seatCount'] = car_dt['seatCount']
                               dt['driverName'] = car_dt.get('carOwner',"张三")
                               if car_dt['licenseNo'] !="":
                                    dt['licenseNo'] = car_dt['licenseNo']
                               dt['modelName'] = car_dt['modelName']
                               dt['motorNo'] = car_dt['engineNo']
                               dt['exhaustScale'] = car_dt['exhaustScale']
                               dt['jyPrice'] = car_dt['jyPrice']
                               dt['jyindustryModelCode'] = car_dt['jyindustryModelCode']
                               dt['net'] = car_dt['net']
                               dt['jyNoticeType'] = car_dt['jyNoticeType']
                               log.info(u'新车购置价格：'+ dt['jyPrice'])
                               dt['powerScale'] = car_dt['powerScale']
                               dt['vehicleCategory'] = car_dt['vehicleCategory']
                               dt['tonCount'] = car_dt['tonCount']
                               dt['jyCarName'] = car_dt['jyCarName']
                               dt['vehicleId'] = car_dt['id']
                               dt['enrollDate'] = car_dt['shEnrollDate']
                               if dt.get('endDate',"")=="":
                                    dt['endDate'] = datetime.today().date() + timedelta(1)
                               #通过以上获取到的准确信息进行最终报价  报价失败的话尝试解析错误信息进行重新报价
                               premuim_dic = calculate_premium(dt)
                               premuim_result = jsonpath(premuim_dic, "$.result")
                               if premuim_result:
                                   calculateErrMeg = premuim_result[0][0].get('insuranceApplication.calculateErrMeg', None)
                                   while calculateErrMeg is not None:
                                       if "车主名称与交管信息不一致" in calculateErrMeg:
                                           str2 = calculateErrMeg.split("：")
                                           str2 = str2[2].split(';')
                                           dt['driverName'] = str2[0]
                                       elif "保单发生重复投保" in calculateErrMeg:
                                           str1 = "\d{4}-\d{2}-\d{2} "
                                           datelist = re.findall(str1, calculateErrMeg, re.S)
                                           if len(datelist) == 2:
                                               endDate = compare_date(datelist[0], datelist[1])
                                               dayGap = compare_time40(str(endDate))
                                               if dayGap>40:
                                                   log.error(calculateErrMeg)
                                                   send_mq(client, dt['licenseNo'], calculateErrMeg, "2", "5",sessionId, isPhone, groupId, insuranceTypeGroup)
                                                   return calculateErrMeg
                                               else:
                                                    dt['endDate'] = compare_date(datelist[0], datelist[1])
                                           else:
                                               log.error(calculateErrMeg)
                                               send_mq(client, dt['licenseNo'], calculateErrMeg, "2", "5", sessionId,isPhone, groupId, insuranceTypeGroup)
                                               return calculateErrMeg
                                           print dt['endDate']
                                       elif "整备质量" in calculateErrMeg:
                                           net = calculateErrMeg.split("：")
                                           net = net[2].split(';')
                                           dt['net'] = net[0]
                                       elif '核定载客人数与交管信息不一致' in calculateErrMeg:
                                           dt['seatCount'] = calculateErrMeg.split("：")[2].split(';')[0].split('.')[0]
                                       else:
                                           log.error(calculateErrMeg)
                                           send_mq(client, dt['licenseNo'], calculateErrMeg, "2", "5", sessionId, isPhone,groupId, insuranceTypeGroup)
                                           return calculateErrMeg
                                       premuim_dic = calculate_premium(dt)
                                       premuim_result = jsonpath(premuim_dic, "$.result")
                                       if premuim_result:
                                           calculateErrMeg = premuim_result[0][0].get('insuranceApplication.calculateErrMeg', None)
                                       else:
                                           break
                                   if len(premuim_result[0][0].get('insuranceApplication.reinsureInfos', ""))>0 :
                                        log.info(premuim_result[0][0].get('insuranceApplication.reinsureInfos', ""))
                                        date = int(float(time.mktime(time.strptime(premuim_result[0][0].get('insuranceApplication.reinsureInfos', "")[0]['endDate'].replace('CST',''),"%a %b %d %H:%M:%S %Y"))))
                                        endDate = datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(date)),"%Y-%m-%d").date()
                                        dayGap = compare_time40(str(endDate))
                                        if dayGap > 40:
                                           log.error(u"重复投保")
                                           send_mq(client, dt['licenseNo'], calculateErrMeg, "2", "5", sessionId, isPhone,
                                                       groupId, insuranceTypeGroup)
                                           return u"重复投保"
                                        else:
                                            dt['endDate'] = endDate
                                        premuim_dic = calculate_premium(dt)
                                        # premuim_result = jsonpath(premuim_dic, "$.result")
                               PremiumInfo = translate.getPriumeInf(premuim_dic, dt['insuranceType'])
                               dataDic = {
                                    'startData':str(dt['endDate']),
                                    'endData': str(datetime.strptime((str(dt['endDate'].year + 1) + '-' + str(dt['endDate'].month) + '-' + str(dt['endDate'].day)),"%Y-%m-%d").date())
                               }
                               data = [dataDic['startData'], dataDic['endData'], dt['seatCount'], groupId, INSURE_CAR_ID, "5"]
                               log.info(PremiumInfo)
                               dt['endDate'] = str(dt['endDate'])
                               dt.pop('req_session')
                               dt.pop('client')
                               r.set_vin(dt['vinNo'], "5", json.dumps(dt, ensure_ascii=False))
                               dt['req_session'] = req_session
                               dt['client'] = client
                               dt['endDate'] = datetime.strptime(dt['endDate'], "%Y-%m-%d").date()
                               soupDb(PremiumInfo,data)
                               log.info(u"大地入库成功，%s" % dt['licenseNo'])
                               send_mq(client, dt['licenseNo'], "", "1", "5", sessionId, isPhone, groupId, insuranceTypeGroup)
                               if insuranceTypeList!="":
                                   for insuranceType in insuranceTypeList:
                                       try:
                                           dt['insuranceType'] = insuranceType
                                           groupId = insuranceType['insuranceTypeGroupId']
                                           insuranceTypeGroup = insuranceType['insuranceTypeGroup']
                                           premuim_dic = calculate_premium(dt)
                                           premuim_result = jsonpath(premuim_dic, "$.result")
                                           if premuim_result:

                                               calculateErrMeg = premuim_result[0][0].get('insuranceApplication.calculateErrMeg', None)
                                               if calculateErrMeg is not None:
                                                   send_mq(client, dt['licenseNo'], calculateErrMeg, "2", "5",sessionId, isPhone, groupId,insuranceTypeGroup)
                                                   return calculateErrMeg
                                           PremiumInfo = translate.getPriumeInf(premuim_dic, dt['insuranceType'])
                                           dataDic = {
                                               'startData': str(dt['endDate']),
                                               'endData': str(datetime.strptime((str(dt['endDate'].year + 1) + '-' + str(dt['endDate'].month) + '-' + str(dt['endDate'].day)),"%Y-%m-%d").date())
                                           }
                                           data = [dataDic['startData'], dataDic['endData'], dt['seatCount'], groupId,INSURE_CAR_ID, "5"]
                                           soupDb(PremiumInfo, data)
                                           log.info(u"大地入库成功，%s" % dt['licenseNo'])
                                           send_mq(client, dt['licenseNo'], "", "1", "5", sessionId, isPhone, groupId,insuranceTypeGroup)
                                           return u"大地入库成功，%s" % dt['licenseNo']
                                       except Exception, e:
                                           log.info(u"%s，根据redis获取的信息查询保费时报正在重试正常流程" % dt['vinNo'])
                                           log.error(traceback.format_exc())
                                           return
                           except:
                               send_mq(client, dt['licenseNo'], "未知错误", "2", "5", sessionId, isPhone, groupId,insuranceTypeGroup)
                               log.error(traceback.format_exc())
                        else:
                            send_mq(client, dt['licenseNo'], "无法获取到车管所信息", "2", "5", sessionId, isPhone, groupId, insuranceTypeGroup)
                            log.info(u"车架号 %s，无法获取到车管所信息" % dt['vinNo'])
                            return
                else:
                    send_mq(client, dt['licenseNo'], "无法获取到车管所信息", "2", "5", sessionId, isPhone, groupId,insuranceTypeGroup)
                    log.info(u"车架号 %s，无法获取到车管所信息" % dt['vinNo'])
                    return post_checkAnswer_res['err']
            else:
                send_mq(client, dt['licenseNo'], "无法获取到车管所信息", "2", "5", sessionId, isPhone, groupId,insuranceTypeGroup)
                log.info(u"车架号 %s，无法获取到车管所信息" % dt['vinNo'])
        else:
            send_mq(client, dt['licenseNo'], "无法获取到车管所信息", "2", "5", sessionId, isPhone, groupId, insuranceTypeGroup)
            log.info(u"车架号 %s，无法获取到车管所信息"% dt['vinNo'])
            return DVM_res['err']
    except:
        log.error(traceback.format_exc())
        send_mq(client, dt['licenseNo'], "未知异常", "2", "5", sessionId, isPhone, groupId, insuranceTypeGroup)
        return "未知异常"



if __name__=="__main__":
    flow_main()





