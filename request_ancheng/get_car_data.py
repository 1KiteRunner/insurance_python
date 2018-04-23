# coding:utf8

import json
import re
import traceback

import time
import urllib

import sys
from bs4 import BeautifulSoup

from common.dama.damaUtil import dama
from common.log import Logger
from common.redisUtil import CRedis
from request_ancheng.get_car_type import get_car_class
from request_ancheng.get_use_year import get_user_years, codeMap, PHCC_VHL_USEYEAR_MAP, JQ_PHCC_VHL_USEYEAR_MAP
from request_ancheng.login import login_ancheng
from request_ancheng.request_body import _damage_insurance_namt_20, _third_party_insurance_15, \
    _driver_liability_insurance_13, _pass_liability_insurance_14, _theft_insurance_namt_18, \
    _autoignition_insurance_namt_5, _crush_insurance_namt_8, _wade_insurance_namt_10, _scratch_insurance_namt_19
from request_ancheng.request_data import get_car_id, get_car_info, query_car, query_car_model, get_vehcle_code

from request_ancheng.template import get_dw
from request_ancheng.util import city_map, city_map_2
from request_cic import utils

reload(sys)
sys.setdefaultencoding('utf-8')
log = Logger()


# 获取协商价格
def get_Vhl_NNewPurchaseValue(insrncBgnTm, fstRegTm, nMonDespRate, NResvNum2):
    months = int(insrncBgnTm[:4]) - int(fstRegTm[:4])
    months *= 12
    months += (int(insrncBgnTm[5:7]) - int(fstRegTm[5:7]))

    if int(fstRegTm[8:10]) > int(insrncBgnTm[8:10]):
        months -= 1

    rate = (1 - int(months) * float(nMonDespRate))
    rate = 0.2 if rate < 0.2 else rate
    Vhl_NNewPurchaseValue = int(NResvNum2) * rate

    Vhl_NNewPurchaseValue = round(Vhl_NNewPurchaseValue, 2)

    return Vhl_NNewPurchaseValue


# 根据车牌号和车架号获取PLAT_ID
def get_car(session, CPlateNo, searchVin):
    ret = get_car_id(session, CPlateNo, searchVin)

    response_body = json.loads(ret.content)

    id = response_body["RESULT_MSG"]

    PLAT_ID = id[:30]
    code = id[36:]
    # YZM_CODE = pic2Str(base64.b64decode(code))
    YZM_CODE = dama("3", code)  # 老王打码
    ret = get_car_info(session, PLAT_ID, YZM_CODE)

    return ret


