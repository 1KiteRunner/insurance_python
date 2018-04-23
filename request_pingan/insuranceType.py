# -*- coding:utf-8 -*-
__author__ = 'weikai'
'''
01 # 车损险     27 # 车损险不计免赔
02 # 三者险    28  # 三者责任险的不计免赔
03  # 盗抢险   48 # 盗抢险不计免赔
04  # 车上人员险（司机） 49 # 车上人员责任险（司机）不计免赔含税保费
05  # 车上人员险(乘客) 80 # 车上人员责任险（乘客）不计免赔含税保费
08 # 玻璃破碎险
17 # 划痕险  75 # 划痕险不计免赔含税保费
18  # 自燃损失险  77 # 自燃损失险不计免赔含税保费
41  # 发动机涉水险 79 # 发动机涉水险不计免赔含税保费
57 指定修理厂
'''


def get_insurance_type(insuranceType, insuredAmount, seats, vino):
    '''
    :param insuranceType:保险类型
    :param insuredAmount: 车辆协商价值
    :param seats: 乘客座位数 = 座位数-1
    :return:
    '''
    all_type = []
    # insuredAmount = ""
    # seats=4
    insuredAmount = int(insuredAmount)
    seats = int(seats)
    otherHurtPremiumAmount = 50  # 50万
    carNickPremiumAmount = 2000
    driverDutyPremiumAmount = 10000
    passengerDutyPremiumAmount = 10000
    carNickPremium = {
        "dutyCode": "17",
        "insuredAmount": carNickPremiumAmount,
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }

    carFirePremium = {
        "dutyCode": "18",
        "insuredAmount": insuredAmount,
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "insuredAmountDefaultValue": insuredAmount,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    carDamageBenchMarkPremium = {
        "dutyCode": "27",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }

    otherHurtBenchMarkPremium = {
        "dutyCode": "28",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }

    engineWadingPremium = {
        "dutyCode": "41",
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }

    carTheftBenchMarkPremium = {
        "dutyCode": "48",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    driverDutyBenchMarkPremium = {
        "dutyCode": "49",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    carNickBenchMarkPremium = {
        "dutyCode": "75",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    carFireBrokenBenchMarkPremium = {
        "dutyCode": "77",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    engineWadingBenchMarkPremium = {
        "dutyCode": "79",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }

    passengerBenchMarkPremium = {
        "dutyCode": "80",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    carDamagePremium = {
        "dutyCode": "01",
        "insuredAmount": insuredAmount,
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    otherHurtPremium = {
        "dutyCode": "02",
        "insuredAmount": otherHurtPremiumAmount,
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    carTheftPremium = {
        "dutyCode": "03",
        "insuredAmount": insuredAmount,
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "insuredAmountDefaultValue": insuredAmount,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    driverDutyPremium = {
        "dutyCode": "04",
        "insuredAmount": driverDutyPremiumAmount,
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }
    passengerDutyPremium = {
        "dutyCode": "05",
        "insuredAmount": passengerDutyPremiumAmount,
        "seats": seats,
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": ""
    }

    glassBrokenPremium = {
        "dutyCode": "08",
        "seats": "0",
        "premiumRate": 0,
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": "",
        "isSpecialGlass": 0
    }
    # 指定修理厂
    repairFactoryPremium = {
        "dutyCode": "57",
        "seats": "0",  # 0 国产 1 进口
        "premiumRate": "15",
        "basePremium": 0,
        "totalStandardPremium": 0,
        "totalAgreePremium": 0,
        "totalActualPremium": 0,
        "pureRiskPremium": "",
        "riskPremium": "",
        "isSpecialGlass": 0
    }
    if insuranceType.get("repairFactoryPremium", {}).get("isCheck", "0") == "1":
        rate = insuranceType.get("repairFactoryPremium", {}).get("rate", "0")
        repairFactoryPremium['premiumRate'] = rate
        # 国产 车架号开头为L
        if vino[0] == "L" or vino[0] == "l":
            repairFactoryPremium['seats'] = "0"
        else:
            repairFactoryPremium['seats'] = "1"
        all_type.append(repairFactoryPremium)
    if insuranceType.get("glassBrokenPremium", "0") == "1":
        # 国产 车架号开头为L
        if vino[0] == "L" or vino[0] == "l":
            glassBrokenPremium['seats'] = "0"
        else:
            glassBrokenPremium['seats'] = "1"
        all_type.append(glassBrokenPremium)

    if insuranceType.get("carFirePremium", "0") == "1":
        all_type.append(carFirePremium)
        if insuranceType.get("carFireBrokenBenchMarkPremium", "0") == "1":
            all_type.append(carFireBrokenBenchMarkPremium)

    if insuranceType.get("engineWadingPremium", "0") == "1":
        all_type.append(engineWadingPremium)
        if insuranceType.get("engineWadingBenchMarkPremium", "") == "1":
            all_type.append(engineWadingBenchMarkPremium)

    if insuranceType.get("carTheftPremium", "0") == "1":
        all_type.append(carTheftPremium)
        if insuranceType.get("carTheftBenchMarkPremium", "0") == "1":
            all_type.append(carTheftBenchMarkPremium)

    if insuranceType.get("carDamagePremium", "0") == "1":
        all_type.append(carDamagePremium)
        if insuranceType.get("carDamageBenchMarkPremium", "0") == "1":
            all_type.append(carDamageBenchMarkPremium)

    if insuranceType.get("otherHurtPremium", {}).get("isCheck", "0") == "1":
        otherHurtPremium['insuredAmount'] = int(
            float(insuranceType.get("otherHurtPremium", {}).get("Amount", "500000"))) / 10000
        all_type.append(otherHurtPremium)
        if insuranceType.get("otherHurtBenchMarkPremium", "0") == "1":
            all_type.append(otherHurtBenchMarkPremium)

    if insuranceType.get("carNickPremium", {}).get("isCheck", "0") == "1":
        carNickPremium['insuredAmount'] = int(insuranceType.get("carNickPremium", {}).get("Amount", "2000"))
        all_type.append(carNickPremium)
        if insuranceType.get("carNickBenchMarkPremium", "0") == "1":
            all_type.append(carNickBenchMarkPremium)

    if insuranceType.get("driverDutyPremium", {}).get("isCheck", "0") == "1":
        driverDutyPremium['insuredAmount'] = int(insuranceType.get("driverDutyPremium", {}).get("Amount", "10000"))
        all_type.append(driverDutyPremium)
        if insuranceType.get("driverDutyBenchMarkPremium", "0") == "1":
            all_type.append(driverDutyBenchMarkPremium)

    if insuranceType.get("passengerDutyPremium", {}).get("isCheck", "0") == "1":
        passengerDutyPremium['insuredAmount'] = int(
            insuranceType.get("passengerDutyPremium", {}).get("Amount", "10000"))
        passengerDutyPremium["seats"] = seats - 1
        all_type.append(passengerDutyPremium)
        if insuranceType.get("passengerBenchMarkPremium", "0") == "1":
            all_type.append(passengerBenchMarkPremium)

    return all_type


if __name__ == "__main__":
    '''
    insuranceType = {
    'compulsoryInsurance': "1",  # 交通事故强制责任险
    'nAggTax': '1',  # 车船税

    'otherHurtPremium': {"isCheck": "1", "Amount": "500000"},  # 第三者责任保险
   # 'carNickPremium': {"isCheck": "1", "Amount": "2000"},  # 车身划痕损失险
    'driverDutyPremium': {"isCheck": "1", "Amount": "10000"},  # 车上人员责任保险（司机）
    'passengerDutyPremium': {"isCheck": "1", "Amount": "10000"},# 车上人员责任保险（乘客）

    'glassBrokenPremium': "1",  # 玻璃单独破碎险(国产)
    'carFirePremium': "1",  # 自燃损失险
    'engineWadingPremium': "1",  # 发动机涉水损失险
    'carTheftPremium': "1",  # 全车盗抢保险
    'carDamagePremium': "1",  # 车辆损失保险
    'carDamageBenchMarkPremium': '1',  # 不计免赔——车辆损失保险
    'otherHurtBenchMarkPremium': '1',  # 不计免赔——第三者责任保险
    'carTheftBenchMarkPremium': '1',  # 不计免赔——全车盗抢保险
    'driverDutyBenchMarkPremium': '1',  # 不计免赔——车上人员责任保险（司机）
    'passengerBenchMarkPremium': '1',  # 不计免赔——车上人员责任保险（乘客）
   # 'carNickBenchMarkPremium': '1',  # 不计免赔——车身划痕损失险
    'carFireBrokenBenchMarkPremium': '1',  # 不计免赔——自燃损失险
    'engineWadingBenchMarkPremium': '1'  # 不计免赔——发动机涉水损失险
     }

    print get_insurance_type(insuranceType,80000,5)
'''
    insuranceType = {
        'compulsoryInsurance': "1",  # 交通事故强制责任险
        'nAggTax': '1',  # 车船税
        'otherHurtPremium': {"isCheck": "0", "Amount": "500000"},  # 第三者责任保险
        # 'carNickPremium': {"isCheck": "1", "Amount": "2000"},  # 车身划痕损失险
        'driverDutyPremium': {"isCheck": "0", "Amount": "10000"},  # 车上人员责任保险（司机）
        'passengerDutyPremium': {"isCheck": "0", "Amount": "10000"},  # 车上人员责任保险（乘客）

        'glassBrokenPremium': "0",  # 玻璃单独破碎险(国产)
        'carFirePremium': "0",  # 自燃损失险
        'engineWadingPremium': "0",  # 发动机涉水损失险
        'carTheftPremium': "0",  # 全车盗抢保险
        'carDamagePremium': "0",  # 车辆损失保险
        'carDamageBenchMarkPremium': '0',  # 不计免赔——车辆损失保险
        'otherHurtBenchMarkPremium': '0',  # 不计免赔——第三者责任保险
        'carTheftBenchMarkPremium': '0',  # 不计免赔——全车盗抢保险
        'driverDutyBenchMarkPremium': '0',  # 不计免赔——车上人员责任保险（司机）
        'passengerBenchMarkPremium': '0',  # 不计免赔——车上人员责任保险（乘客）
        # 'carNickBenchMarkPremium': '1',  # 不计免赔——车身划痕损失险
        'carFireBrokenBenchMarkPremium': '0',  # 不计免赔——自燃损失险
        'engineWadingBenchMarkPremium': '0'  # 不计免赔——发动机涉水损失险
    }

    print get_insurance_type(insuranceType, 80000, 5)
