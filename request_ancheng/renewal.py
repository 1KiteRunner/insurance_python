# coding:utf8
import codecs
import json
import pickle
import re
import sys
import traceback

import jsonpath
from bs4 import BeautifulSoup

from common.log import Logger
from common.redisUtil import CRedis

from request_ancheng.login import login_ancheng
from request_ancheng.request_data import get_xubao_1, get_xubao_2
from request_cic import utils

reload(sys)
sys.setdefaultencoding('utf-8')

log = Logger()


# 续保
def is_ancheng_renewal(session, plateNumber):
    try:
        # 获取CPlyNo, 判断有没有续保信息
        ret = get_xubao_1(session, plateNumber)

        if 'JSP Processing Error' in ret.text:
            session = login_ancheng()
            return is_ancheng_renewal(session, plateNumber)

        ra = "DATA:\['(.*?)'\]"
        rb = re.compile(ra)

        title_list = re.findall(rb, ret.content)

        html = title_list[0]

        # 没有续保信息返回0
        if "CPlyNo" not in html:
            log.info(u"未查询到续信息%s" % plateNumber)
            return 0

        soup = BeautifulSoup(html, 'html.parser')

        sy_premium, jq_premium = 0, 0
        syPlyNo, jqPlyNo = 0, 0
        try:
            premiums = soup.findAll("attribute", attrs={"name": "NPrm"})
            PlyNo = soup.findAll("attribute", attrs={"name": "CPlyNo"})

            premium_1 = float(premiums[0].get_text())
            premium_2 = float(premiums[1].get_text())

            if premium_1 > premium_2:
                syPlyNo = PlyNo[0].get_text()
                jqPlyNo = PlyNo[1].get_text()
            else:
                syPlyNo = PlyNo[1].get_text()
                jqPlyNo = PlyNo[0].get_text()

            sy_premium = max(premium_1, premium_2)
            jq_premium = min(premium_1, premium_2)

        except Exception as e:
            log.info('查询商业险和交强险出错 - {0}'.format(e))

        if not syPlyNo or not jqPlyNo:
            log.info('查询保单号出错')
            return

        # 获取续保信息
        ret = get_xubao_2(session, syPlyNo, jqPlyNo)

        response_body = json.loads(ret.content)

        fields = ["Insured.CInsuredNme", "Insured.CCertfCde", "Insured.CMobile", "Insured.CSuffixAddr", "Vhl.CFrmNo",
                  "Vhl.CPlateNo", "Vhl.CEngNo", "Vhl.CModelCde", "Vhl.CModelNme", "Vhl.CFstRegYm", "Vhl.NSeatNum",
                  "SY_Base.TInsrncEndTm", "SY_Base.TInsrncBgnTm", "JQ_Base.TInsrncEndTm", "JQ_Base.TInsrncBgnTm",
                  "Vhl.CRegVhlTyp"]

        Insured_DW = jsonpath.jsonpath(response_body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Insured_DW')]")[0]
        Insured_DW_dataObjVoList = jsonpath.jsonpath(Insured_DW, "$.dataObjVoList")
        dict_1 = Insured_DW_dataObjVoList[0][0]['attributeVoList']

        Vhl_DW = jsonpath.jsonpath(response_body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Vhl_DW')]")[0]
        Vhl_DW_dataObjVoList = jsonpath.jsonpath(Vhl_DW, "$.dataObjVoList")
        dict_2 = Vhl_DW_dataObjVoList[0][0]['attributeVoList']

        Base_DW = jsonpath.jsonpath(response_body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Base_DW')]")[0]
        Base_DW_dataObjVoList = jsonpath.jsonpath(Base_DW, "$.dataObjVoList")
        dict_3 = Base_DW_dataObjVoList[0][0]['attributeVoList']

        dict_4 = dict(dict_1, **dict_2)
        dict_5 = dict(dict_4, **dict_3)

        # print dict_5

        _data = {field: dict_5[field]['value'] for field in fields}

        VsTax_DW = jsonpath.jsonpath(response_body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.VsTax_DW')]")[0]
        VsTax_DW_dataObjVoList = jsonpath.jsonpath(VsTax_DW, "$.dataObjVoList")
        dict_6 = VsTax_DW_dataObjVoList[0][0]['attributeVoList']

        VsTax_NAggTax = dict_6.get('VsTax.NTaxableAmt').get('value', 0)
        jq_premium += float(VsTax_NAggTax)

        nAggTax = '1' if VsTax_NAggTax else '0'

        # 获取险别
        Cvrg_DW = jsonpath.jsonpath(response_body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Cvrg_DW')]")[
            0]
        Cvrg_DW_dataObjVoList = jsonpath.jsonpath(Cvrg_DW, "$.dataObjVoList")

        attrs = Cvrg_DW_dataObjVoList[0]

        # print attrs

        insuranceType = {
            "otherHurtPremium": {
                "Amount": '0',
                "isCheck": "0"
            },
            "driverDutyPremium": {
                "Amount": "0",
                "isCheck": "0"
            },
            "passengerDutyPremium": {
                "Amount": '0',
                "isCheck": "0"
            },
            "carDamagePremium": "0",
            "carFireBrokenBenchMarkPremium": "0",
            "carTheftPremium": "0",
            "otherHurtBenchMarkPremium": "0",
            "carTheftBenchMarkPremium": "0",
            "engineWadingBenchMarkPremium": "0",
            "JqSumPremium": jq_premium,
            "carNickPremium": {
                "Amount": "0",
                "isCheck": "0"
            },
            "carDamageBenchMarkPremium": "0",
            "carNickBenchMarkPremium": "0",
            "engineWadingPremium": "0",
            "passengerBenchMarkPremium": "0",
            "SySumPremium": sy_premium,
            "driverDutyBenchMarkPremium": "0",
            "carFirePremium": "0",
            "glassBrokenPremium": "0",
            "compulsoryInsurance": "0",
            "nAggTax": nAggTax
        }

        for i, k in enumerate(attrs):
            num = int(k["attributeVoList"]["Cvrg.NSeqNo"]["value"])
            if num == 15:
                _otherHurtPremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 三者险
                otherHurtBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_otherHurtPremium) + u' 三者险')

                otherHurtPremium = {}
                otherHurtPremium['Amount'] = str(_otherHurtPremium)
                otherHurtPremium['isCheck'] = '1'

                insuranceType['otherHurtPremium'] = otherHurtPremium
                insuranceType['otherHurtBenchMarkPremium'] = '1' if otherHurtBenchMarkPremium == '345021001' else '0'

            elif num == 20:
                _carDamagePremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 车损险
                carDamageBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_carDamagePremium) + u' 车损险')

                carDamagePremium = '1'
                insuranceType['carDamagePremium'] = carDamagePremium
                insuranceType['carDamageBenchMarkPremium'] = '1' if carDamageBenchMarkPremium == '345021001' else '0'

            elif num == 13:
                _driverDutyPremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 车上人员险（司机）
                driverDutyBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_driverDutyPremium) + u' 车上人员险（司机）')

                driverDutyPremium = {}
                driverDutyPremium['Amount'] = _driverDutyPremium
                driverDutyPremium['isCheck'] = '1'

                insuranceType['driverDutyPremium'] = driverDutyPremium
                insuranceType['driverDutyBenchMarkPremium'] = '1' if driverDutyBenchMarkPremium == '345021001' else '0'

            elif num == 14:
                _passengerDutyPremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 车上人员险（乘客）
                passengerBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_passengerDutyPremium) + u' 车上人员险（乘客）')

                passengerDutyPremium = {}
                passengerDutyPremium['Amount'] = _passengerDutyPremium
                passengerDutyPremium['isCheck'] = '1'

                insuranceType['passengerDutyPremium'] = passengerDutyPremium
                insuranceType['passengerBenchMarkPremium'] = '1' if passengerBenchMarkPremium == '345021001' else '0'

            elif num == 18:
                _carTheftPremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 盗抢险
                carTheftBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_carTheftPremium) + u' 盗抢险')

                carTheftPremium = '1'
                insuranceType['carTheftPremium'] = carTheftPremium
                insuranceType['carTheftBenchMarkPremium'] = '1' if carTheftBenchMarkPremium == '345021001' else '0'

            elif num == 19:
                _carNickPremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 划痕险
                carNickBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_carNickPremium) + u' 划痕险')

                carNickPremium = {}
                carNickPremium['Amount'] = _carNickPremium
                carNickPremium['isCheck'] = '1'

                insuranceType['carNickPremium'] = carNickPremium
                insuranceType['carNickBenchMarkPremium'] = '1' if carNickBenchMarkPremium == '345021001' else '0'

            elif num == 8:
                _glassBrokenPremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 玻璃破碎险
                glassBrokenMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_glassBrokenPremium) + u' 玻璃破碎险')

                glassBrokenPremium = '1'
                insuranceType['glassBrokenPremium'] = glassBrokenPremium
                insuranceType['glassBrokenMarkPremium'] = '1' if glassBrokenMarkPremium == '345021001' else '0'

            elif num == 5:
                _carFirePremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 自燃险
                carFireBrokenBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_carFirePremium) + u' 自燃险')

                carFirePremium = '1'
                insuranceType['carFirePremium'] = carFirePremium
                insuranceType[
                    'carFireBrokenBenchMarkPremium'] = '1' if carFireBrokenBenchMarkPremium == '345021001' else '0'

            elif num == 10:
                _engineWadingPremium = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 涉水险
                engineWadingBenchMarkPremium = k["attributeVoList"]["Cvrg.CDductMrk"]["value"]
                log.info(str(_engineWadingPremium) + u' 涉水险')

                engineWadingPremium = '1'
                insuranceType['engineWadingPremium'] = engineWadingPremium
                insuranceType[
                    'engineWadingBenchMarkPremium'] = '1' if engineWadingBenchMarkPremium == '345021001' else '0'

            elif num == 1:
                _compulsory_insurance = float(k["attributeVoList"]["Cvrg.NAmt"]["value"])  # 交强险
                log.info(str(_compulsory_insurance) + u' 交强险')

                compulsoryInsurance = '1'
                insuranceType['compulsoryInsurance'] = compulsoryInsurance

        # print _data

        out = {
            'licenseNo': _data['Vhl.CPlateNo'],  # 车牌号
            'vinNo': _data['Vhl.CFrmNo'],  # 车架号
            'endDate': utils.getlatedate(-365, str_date=_data['SY_Base.TInsrncEndTm'][:10]),  # 保险结束期
            'CCardDetail': _data['Vhl.CRegVhlTyp'],  # 车辆类型
            'brandName': _data['Vhl.CModelNme'],  # 汽车名字
            'insuredName': _data['Insured.CInsuredNme'],  # 车主
            'identifyNumber': _data['Insured.CCertfCde'],  # 身份证号
            'mobile': _data['Insured.CMobile'],  # 手机号
            'insuredAddress': _data['Insured.CSuffixAddr'],  # 地址
            'CUsageCde': "",
            'NNewPurchaseValue': "",
            'enrollDate': _data['Vhl.CFstRegYm'],  # 初登日期
            'engineNo': _data['Vhl.CEngNo'],  # 发动机号
            'CModelCde': _data['Vhl.CModelCde'],
            'NSeatNum': _data['Vhl.NSeatNum'],  # 座位数
            'COMPANY_ID': "12",
            'insuranceType': insuranceType,
            'insuranceTime': {
                'syEnd': utils.getlatedate(-365, str_date=_data['SY_Base.TInsrncEndTm'][:10]) + ' 23:59:59',
                'syStart': utils.getlatedate(-365, str_date=_data['SY_Base.TInsrncBgnTm'][:10]) + ' 00:00:00',
                'jqStart': utils.getlatedate(-365, str_date=_data['JQ_Base.TInsrncBgnTm'][:10]) + ' 00:00:00',
                'jqEnd': utils.getlatedate(-365, str_date=_data['JQ_Base.TInsrncEndTm'][:10]) + ' 23:59:59'}
        }

        # print out
        return out
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0


if __name__ == "__main__":
    r = CRedis()
    sessBase = r.get('12_COMPANY')
    if not sessBase:
        session = login_ancheng()
    else:
        session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
    plateNumber = "苏JL5099"

    is_ancheng_renewal(session, plateNumber)