# 查询车辆信息
def query_car_info(session, data, syStart, CPlateNo, searchVin):
    try:
        ret = query_car(session, CPlateNo, searchVin)

        if '车辆识别失败' in ret.text or not ret.text:

            # 交管车型查询
            try:
                result = None
                for i in range(5):
                    result = get_car(session, CPlateNo, searchVin)
                    if '录入的校验码有误' not in result.text:
                        break
                    if i == 4 and '录入的校验码有误' in result.text:
                        log.info('验证码5次识别失败')
                        return 0

                if '交管车辆查询校验信息不存在' in result.text:
                    log.info('{0},{1} - 交管车辆查询校验信息不存在'.format(CPlateNo, searchVin))
                    return 0

                ra = "DATA:\['(.*?)'\]"
                rb = re.compile(ra)

                title_list = re.findall(rb, result.text)
                if not title_list:
                    log.info('{0},{1} - 交管车辆查询校验信息不存在'.format(CPlateNo, searchVin))
                    return 0
                html = title_list[0]
                soup = BeautifulSoup(html, 'html.parser')
                a = soup.find('dataobj', attrs={"status": "UNCHANGED"})
                soup = BeautifulSoup(str(a), 'html.parser')
            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
                return 0

            VEHICLE_MODEL = soup.find("attribute", attrs={"name": "VEHICLE_MODEL"}).get_text()  # 车辆型号

            VEHICLE_MODEL = VEHICLE_MODEL[:-1] + VEHICLE_MODEL[-1:].lower()

            ret = query_car_model(session, VEHICLE_MODEL)

            if '车辆识别失败' in ret.text or not ret.text:
                log.info(u'{0},{1} - 车辆识别失败'.format(CPlateNo, searchVin))
                return 0

        ra = "DATA:\['(.*?)'\]"
        rb = re.compile(ra)

        title_list = re.findall(rb, ret.text)
        if not title_list:
            session = login_ancheng()
            from request_ancheng.request_premium import get_premium
            return get_premium(session, data)

        html = title_list[0]
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('dataobj', attrs={"status": "UNCHANGED"})
        a = list(a)

        c = sorted(a, key=lambda x: int(
            BeautifulSoup(str(x), 'html.parser').find("attribute", attrs={"name": "VehiclePrice"}).get_text()),
                   reverse=False)

        if not c:
            return 0

        d = c[0]
        car_value = int(
            BeautifulSoup(str(d), 'html.parser').find("attribute", attrs={"name": "VehiclePrice"}).get_text())
        log.info(u'车辆价格 - {0}'.format(car_value))

        soup = BeautifulSoup(str(d), 'html.parser')
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0

    Vhl_CBrandNme = soup.find("attribute", attrs={"name": "BrandName"}).get_text()  # 品牌
    Cmodel_Code = soup.find("attribute", attrs={"name": "VehicleId"}).get_text()[:10]  # PK

    log.info(u'车型编码 - {0}'.format(Cmodel_Code))

    Vhl_NResvNum2 = soup.find("attribute", attrs={"name": "VehiclePrice"}).get_text()  # 车辆价格
    Vhl_CProdPlace = soup.find("attribute", attrs={"name": "VehicleType"}).get_text()  # 种类
    NewVehicleClass = soup.find("attribute", attrs={"name": "NewVehicleClass"}).get_text()  # 车辆种类 牵引车 等
    seat_01 = int(soup.find("attribute", attrs={"name": "VehicleSeat"}).get_text())  # 座位数
    Vhl_CModelNme = soup.find("attribute", attrs={"name": "VehicleName"}).get_text()  # 车型名称

    Vhl_CGroupNme = soup.find("attribute", attrs={"name": "GroupName"}).get_text()  # 车组名称

    code = unicode(CPlateNo)[1]

    Base_CAreaFlag = city_map.get(code, '320100')
    Base_CCountyCde = city_map_2.get(code, '320101')

    Vhl_CProdPlace = "0" if Vhl_CProdPlace == "国产" else "1"

    try:
        ret = get_vehcle_code(session, Cmodel_Code)

        ra = "###(.+?)###"
        rb = re.compile(ra)

        Vehcle_Code = re.findall(rb, ret.text)[0]

        if Vehcle_Code == 'null':
            log.info(u'无法获取行业车型编码')
            return 0

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0

    # 交管车型查询
    try:
        result = None
        for i in range(5):
            result = get_car(session, CPlateNo, searchVin)
            if not '录入的校验码有误' in result.text:
                break
            if i == 4 and '录入的校验码有误' in result.text:
                log.info(u'验证码5次识别失败')
                return 0

        if '交管车辆查询校验信息不存在' in result.text:
            log.info(u'{0},{1} - 交管车辆查询校验信息不存在'.format(CPlateNo, searchVin))
            return 0

        ra = "DATA:\['(.*?)'\]"
        rb = re.compile(ra)

        title_list = re.findall(rb, result.text)
        html = title_list[0]
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find('dataobj', attrs={"status": "UNCHANGED"})
        soup = BeautifulSoup(str(a), 'html.parser')
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0

    Applicant_CAppNme = soup.find("attribute", attrs={"name": "OWNER"}).get_text()  # 车主
    Insured_CInsuredNme = Applicant_CAppNme

    Applicant_CAppNme = unicode(Applicant_CAppNme)
    if len(Applicant_CAppNme) >= 5:
        Applicant_CAppNme = '测试单位'
        Applicant_CClntMrk = '3'
        Insured_CClntMrk = '3'
    else:
        Applicant_CAppNme = "测试个人"
        Applicant_CClntMrk = '1'
        Insured_CClntMrk = '1'

    Vhl_CFstRegYm = soup.find("attribute", attrs={"name": "VEHICLE_REGISTER_DATE"}).get_text()  # 初登日期
    Vhl_CRegVhlTyp = soup.find("attribute", attrs={"name": "VEHICLE_STYLE"}).get_text()  # 交管车辆种类
    LIMIT_LOAD_PERSON = soup.find("attribute", attrs={"name": "LIMIT_LOAD_PERSON"}).get_text()  # 座位数
    DISPLACEMENT = soup.find("attribute", attrs={"name": "DISPLACEMENT"}).get_text()  # 排量
    VEHICLE_TYPE = soup.find("attribute", attrs={"name": "VEHICLE_TYPE"}).get_text()  # 号牌种类 01 大型汽车 02 小型汽车 15 挂车
    SY_Vhl_TTransferDate = soup.find("attribute", attrs={"name": "TRANSFER_DATE"}).get_text()  # 过户日期
    PM_USE_TYPE = soup.find("attribute", attrs={"name": "PM_USE_TYPE"}).get_text()  # 使用性质 F商业 A家用
    VEHICLE_STYLE = soup.find("attribute", attrs={"name": "VEHICLE_STYLE"}).get_text()  # 车辆类型 K31 K33 、Q11货车
    HAULAGE = soup.find("attribute", attrs={"name": "HAULAGE"}).get_text()  # 牵引质量 牵引车
    LIMIT_LOAD = soup.find("attribute", attrs={"name": "LIMIT_LOAD"}).get_text()  # 核定载质量
    VEHICLE_CATEGORY = soup.find("attribute", attrs={"name": "VEHICLE_CATEGORY"}).get_text()  # 平台车辆种类(编码)
    Vhl_NPoWeight = soup.find("attribute", attrs={"name": "WHOLE_WEIGHT"}).get_text()  # 整备质量

    SY_Vhl_CVhlTransFlag = '0'
    JQ_Vhl_CVhlTransFlag = '0'

    if SY_Vhl_TTransferDate:
        SY_Vhl_CVhlTransFlag = '1'
        JQ_Vhl_CVhlTransFlag = '1'

    DISPLACEMENT = float(DISPLACEMENT) / 1000

    Vhl_NDisplacement = str(DISPLACEMENT)  # 排量

    WHOLE_WEIGHT = float(soup.find("attribute", attrs={"name": "WHOLE_WEIGHT"}).get_text())
    WHOLE_WEIGHT = float(WHOLE_WEIGHT) / 1000

    VsTax_NCurbWt = str(WHOLE_WEIGHT)  # 整备质量

    seats = int(LIMIT_LOAD_PERSON)
    # 车管所查询出的座位数为0 使用车辆信息中的座位数
    if seat_01 != "" and LIMIT_LOAD_PERSON == "0":
        seats = int(seat_01)

    Vhl_CFstRegYm = Vhl_CFstRegYm[:4] + '-' + Vhl_CFstRegYm[4:6] + '-' + Vhl_CFstRegYm[6:]
    Vhl_CEngNo = soup.find("attribute", attrs={"name": "ENGINE_NO"}).get_text()  # 发动机号

    _VEHICLE_REGISTER_DATE = soup.find("attribute", attrs={"name": "VEHICLE_REGISTER_DATE"}).get_text()  # 车辆注册时间
    VEHICLE_REGISTER_DATE = _VEHICLE_REGISTER_DATE[:4] + '-' + _VEHICLE_REGISTER_DATE[
                                                               4:6] + '-' + _VEHICLE_REGISTER_DATE[6:]

    car_info = {}

    car_info['Vhl_CBrandNme'] = Vhl_CBrandNme
    car_info['Vhl_NResvNum2'] = Vhl_NResvNum2
    car_info['Vhl_CProdPlace'] = Vhl_CProdPlace
    car_info['Applicant_CAppNme'] = Applicant_CAppNme
    car_info['Vhl_CFstRegYm'] = Vhl_CFstRegYm
    car_info['Vhl_CRegVhlTyp'] = Vhl_CRegVhlTyp
    car_info['seats'] = seats
    car_info['Vhl_CEngNo'] = Vhl_CEngNo
    car_info['VEHICLE_REGISTER_DATE'] = VEHICLE_REGISTER_DATE
    car_info['Vehcle_Code'] = Vehcle_Code
    car_info['Cmodel_Code'] = Cmodel_Code
    car_info['Vhl_NDisplacement'] = Vhl_NDisplacement
    car_info['VsTax_NCurbWt'] = VsTax_NCurbWt
    car_info['VEHICLE_TYPE'] = VEHICLE_TYPE
    car_info['VEHICLE_CATEGORY'] = VEHICLE_CATEGORY
    car_info['PM_USE_TYPE'] = PM_USE_TYPE
    car_info['VEHICLE_STYLE'] = VEHICLE_STYLE
    car_info['HAULAGE'] = HAULAGE
    car_info['LIMIT_LOAD'] = LIMIT_LOAD
    car_info['SY_Vhl_CVhlTransFlag'] = SY_Vhl_CVhlTransFlag
    car_info['JQ_Vhl_CVhlTransFlag'] = JQ_Vhl_CVhlTransFlag
    car_info['SY_Vhl_TTransferDate'] = SY_Vhl_TTransferDate
    car_info['NewVehicleClass'] = NewVehicleClass
    car_info['Vhl_CModelNme'] = Vhl_CModelNme
    car_info['CPlateNo'] = CPlateNo
    car_info['Vhl_CGroupNme'] = Vhl_CGroupNme
    car_info['Insured_CInsuredNme'] = Insured_CInsuredNme
    car_info['Vhl_NPoWeight'] = Vhl_NPoWeight

    car_info['Base_CAreaFlag'] = Base_CAreaFlag
    car_info['Base_CCountyCde'] = Base_CCountyCde
    car_info['Applicant_CClntMrk'] = Applicant_CClntMrk
    car_info['Insured_CClntMrk'] = Insured_CClntMrk

    car_class_dict = get_car_class(car_info)
    if not car_class_dict:
        return None

    car_info['SY_Vhl_CBizMrk'] = car_class_dict['SY_Vhl_CBizMrk']
    car_info['JQ_Vhl_CBizMrk'] = car_class_dict['JQ_Vhl_CBizMrk']
    car_info['SY_Vhl_CUsageCde'] = car_class_dict['SY_Vhl_CUsageCde']
    car_info['JQ_Vhl_CUsageCde'] = car_class_dict['JQ_Vhl_CUsageCde']
    car_info['SY_Vhl_CVhlTyp'] = car_class_dict['SY_Vhl_CVhlTyp']
    car_info['JQ_Vhl_CVhlTyp'] = car_class_dict['JQ_Vhl_CVhlTyp']
    car_info['Vhl_NTonage'] = car_class_dict['Vhl_NTonage']
    car_info['is_tezhongche'] = car_class_dict['is_tezhongche']
    car_info['is_guache'] = car_class_dict['is_guache']
    car_info['SY_Vhl_CMonDespRate'] = car_class_dict['SY_Vhl_CMonDespRate']

    # 查询保额
    Vhl_NNewPurchaseValue = get_Vhl_NNewPurchaseValue(syStart, Vhl_CFstRegYm, car_class_dict['SY_Vhl_CMonDespRate'],
                                                      Vhl_NResvNum2)

    log.info('保额 - {0}'.format(Vhl_NNewPurchaseValue))

    car_info['Vhl_NNewPurchaseValue'] = Vhl_NNewPurchaseValue
    r = CRedis()
    r.set_vin(searchVin, "12", json.dumps(car_info, ensure_ascii=False))

    return car_info


