# -*- coding:utf-8 -*-
import jsonpath
def readJson(json,seatCount,jq_resp):
    compulsory_insurance =  None
    NAggTax = None
    if jq_resp is not None:
        compulsory_insurance = jq_resp['premiumBZ']
        NAggTax = jq_resp['thisPayTax']
    Premium = {
        # jsonpath.jsonpath(json, "$.commonPackage.items[?(@.kindCode=='050200')].amount")
        "compulsory_insurance": compulsory_insurance,  # 交强险
        "NAggTax": NAggTax,  # 车船税
        "carDamagePremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050200')].premium"),  # 车损险
        "carTheftPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050500')].premium"),  # 盗抢险
        "otherHurtPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050600')].premium"),  # 三者险
        "driverDutyPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050701')].premium"),  # 车上人员险（司机）
        "passengerDutyPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050702')].premium"),  # 车上人员险(乘客)
        "carNickPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050210')].premium"),  # 划痕险
        "glassBrokenPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050231')].premium"),  # 玻璃破碎险
        "carFirePremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050310')].premium"),  # 自燃损失险
        "engineWadingPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050291')].premium"),  # 发动机涉水险
        "seatCount": seatCount
    }
    BaoE = {
        "otherHurtBaoE": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050600')].amount"),
        "driverDutyBaoE": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050701')].amount"),
        "passengerDutyBaoe": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050702')].amount"),
        "carNickBaoE": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050210')].amount")
    }
    MarkPremium = {
        "carDamageBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050911')].premium"),  # 车损险不计免赔
        "carTheftBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050921')].premium"),  # 盗抢险不计免赔
        "otherHurtBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050912')].premium"),  # 三者责任险的不计免赔
        "driverDutyBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050928')].premium"),  # 车上人员责任险（司机）不计免赔含税保费
        "passengerBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050929')].premium"),  # 车上人员责任险（乘客）不计免赔含税保费
        "carNickBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050922')].premium"),  # 划痕险不计免赔含税保费
        "carFireBrokenBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050935')].premium"),  # 自燃损失险不计免赔含税保费
        "engineWadingBenchMarkPremium": jsonpath.jsonpath(json, "$.[?(@.kindCode=='050924')].premium")  # 发动机涉水险不计免赔含税保费
    }
    PremiumInfo = [Premium,BaoE,MarkPremium]
    return PremiumInfo
