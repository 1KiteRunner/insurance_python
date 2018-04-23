# coding:utf8
import sys
from common.sessionUtil import get_session
from request_xinda.request_data import get_car_vin, get_car_info, get_car_value, get_InputSubmitBI, get_ValidateRulesBI, \
    get_premium_data, get_jq_data, get_save_tmp_premium, get_riskLevelFlag, sav_premium
from request_xinda.xd_parse import parse_vin_car, xd_parse_get_premuim
from request_xinda.xd_insuranceType import choose_jq_sy
import json
from common.getSpecialType import get_main_cartype, get_specical_car_type
from my_dbUtil.dbInsert import soupDb
from request_huanong.hn_util import calc_user_years
from xd_login import xd_login
from common.timeUtil import getlatedate
from common.MqSend import send_mq
from common.log import Logger
from request_xinda.xd_carcodetype import get_car_type, get_bi_rate

reload(sys)
sys.setdefaultencoding('utf8')
log = Logger()


# licenseNoBC = '苏EE9N06'.encode('gbk')
# FrameNo = 'LSVAG2186B2299594'  # 车架号


def xd_request_premium(renewal_data_dt):
    try:
        alldata = {}
        # licenseNoBC = '苏EE9N06'.encode('gbk')
        # FrameNo = 'LSVAG2186B2299594'  # 车架号
        insureCarId = renewal_data_dt.get('insureCarId', '')

        CPlateNo = renewal_data_dt.get('plateNumber', '')
        licenseNoBC = CPlateNo.encode('gbk')
        searchVin = renewal_data_dt.get('vinNo', '')
        FrameNo = searchVin
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

        permium_dict = {}
        # session = get_session("14")
        # if session is None:
        session = xd_login()
        sy_insuranceEndTime = renewal_data_dt.get("insuranceTime", {}).get("syStart", getlatedate(1))
        jq_insuranceEndTime = renewal_data_dt.get("insuranceTime", {}).get("jqStart", getlatedate(1))

        permium_dict['insuranceType'] = insuranceType
        permium_dict['jq_insuranceEndTime'] = jq_insuranceEndTime
        permium_dict['sy_insuranceEndTime'] = sy_insuranceEndTime

        # vin查询
        car_vin_ret = get_car_vin(licenseNoBC, FrameNo, session)
        carVinInfo = parse_vin_car(car_vin_ret)
        if not isinstance(carVinInfo, dict):
            send_mq(client, CPlateNo, "获取车辆型号失败", "2", "14", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
            return
        permium_dict['carVinInfo'] = carVinInfo

        # 获取车管所信息
        vehicle = get_car_info(licenseNoBC, FrameNo, session)
        if not isinstance(vehicle, dict):
            send_mq(client, CPlateNo, "获取车管所信息失败%s" % licenseNoBC, "2", "14", sessionId, isPhone, insureTypeGroupId,
                    insuranceTypeGroup)
            return
        permium_dict['vehicle'] = vehicle
        # 判断车辆种类
        syName = carVinInfo['syName']
        mainCarKindCodeBC = get_main_cartype(carVinInfo['brandNameBC'])
        # 如果带挂 说明是挂车
        if "挂" in CPlateNo:
            mainCarKindCodeBC = "G"
        if mainCarKindCodeBC == "BG":
            mainCarKindCodeBC = "H"
        if mainCarKindCodeBC is None:
            # 非客车
            # 如果还是None 取车辆名称型号 判断特种车
            mainCarKindCodeBC = get_specical_car_type(carVinInfo['brandNameBC'])
            if isinstance(mainCarKindCodeBC, dict):
                if mainCarKindCodeBC['type'] == "货车":
                    mainCarKindCodeBC = "H"
                elif mainCarKindCodeBC['type'] == "挂车":
                    mainCarKindCodeBC = "G"
        if mainCarKindCodeBC is None:
            # 如果还是None 取vin查询返回的商业险名称
            if "吨" in syName:
                mainCarKindCodeBC = "H"
            if "特" in syName:
                if "一" in syName:
                    mainCarKindCodeBC = "T1"
                elif "二" in syName:
                    mainCarKindCodeBC = "T2"
                elif "三" in syName:
                    mainCarKindCodeBC = "T3"
                elif "四" in syName:
                    mainCarKindCodeBC = "T4"
                else:
                    mainCarKindCodeBC = "H"
            else:
                mainCarKindCodeBC = "A"
        permium_dict['carVinInfo']['mainCarKindCodeBC'] = mainCarKindCodeBC
        if mainCarKindCodeBC == "A":
            # 如果大类是客车 那么子类也为客车，使用性质为家庭自用carKindCodeBC
            permium_dict['carVinInfo']['mainCarKindCodeBC'] = "A0"  # 种类为A0
            permium_dict['carVinInfo']['useNatureCodeBC'] = "8A"
        if mainCarKindCodeBC == "G":
            #
            permium_dict['carVinInfo']['mainCarKindCodeBC'] = "G0"  #
            permium_dict['carVinInfo']['useNatureCodeBC'] = "9D"
        if mainCarKindCodeBC == "H":
            if "XXY" in carVinInfo['brandNameBC']:
                # 厢式货车
                permium_dict['carVinInfo']['carKindCodeBC'] = "H3"
            elif get_main_cartype(carVinInfo['brandNameBC']) == "BG":
                permium_dict['carVinInfo']['carKindCodeBC'] = "H5"  #
            else:
                permium_dict['carVinInfo']['carKindCodeBC'] = "H0"  #
            # 使用性质
            permium_dict['carVinInfo']['useNatureCodeBC'] = "9D"

        # carTypeCodeBC判断车辆类型
        carTypeCodeBC = "1"
        myCarTypeCodeBC = "1"
        if len(syName) != 0:
            codelist = get_car_type(syName)
            carTypeCodeBC = codelist[2]
            myCarTypeCodeBC = codelist[3]
        permium_dict['vehicle']['carTypeCodeBC'] = carTypeCodeBC
        permium_dict['vehicle']['myCarTypeCodeBC'] = myCarTypeCodeBC
        # 判断交强险与商业险选项
        # 获取车辆实际价格以及纯风险保费
        actualValue = get_car_value(permium_dict, session, sy_insuranceEndTime)
        if not isinstance(actualValue, dict):
            send_mq(client, CPlateNo, "获取车辆协商价格以及纯风险保费失败%s" % licenseNoBC, "2", "14", sessionId, isPhone,
                    insureTypeGroupId, insuranceTypeGroup)
            return
        permium_dict['actualValue'] = actualValue
        # 计算车辆实际使用年限
        userYear = calc_user_years(sy_insuranceEndTime, vehicle['enrollDateBC'])
        permium_dict['actualValue']['useYears'] = userYear
        chose_flag = choose_jq_sy(permium_dict['insuranceType'])
        JQ = {}
        if chose_flag == "2" or chose_flag == "3":
            # 只选了交强险
            JQ = get_jq_data(session, permium_dict)
            if not isinstance(JQ, dict):
                send_mq(client, CPlateNo, "交强险重复投保%s" % licenseNoBC, "2", "14", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return
            permium_dict['JQ'] = JQ
            if chose_flag == "2":
                jq_insert = [{"compulsory_insurance": JQ['compulsory_insurance'], "NAggTax": JQ['NAggTax']}, {}, {},
                             {"jq_disCount": JQ['jq_disCount']}]
                soupDb(jq_insert, [getlatedate(1) + ' 00:00:00', getlatedate(365) + " 23:59:59", vehicle['seatCountBC'],
                                   insureTypeGroupId, insureCarId, "14"])
                # 发送成功队列
                send_mq(client, CPlateNo, "", "1", "14", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
                log.info(u"信达入库成功:%s|%s" % (CPlateNo, searchVin))
                return

        if chose_flag == "1" or chose_flag == "3":

            # 请求系数以及等
            SubmitBI = get_InputSubmitBI(session, permium_dict)
            if not isinstance(SubmitBI, dict):
                send_mq(client, CPlateNo, SubmitBI, "2", "14", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return
            permium_dict['SubmitBI'] = SubmitBI

            Rules = get_ValidateRulesBI(session, permium_dict)
            if not isinstance(Rules, dict):
                send_mq(client, CPlateNo, SubmitBI, "2", "14", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return
            permium_dict['Rules'] = Rules

            # 计算修改费率
            get_bi_rate(permium_dict)
            # 请求保费请求 查询码
            premium_data = get_premium_data(session, permium_dict)
            permium_dict['premium'] = premium_data

            SY = xd_parse_get_premuim(permium_dict)
            permium_dict['sy_premuim'] =SY
            # 发送保单暂存
            permium_dict['tempSaveFlag'] = "1"
            tmp_out = get_save_tmp_premium(session, permium_dict)
            if not isinstance(tmp_out, dict):
                send_mq(client, CPlateNo, tmp_out, "2", "14", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return
            permium_dict['tmpBICI'] = tmp_out
            permium_dict['tempSaveFlag'] = "0"
            riskLevelFlag = get_riskLevelFlag(session, permium_dict)
            if not isinstance(riskLevelFlag, dict):
                send_mq(client, CPlateNo, riskLevelFlag, "2", "14", sessionId, isPhone,
                        insureTypeGroupId, insuranceTypeGroup)
                return
            permium_dict['riskLevel'] = riskLevelFlag


            sav_premium(session, permium_dict)
            #
            if chose_flag == "1":
                soupDb(SY, [getlatedate(1) + ' 00:00:00', getlatedate(365) + " 23:59:59", vehicle['seatCountBC'],
                            insureTypeGroupId, insureCarId, "14"])
                send_mq(client, CPlateNo, "", "1", "14", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
                log.info(u"信达入库成功:%s|%s" % (CPlateNo, searchVin))
                return
            elif chose_flag == "3":
                # 交强险加商业险 入库返回
                SY[0]['compulsory_insurance'] = JQ['compulsory_insurance']
                SY[0]['NAggTax'] = JQ['NAggTax']
                SY[3]['jq_disCount'] = JQ['jq_disCount']
                log.info(SY)
                soupDb(SY, [getlatedate(1) + ' 00:00:00', getlatedate(365) + " 23:59:59", vehicle['seatCountBC'],
                            insureTypeGroupId, insureCarId, "14"])
                send_mq(client, CPlateNo, "", "1", "14", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
                log.info(u"信达入库成功:%s|%s" % (CPlateNo, searchVin))

    except Exception as e:
        import traceback
        log.error(traceback.format_exc())
        log.error(e)
        send_mq(client, CPlateNo, "未知异常 %s " % e, "2", "14", sessionId, isPhone, insureTypeGroupId, insuranceTypeGroup)
        return 0


if __name__ == "__main__":
    name = {
        'insureCarId': 3797,
        'firstRegister': '2008-08-01',
        'cityCode': '32010000',
        'vinNo': 'LZFE18M186D009905',
        'plateNumber': '苏A55431',
        'insuranceTime': {
            'msg': '',
            'syStart': '2017-06-27',
            'jqStart': '2017-06-27',
            'code': '1000'
        },
        'vehicleBrand': '丰田SCT6490',
        'client': '',
        'custName': '韩军',
        'insuranceType': {
            'driverDutyPremium': {
                'Amount': '10000',
                'isCheck': '0'
            },
            'carDamagePremium': '1',
            'otherHurtBenchMarkPremium': '1',
            'passengerBenchMarkPremium': '0',
            'compulsoryInsurance': '1',
            'carFirePremium': '0',
            'otherHurtPremium': {
                'Amount': '1000000',
                'isCheck': '1'
            },
            'repairFactoryPremium': {
                'rate': '',
                'isCheck': '0'
            },
            'engineWadingBenchMarkPremium': '0',
            'insuranceTypeGroupId': '1541',
            'glassBrokenPremium': '0',
            'nAggTax': '1',
            'carDamageBenchMarkPremium': '1',
            'passengerDutyPremium': {
                'Amount': '10000',
                'isCheck': '0'
            },
            'driverDutyBenchMarkPremium': '0',
            'carTheftBenchMarkPremium': '0',
            'carNickPremium': {
                'Amount': '',
                'isCheck': '0'
            },
            'insuranceTypeGroup': '1_12_2_20_3_30_5_50_6_60',
            'carFireBrokenBenchMarkPremium': '0',
            'carNickBenchMarkPremium': '0',
            'engineWadingPremium': '0',
            'carTheftPremium': '0'
        },
        'sessionId': 'sessionId',
        'engineNo': '50607090559',
        'NSeatNum': '8',
        'identitCard': '02000635',
        'endDate': '2017-06-18',
        'isPhone': '1',
        'licenseType': '02'
    }
    xd_request_premium(name)