# 总请求
def get_premium_request(session, jqStart, syStart, CPlateNo, searchVin, insuranceType, car_info,
                        PrmCoef_NExpectTotal='0', CAppNo='', hebao_premium={}):
    Applicant_CAppNme = car_info.get('Applicant_CAppNme', '')
    Insured_CInsuredNme = car_info.get('Insured_CInsuredNme', '')
    seats = car_info.get('seats', '')
    Vhl_CEngNo = car_info.get('Vhl_CEngNo', '')
    Vhl_CFstRegYm = car_info.get('Vhl_CFstRegYm', '')
    Vhl_CRegVhlTyp = car_info.get('Vhl_CRegVhlTyp', '')
    Vhl_CProdPlace = car_info.get('Vhl_CProdPlace', '')
    Vhl_CBrandNme = car_info.get('Vhl_CBrandNme', '')
    VEHICLE_REGISTER_DATE = car_info.get('VEHICLE_REGISTER_DATE', '')
    Vhl_NResvNum2 = car_info.get('Vhl_NResvNum2', '')
    Vehcle_Code = car_info.get('Vehcle_Code', '')
    Cmodel_Code = car_info.get('Cmodel_Code', '')
    Vhl_NDisplacement = car_info.get('Vhl_NDisplacement', '')
    VsTax_NCurbWt = car_info.get('VsTax_NCurbWt', '')
    SY_Vhl_CMonDespRate = car_info.get('SY_Vhl_CMonDespRate', '')
    Vhl_NNewPurchaseValue = car_info.get('Vhl_NNewPurchaseValue', '')
    Vhl_CModelNme = car_info.get('Vhl_CModelNme', '')
    Vhl_NPoWeight = car_info.get('Vhl_NPoWeight', '')

    NewVehicleClass = car_info.get('NewVehicleClass', '')
    Vhl_CGroupNme = car_info.get('Vhl_CGroupNme', '')

    Base_CAreaFlag = car_info['Base_CAreaFlag']
    Base_CCountyCde = car_info['Base_CCountyCde']
    Applicant_CClntMrk = car_info['Applicant_CClntMrk']
    Insured_CClntMrk = car_info['Insured_CClntMrk']

    SY_Vhl_CVhlTransFlag = car_info.get('SY_Vhl_CVhlTransFlag', '')  # 商 车辆过户
    JQ_Vhl_CVhlTransFlag = car_info.get('JQ_Vhl_CVhlTransFlag', '')  # 交 车辆过户
    SY_Vhl_TTransferDate = car_info.get('SY_Vhl_TTransferDate', '')  # 过户日期
    SY_Vhl_TTransferDate = SY_Vhl_TTransferDate[:4] + '-' + SY_Vhl_TTransferDate[4:6] + '-' + SY_Vhl_TTransferDate[6:8]

    Vhl_CPlateTyp = car_info.get("VEHICLE_TYPE", "02")  # 号牌种类 01 大型汽车 02 小型汽车 15 挂车
    Applicant_CAppNme = Insured_CInsuredNme
    Applicant_CCertfCls = "123007"
    Applicant_CCertfCde = "510130197608144113"
    Applicant_CResvTxt12 = "1"
    Applicant_CClntAddr = "中国四川省成都市成华区保和乡东升村10组29号附1号"
    Applicant_CMobile = "13981876776"

    Insured_CInsuredNme = Applicant_CAppNme
    Insured_CCertfCls = Applicant_CCertfCls
    Insured_CCertfCde = Applicant_CCertfCde
    Insured_CResvTxt12 = Applicant_CResvTxt12
    Insured_CClntAddr = Applicant_CClntAddr
    Insured_CMobile = Applicant_CMobile

    Vhlowner_COwnerNme = Applicant_CAppNme
    Vhlowner_CCertfCls = Applicant_CCertfCls
    Vhlowner_CCertfCde = Applicant_CCertfCde

    Base_TAppTm = utils.getlatedate(0)  # （计算）投保日期
    Base_TIssueTm = utils.getlatedate(0)  # 签单日期

    SY_Base_TInsrncBgnTm = syStart + ' 00:00:00'  # 保险起止期(商)
    SY_Base_TInsrncEndTm = utils.getlatedate(364, syStart) + " 23:59:59"  # 保险起止期(商)
    JQ_Base_TInsrncBgnTm = jqStart + " 00:00:00"  # 保险起止期(交)
    JQ_Base_TInsrncEndTm = utils.getlatedate(364, jqStart) + " 23:59:59"  # 保险起止期(交)

    Base_TInsrncBgnTm = JQ_Base_TInsrncBgnTm if jqStart else SY_Base_TInsrncBgnTm
    Base_TInsrncEndTm = JQ_Base_TInsrncEndTm if jqStart else SY_Base_TInsrncEndTm

    log.info(u'保险开始时间 （商） - {0}'.format(SY_Base_TInsrncBgnTm))
    log.info(u'保险开始时间 （交） - {0}'.format(JQ_Base_TInsrncBgnTm))

    Base_CAreaFlag = Base_CAreaFlag  # 地区标识
    Base_CCountyCde = Base_CCountyCde  # 保单归属地
    Base_CVhlchanlFlag = "0"  # 车型渠道（固定）
    Base_CDisptSttlCde = "007001"  # 争议处理（固定）
    Base_CFinTyp = "002001"  # 缴费方式（固定）
    Base_CBsnsTyp = "19002"  # 业务来源（固定）
    Base_CChaType = "191008"  # 渠道中级（固定）
    Base_CChaSubtype = "19100801"  # 渠道子类（固定）
    Base_CSlsId = "132021610"  # 渠道维护员工号（固定）
    Base_CSlsNme = "田江平"  # 渠道维护员名称（固定）
    Base_CBrkrCde = "10000001502"  # 代理人（固定）
    Base_CAgtAgrNo = "B32201700075"  # 代理协议（固定）
    Base_NSubCoNo = "0"  # 补充协议号（固定）
    Base_CAgtSls = "32020203008033"  # 中介经办人（固定）
    Base_CTel = "13771615588"  # 联系电话（固定）
    Base_CRatioTyp = "1"  # 短期费率类型（固定）
    Base_CAgriMrk = "2"  # 涉农标志（固定）

    Vhl_CNewMrk = "0"  # 是否上牌（固定）'0 是 1 否'
    Vhl_CNewVhlFlag = "0"  # 是否新车（固定）'1 是 0 否'

    Vhl_CPlateTyp = Vhl_CPlateTyp  # 号牌种类（获取）
    Vhl_CPlateNo = CPlateNo  # 车牌号
    Vhl_CFrmNo = searchVin  # 车架号
    Vhl_CEngNo = Vhl_CEngNo  # 发动机号（获取）
    Vhl_CFstRegYm = Vhl_CFstRegYm  # 初登日期（获取）
    Vhl_CRegVhlTyp = Vhl_CRegVhlTyp  # 交管车辆种类（获取）
    Vhl_NNewPurchaseValue = Vhl_NNewPurchaseValue  # 协商价值（获取）
    Vhl_CProdPlace = Vhl_CProdPlace  # 国产/进口 国产-0 进口-1 （手动输入）
    SY_Vhl_CMonDespRate = SY_Vhl_CMonDespRate  # 折旧率（计算）
    Vhl_CBrandNme = Vhl_CBrandNme  # 品牌车型（获取）
    userYear = get_user_years(syStart, VEHICLE_REGISTER_DATE)  # 商 车龄（计算获取）345020003

    if searchVin[0].upper() == 'L':
        glassBrokenPremium = '303011001'  # 国产玻璃
    else:
        glassBrokenPremium = '303011002'  # 进口玻璃

    SY_Vhl_CUseYear = codeMap.get(userYear, '345020004')  # 商车龄
    SY_Vhl_CAddriskVhlAge = PHCC_VHL_USEYEAR_MAP.get(userYear, '345003010')

    JQ_Vhl_CUseYear = JQ_PHCC_VHL_USEYEAR_MAP.get(userYear, '345011005')  # 交 车龄
    SY_Vhl_CEcdemicMrk = "0"  # 商是否外地车（获取）本地车-0
    JQ_Vhl_CEcdemicMrk = "0"  # 交是否外地车（获取）本地车-0
    Vhl_NSeatNum = seats  # 座位数（获取）

    JQ_Vhl_CFuelType = "0"  # 交能源类型（燃油）

    Vhl_CProjCde = "A3201ZZ001"  # 项目代码 （固定）

    CDductMrk = "345021001"  # 不计免赔 是
    No_CDductMrk = "345021007"  # 不计免赔 否

    SY_Vhl_CBizMrk = car_info['SY_Vhl_CBizMrk']
    JQ_Vhl_CBizMrk = car_info['JQ_Vhl_CBizMrk']
    SY_Vhl_CUsageCde = car_info['SY_Vhl_CUsageCde']
    JQ_Vhl_CUsageCde = car_info['JQ_Vhl_CUsageCde']
    SY_Vhl_CVhlTyp = car_info['SY_Vhl_CVhlTyp']
    JQ_Vhl_CVhlTyp = car_info['JQ_Vhl_CVhlTyp']

    Vhl_NTonage = car_info['Vhl_NTonage']

    # 车船税
    VsTax_CPaytaxTyp = 'T'  # 纳税类型代码（固定）
    VsTax_CTaxdptVhltyp = '345030002'  # 行驶证车辆类型（固定）
    VsTax_TTaxEffBgnTm = time.strftime("%Y", time.localtime()) + '-01-01'  # 税款所属期始（获取）
    VsTax_TTaxEffEndTm = time.strftime("%Y", time.localtime()) + '-12-31'  # 税款所属期止（获取）
    VsTax_CTaxpayerComId = '370784197612165510'  # 纳税人识别号
    VsTax_CMotorvehFueltyp = 'A'  # 燃油种类

    is_tezhongche = int(car_info.get('is_tezhongche', 0))
    is_guache = int(car_info.get('is_guache', 0))

    _driverDutyPremium = insuranceType.get("driverDutyPremium", None)  # 驾驶人责任险 check
    _driverDutyBenchMarkPremium = CDductMrk if int(
        insuranceType.get("driverDutyBenchMarkPremium", "0")) else No_CDductMrk

    _carDamagePremium = insuranceType.get("carDamagePremium", "0")  # 车损险
    _carDamageBenchMarkPremium = CDductMrk if int(
        insuranceType.get("carDamageBenchMarkPremium", "0")) else No_CDductMrk

    _otherHurtPremium = insuranceType.get("otherHurtPremium", None)  # 机动车第三责任保险 check
    _otherHurtBenchMarkPremium = CDductMrk if int(
        insuranceType.get("otherHurtBenchMarkPremium", "0")) else No_CDductMrk

    _passengerDutyPremium = insuranceType.get("passengerDutyPremium", None)  # 乘客责任险 check
    _passengerBenchMarkPremium = CDductMrk if int(
        insuranceType.get("passengerBenchMarkPremium", "0")) else No_CDductMrk

    _carTheftPremium = insuranceType.get("carTheftPremium", "0")  # 盗抢险
    _carTheftBenchMarkPremium = CDductMrk if int(
        insuranceType.get("carTheftBenchMarkPremium", "0")) else No_CDductMrk

    _carFireBrokenBenchMarkPremium = insuranceType.get("carFirePremium", "0")  # 自燃险
    _carFireBrokenBenchMarkPremium22 = CDductMrk if int(
        insuranceType.get("carFireBrokenBenchMarkPremium", "0")) else No_CDductMrk

    _glassBrokenPremium = insuranceType.get("glassBrokenPremium", "0")  # 玻璃破碎险

    _engineWadingBenchMarkPremium = insuranceType.get("engineWadingPremium", "0")  # 涉水险
    _engineWadingBenchMarkPremium22 = CDductMrk if int(
        insuranceType.get("engineWadingBenchMarkPremium", "0")) else No_CDductMrk

    _carNickPremium = insuranceType.get("carNickPremium", None)  # 划痕险 check
    _carNickBenchMarkPremium = CDductMrk if int(insuranceType.get("carNickBenchMarkPremium", "0")) else No_CDductMrk

    # 删除车损险需删除其他险
    if not int(_carDamagePremium):
        _carFireBrokenBenchMarkPremium = '0'  # 自燃险
        _glassBrokenPremium = '0'  # 玻璃破碎险
        _carNickPremium['isCheck'] = '0'  # 划痕险
        _engineWadingBenchMarkPremium = '0'  # 涉水险

    # 根据所传的参数生成动态消息体
    damage_insurance_namt_20 = _damage_insurance_namt_20(Vhl_NNewPurchaseValue, _carDamageBenchMarkPremium,
                                                         SY_Base_TInsrncBgnTm, SY_Base_TInsrncEndTm,
                                                         CAppNo=CAppNo, hebao_premium=hebao_premium) if int(
        _carDamagePremium) else ''  # 机动车损失保险

    third_party_insurance_15 = _third_party_insurance_15(_otherHurtPremium, _otherHurtBenchMarkPremium,
                                                         SY_Base_TInsrncBgnTm,
                                                         SY_Base_TInsrncEndTm,
                                                         CAppNo=CAppNo,
                                                         hebao_premium=hebao_premium) if _otherHurtPremium and int(
        _otherHurtPremium.get("isCheck", 0)) else ''  # 第三者责任险

    driver_liability_insurance_13 = _driver_liability_insurance_13(_driverDutyPremium, _driverDutyBenchMarkPremium,
                                                                   SY_Base_TInsrncBgnTm,
                                                                   SY_Base_TInsrncEndTm,
                                                                   CAppNo=CAppNo,
                                                                   hebao_premium=hebao_premium) if _driverDutyPremium and int(
        _driverDutyPremium.get("isCheck", 0)) else ''  # 驾驶人责任险

    pass_liability_insurance_14 = _pass_liability_insurance_14(_passengerDutyPremium, seats,
                                                               _passengerBenchMarkPremium, SY_Base_TInsrncBgnTm,
                                                               SY_Base_TInsrncEndTm,
                                                               CAppNo=CAppNo,
                                                               hebao_premium=hebao_premium) if _passengerDutyPremium and int(
        _passengerDutyPremium.get("isCheck", 0)) else ''  # 乘客责任险

    theft_insurance_namt_18 = _theft_insurance_namt_18(Vhl_NNewPurchaseValue, _carTheftBenchMarkPremium,
                                                       SY_Base_TInsrncBgnTm, SY_Base_TInsrncEndTm,
                                                       CAppNo=CAppNo, hebao_premium=hebao_premium) if int(
        _carTheftPremium) else ''  # 盗抢险

    autoignition_insurance_namt_5 = _autoignition_insurance_namt_5(Vhl_NNewPurchaseValue,
                                                                   _carFireBrokenBenchMarkPremium22,
                                                                   SY_Base_TInsrncBgnTm,
                                                                   SY_Base_TInsrncEndTm, CAppNo=CAppNo,
                                                                   hebao_premium=hebao_premium) if int(
        _carFireBrokenBenchMarkPremium) else ''  # 自燃险

    crush_insurance_namt_8 = _crush_insurance_namt_8(Vhl_NResvNum2, SY_Base_TInsrncBgnTm,
                                                     SY_Base_TInsrncEndTm, glassBrokenPremium, CAppNo=CAppNo,
                                                     hebao_premium=hebao_premium) if int(
        _glassBrokenPremium) else ''  # 玻璃破碎险险

    wade_insurance_namt_10 = _wade_insurance_namt_10(Vhl_NNewPurchaseValue, _engineWadingBenchMarkPremium22,
                                                     SY_Base_TInsrncBgnTm, SY_Base_TInsrncEndTm, CAppNo=CAppNo,
                                                     hebao_premium=hebao_premium) if int(
        _engineWadingBenchMarkPremium) else ''  # 涉水险

    scratch_insurance_namt_19 = _scratch_insurance_namt_19(_carNickPremium, _carNickBenchMarkPremium,
                                                           SY_Base_TInsrncBgnTm,
                                                           SY_Base_TInsrncEndTm,
                                                           CAppNo=CAppNo,
                                                           hebao_premium=hebao_premium) if _carNickPremium and int(
        _carNickPremium.get("isCheck", 0)) else ''  # 划痕险

    if not scratch_insurance_namt_19 and not wade_insurance_namt_10 and not crush_insurance_namt_8 and not autoignition_insurance_namt_5 and not theft_insurance_namt_18 and not pass_liability_insurance_14 and not driver_liability_insurance_13 and not third_party_insurance_15 and not damage_insurance_namt_20:
        Base_CProdNo = '0330'

    elif not int(insuranceType.get("compulsoryInsurance", "0")) and not is_tezhongche:
        Base_CProdNo = '0336'

    elif not int(insuranceType.get("compulsoryInsurance", "0")) and is_tezhongche:
        Base_CProdNo = '0335'

    elif int(insuranceType.get("compulsoryInsurance", "0")) and is_tezhongche:
        Base_CProdNo = '0335_0330'

    else:
        Base_CProdNo = '0336_0330'

    if is_tezhongche:
        wade_insurance_namt_10 = ''
        scratch_insurance_namt_19 = ''
    if is_guache:
        driver_liability_insurance_13 = ''
        pass_liability_insurance_14 = ''
        wade_insurance_namt_10 = ''
        scratch_insurance_namt_19 = ''
        crush_insurance_namt_8 = ''

    log.info(Base_CProdNo)
    DW_DATA = get_dw(
        Applicant_CAppNme, Applicant_CCertfCls, Applicant_CCertfCde, Applicant_CResvTxt12, Applicant_CClntAddr,
        Applicant_CMobile, Insured_CInsuredNme, Insured_CCertfCls, Insured_CCertfCde, Insured_CResvTxt12,
        Insured_CClntAddr, Insured_CMobile, Vhlowner_COwnerNme, Vhlowner_CCertfCls, Vhlowner_CCertfCde, Base_TAppTm,
        SY_Base_TInsrncBgnTm, SY_Base_TInsrncEndTm, JQ_Base_TInsrncBgnTm, JQ_Base_TInsrncEndTm, Base_CAreaFlag,
        Base_CCountyCde, Base_CVhlchanlFlag, Base_CDisptSttlCde, Base_CFinTyp, Base_CBsnsTyp, Base_CChaType,
        Base_CChaSubtype, Base_CSlsId, Base_CSlsNme, Base_CBrkrCde, Base_CAgtAgrNo, Base_NSubCoNo, Base_CAgtSls,
        Base_CTel, Base_CRatioTyp, Base_CAgriMrk, SY_Vhl_CBizMrk, SY_Vhl_CUsageCde, SY_Vhl_CVhlTyp, JQ_Vhl_CBizMrk,
        JQ_Vhl_CUsageCde, JQ_Vhl_CVhlTyp, Vhl_CPlateTyp, Vhl_CPlateNo, Vhl_CFrmNo, Vhl_CEngNo, Vhl_CFstRegYm,
        Vhl_CRegVhlTyp, Vhl_NNewPurchaseValue, Vhl_CProdPlace, SY_Vhl_CMonDespRate, Vhl_CBrandNme, SY_Vhl_CUseYear,
        JQ_Vhl_CUseYear, SY_Vhl_CEcdemicMrk, JQ_Vhl_CEcdemicMrk, Vhl_NSeatNum, Vhl_NTonage, JQ_Vhl_CFuelType,
        Base_TIssueTm, Vhl_CNewMrk, Vhl_CNewVhlFlag, SY_Vhl_CVhlTransFlag, Vhl_CProjCde,
        damage_insurance_namt_20, third_party_insurance_15, driver_liability_insurance_13,
        pass_liability_insurance_14, theft_insurance_namt_18, autoignition_insurance_namt_5, crush_insurance_namt_8,
        wade_insurance_namt_10, scratch_insurance_namt_19, Vehcle_Code, Cmodel_Code, SY_Vhl_CAddriskVhlAge,
        Vhl_NResvNum2, JQ_Vhl_CVhlTransFlag, VsTax_CPaytaxTyp, VsTax_CTaxdptVhltyp, VsTax_TTaxEffBgnTm,
        VsTax_TTaxEffEndTm, VsTax_CTaxpayerComId, VsTax_CMotorvehFueltyp, Vhl_NDisplacement, PrmCoef_NExpectTotal,
        VsTax_NCurbWt, Base_CProdNo, SY_Vhl_TTransferDate, CAppNo, hebao_premium, Vhl_CModelNme, NewVehicleClass,
        Vhl_CGroupNme, Applicant_CClntMrk,Insured_CClntMrk, Base_TInsrncBgnTm, Base_TInsrncEndTm, Vhl_NPoWeight)

    DW_DATA = urllib.quote(urllib.quote(str(DW_DATA)))

    return DW_DATA, Base_CProdNo, Vhl_NNewPurchaseValue
