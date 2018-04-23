# coding:utf8
import base64, re
import requests
from  common.timeUtil import getlatedate
from common.dama.damaUtil import dama
from request_xinda.settings import HEADERS_XINDA, CAR_INFO_DATA, BEFORE_YZM_DATA
import sys
from common.timeUtil import compare_date, getlatedate
from common.log import Logger
from request_xinda.xd_parse import parse_vin_car, parse_vehicle_info, parse_first_html, parse_xd_RulesBI, \
    xd_parse_premuim, xd_parse_jq_premuim, xd_parse_actualValue, xd_parse_tmp_no, xd_parse_riskLevelFlag, xd_parse_no
import datetime
from xd_tmp_body.first import xd_get_first_body
import traceback
from request_huanong.hn_util import calc_user_years

reload(sys)
sys.setdefaultencoding('utf8')
log = Logger()


# 获取车型代码
def get_car_vin(licenseNoBC, FrameNo, session):
    url = "http://10.75.1.10:8001/prpall/commoncar/pub/UIModelCodeQueryListBCFGFromVIN.jsp"
    "licenseNoBC=%E8%8B%8FE68K6S&frameNoBC=LSVE349F6A2644102&enrollDateBC=&ComCode=03120000&RiskCode=0500"
    str_data = {"licenseNoBC": licenseNoBC, "frameNoBC": FrameNo, "enrollDateBC": "", "ComCode": "03120000",
                "RiskCode": "0500"}
    ret = session.get(url, headers=HEADERS_XINDA, params=str_data)

    return ret.text


# 获取验证码之前调用
def before_yzm(licenseNoBC, FrameNo, session):
    try:
        url = "http://10.75.1.10:8001/prpall/commoncar/pub/UICarInfoQueryCheckPlatFormJS.jsp"

        data = BEFORE_YZM_DATA.format(LicenseNo=licenseNoBC, FrameNo=FrameNo)

        ret = session.post(url, headers=HEADERS_XINDA, data=data)
        CheckNoJS = re.findall(re.compile("parent.fraInterface.fm.checkNoJS.value = '(.+?)';"), ret.text)[0]
        log.info("xinda CheckNoJS %s", CheckNoJS)
        return CheckNoJS
    except Exception as e:
        log.error(e)


# 获取验证码
def get_yzm(session):
    url = "http://10.75.1.10:8001/prpall/CreateImage.jsp?"
    ret = session.get(url, headers=HEADERS_XINDA)

    YZM_CODE = dama("3", base64.b64encode(ret.content))

    return YZM_CODE


# 获取车辆信息
def get_car_info(LicenseNo, FrameNo, session):
    # 获取checkNo
    CheckNoJS = before_yzm(LicenseNo, FrameNo, session)
    # 调用失败重发一次
    if CheckNoJS is None:
        CheckNoJS = before_yzm(LicenseNo, FrameNo)
    ## 获取验证码
    YZM_CODE = get_yzm(session)
    str_data = {"ComCode": "03120000",
                "CheckNoJS": CheckNoJS, "CheckCodeJS": YZM_CODE, "FrameNo": FrameNo, "LicenseNo": LicenseNo
                }
    url = "http://10.75.1.10:8001/prpall/commoncar/pub/UICarInfoQueryConfirmPlatFormJS.jsp"

    ret = session.post(url, headers=HEADERS_XINDA, params=str_data)
    html = ret.text
    if "交管车辆信息查询成功" in html:
        dct = parse_vehicle_info(html)
        if isinstance(dct, dict):
            dct['CheckNoJS'] = CheckNoJS
            dct['CheckCodeJS'] = YZM_CODE
            return dct
    if "未查到" in html:
        log.info("%s通过车架号未查询车管所信息" % LicenseNo)
        return "%s通过车架号未查询车管所信息" % LicenseNo
    count = 1
    while "有误" in html and count < 5:
        return get_car_info(LicenseNo, FrameNo, session)


# 车价查询
def get_car_value(permium_dict, session, startBI=None):
    vehicle = permium_dict['vehicle']
    carVinInfo = permium_dict['carVinInfo']
    url = "http://10.75.1.10:8001/prpall/commoncar/pub/UIModelCodeQueryListPlatFormFG.jsp"
    carKindCodeBC = carVinInfo['carKindCodeBC']  # 车辆种类
    carTypeCodeBC = vehicle['carTypeCodeBC']  # 车辆类型
    licenseCategoryBC = vehicle['licenseCategoryBC']
    if carKindCodeBC == "G0":  # 挂车
        licenseCategoryBC = "B11"
    elif carKindCodeBC == "H1":
        licenseCategoryBC = "H51"
    elif carKindCodeBC == "H2":
        licenseCategoryBC = "N11"
    elif carKindCodeBC == "N0":
        licenseCategoryBC = "N21"
    elif carKindCodeBC in "TP,TQ,TR":  # 特一
        licenseCategoryBC = "Z71"
    elif carKindCodeBC == "TO3":  # 特三
        licenseCategoryBC = "X99"
    elif carKindCodeBC in "T1,T10,T11,T12,T3,T7,TD,TE,TG,TH,TK,TL,TN,TS":  # 特二
        if carKindCodeBC in "T1,T3,TE,TG,TH,TL":
            licenseCategoryBC = "Z11"
        else:
            licenseCategoryBC = "Z21"
    elif carKindCodeBC == "T2":
        licenseCategoryBC = "J11"
    elif carKindCodeBC == "TF":
        licenseCategoryBC = "J12"
    elif carKindCodeBC == "H3" and carTypeCodeBC == "6":
        licenseCategoryBC = "H32"  # 2吨以下
    elif carKindCodeBC == "H3" and (carTypeCodeBC == "7" or carTypeCodeBC == "8"):
        licenseCategoryBC = "H22"
    elif carKindCodeBC == "H3" and carTypeCodeBC == "9":  # {//货车+特四
        licenseCategoryBC = "H12"  # //10吨以上
    elif carKindCodeBC == "H6" and carTypeCodeBC == "6":  # ){//货车+特四
        licenseCategoryBC = "H37"  # ;//2吨以下
    elif carKindCodeBC == "H6" and (carTypeCodeBC == "7" or carTypeCodeBC == "8"):  # )){//货车+特四
        licenseCategoryBC = "H27"  # ;//2-10吨
    elif carKindCodeBC == "H6" and carTypeCodeBC == "9":
        licenseCategoryBC = "H17"  # ;//10吨以上
    elif carTypeCodeBC == "6" and carKindCodeBC in "H7,H8,H0,H4":
        licenseCategoryBC = "H31";  # //2吨以下
    elif carKindCodeBC in "H7,H8,H0,H4" and (carTypeCodeBC == "7" or carTypeCodeBC == "8"):  # ){//货车+特四
        licenseCategoryBC = "H21"  # ;//2-10吨
    elif carKindCodeBC in "H7,H8,H0,H4" and carTypeCodeBC == "9":  # {//货车+特四
        licenseCategoryBC = "H11"  # ;//10吨以上
    elif carKindCodeBC in "H5,TT":  # 货车+特四
        licenseCategoryBC = "Q11"

    #permium_dict['vehicle']['licenseCategoryBC'] = licenseCategoryBC
    useNatureCodeBC = permium_dict['carVinInfo']['useNatureCodeBC']
    if startBI is None:
        startBI = getlatedate(1)
    try:
        str_data = {
            'startHourBI': str(int(datetime.datetime.now().strftime("%H")) + 1),
            'VEHICLEMODEL': vehicle['vehicle_modelCI'],
            'BusinessNature': '0',
            'BrandName': carVinInfo['brandNameBC'],
            'MainCarKindCode': carVinInfo['mainCarKindCodeBC'],
            'vehicleBrand': '',
            'MadeFactory': vehicle['madeFactoryBI'],
            'seatCountBC': vehicle['seatCountBC'],
            'tonCountBC': vehicle['tonCountBC'],
            'LicenseKindCode': vehicle['licenseKindCodeBC'],
            'CompleteKerbMassNew': vehicle['completeKerbMassNewBC'],
            'EnrollDate': vehicle['enrollDateBC'],
            'AgentCode': '',
            'MakeDate': '',
            'immeValidFlagBI': 'false',
            'LicenseNo': vehicle['licenseNoBC'],
            'ExhaustScale': vehicle['exhaustScaleBC'],
            'FrameNo': vehicle['frameNoBC'],
            'startDateBI': startBI,
            'businessNatureFlag': 'FG',
            'enrollDateBC': vehicle['enrollDateBC'],
            'EngineNo': vehicle['EngineNo'],
            'useNatureCodeBC': useNatureCodeBC,
            'immeValidStartDateBI': getlatedate(-1),
            'LicenseCategory': licenseCategoryBC,
            'VINNo': '',
            'carKindCodeBC': carVinInfo['carKindCodeBC'],
            'BrandCode': carVinInfo['BrandCode'],
            'purchasePriceBC': carVinInfo['compromisePrice'],
            'clauseTypeBI': 'F54',
            'SeatCount': vehicle['seatCountBC'],
            'ComCode': '03120000',
            'currentDate': getlatedate(0)
        }
        ret = session.post(url, headers=HEADERS_XINDA, params=str_data)
        out = xd_parse_actualValue(ret.text)
        return out
    except Exception as e:
        log.error(e)
        log.error(u"车辆实际价值获取失败")
        return "车辆实际价值获取失败"


# 获取用户出险情况 计算保费的倒第四个请求
def get_InputSubmitBI(session, permium_dict):
    url = "http://10.75.1.10:8001/prpall/commoncar/pub/UIPrPoEnDemandInputSubmitBI.jsp"
    data = xd_get_first_body(permium_dict)
    ret = session.post(url, headers=HEADERS_XINDA, data=data)
    html = ret.text
    if "重复投保" in html:
        errmsg = re.findall(re.compile('errorMessage\((.+?)\)'), html)[0]
        if "终保日期" in html:
            str1 = u"终保日期:\d{4}\d{2}\d{2}"
            datelist = re.findall(str1, errmsg, re.S)
            if len(datelist) != 0:
                endDate = datelist[0].split(":")[1]
                endDate = endDate[0:4] + "-" + endDate[4:6] + "-" + endDate[6:]
                permium_dict['sy_insuranceEndTime'] = endDate
                # 重新计算车辆价值
                # 获取车辆实际价格以及纯风险保费

                try:
                    log.info("重复投保 重新获取车辆价值以及纯风险保费")
                    actualValue = get_car_value(permium_dict, session, endDate)
                    permium_dict['actualValue'] = actualValue
                    userYear = calc_user_years(endDate, permium_dict['vehicle']['enrollDateBC'])
                    permium_dict['actualValue']['useYears'] = userYear
                except Exception as e:

                    log.error(e)

                return get_InputSubmitBI(session, permium_dict)
        else:
            return errmsg
    return parse_first_html(html)


def get_ValidateRulesBI(session, permium_dict):
    try:
        url = "http://10.75.1.10:8001/prpall/0500/tbcbpg/UIPrPoEn0500QueryValidateRulesBI.jsp?isAssociateCI=1"
        data = xd_get_first_body(permium_dict)
        ret = session.post(url, headers=HEADERS_XINDA, data=data)
        html = ret.text
        permium_d = parse_xd_RulesBI(html)
        return permium_d
    except Exception as e:
        log.error(traceback.format_exc())
        log.error(e)
        return "parse_xd_RulesBI Error"


# 获取保费
def get_premium_data(session, permium_dict):
    url = "http://10.75.1.10:8001/prpall/0500/tbcbpg/UIPrPoEn0500PremiumCaculateFG.jsp?caculateFlagBI=1&caculateFlagCI=0"
    data = xd_get_first_body(permium_dict)
    ret = session.post(url, headers=HEADERS_XINDA, data=data)

    return xd_parse_premuim(ret.text, permium_dict)


def get_jq_data(session, permium_dict):
    url = 'http://10.75.1.10:8001/prpall/commoncar/pub/UIPrPoEnDemandInputSubmitCI.jsp'
    data = xd_get_first_body(permium_dict)
    ret = session.post(url, headers=HEADERS_XINDA, data=data)
    if '重复投保' in ret.text and '终保日期' in ret.text:
        # str1 = "\d{4}-\d{2}-\d{2}"
        datelist = re.findall('\d{4}-\d{2}-\d{2}', ret.text, re.S)
        if len(datelist) == 2:
            bigdate = compare_date(datelist[0], datelist[1])
            bigdate = compare_date(bigdate, getlatedate(0))
            permium_dict['jq_insuranceEndTime'] = bigdate
            return get_jq_data(session, permium_dict)

        elif len(datelist) == 3:
            bigdate = compare_date(datelist[0], datelist[1])
            bigdate = compare_date(bigdate, datelist[2])
            bigdate = compare_date(bigdate, getlatedate(0))
            permium_dict['jq_insuranceEndTime'] = bigdate
            return get_jq_data(session, permium_dict)

        else:
            log.error("交强险重复投保")
            return "重复投保"
    JQ = xd_parse_jq_premuim(ret.text)
    permium_dict['query_sequence_noCI'] = JQ['query_sequence_noCI']
    log.info(JQ)
    return JQ


# 请求进行暂存
def get_save_tmp_premium(session, premium_idct):
    url = "http://10.75.1.10:8001/prpall/0500/tbcbpg/UIPrPoEn0500TempSave.jsp"
    data = xd_get_first_body(premium_idct)
    ret = session.post(url, headers=HEADERS_XINDA, data=data)

    return xd_parse_tmp_no(ret.text)


# 获取theform.riskLevelFlag.value="C-营业普通货车【5-10）";
def get_riskLevelFlag(session, premium_dict):
    url = "http://10.75.1.10:8001/prpall/commoncar/pub/UIGetCustomerTypeValueNew.jsp?CustomerTypeFlag=YES"
    data = xd_get_first_body(premium_dict)
    ret = session.post(url, headers=HEADERS_XINDA, data=data)

    return xd_parse_riskLevelFlag(ret.text)


# 保存保单号
def sav_premium(session, premium_idct):
    url = "http://10.75.1.10:8001/prpall/0500/tbcbpg/UIPrPoEn0500Save.jsp"
    data = xd_get_first_body(premium_idct)
    ret = session.post(url, headers=HEADERS_XINDA, data=data)

    return xd_parse_no(ret.text)


# 提交核保
def submit_CIBI(session, premium_idct):
    url = "http://10.75.1.10:8001/prpall/0500/tbcb/UIPrpslPoli0500UnderwriteSubmit.jsp?ManualUnderWriteFlag=N&proposalNoCI=T170312000507004742&proposalNoBI=T170312000518004819"
    # data = xd_get_first_body(premium_idct)
    ret = session.post(url, headers=HEADERS_XINDA, data="")
