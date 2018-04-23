# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json

def get_hn_insurance_type(insuranceType, insuredAmount, seats,carPrice):
    '''
    :param insuranceType:保险类型
    :param insuredAmount: 车辆协商价值
    :param seats: 乘客座位数 = 座位数-1
    :param carPrice 新车购置价
    :return:
    '''
    all_type = []
    # insuredAmount = ""
    # seats=4
    insuredAmount = int(insuredAmount)
    seats = int(seats)

    if insuranceType.get("compulsoryInsurance","0")=="1":
        all_type.append({"amount":"122000.00","kindName":"机动车交通事故责任强制保险","flag":"10","kindCode":"BZ"})

    if insuranceType.get("glassBrokenPremium", "0") == "1":
        all_type.append({"modeName":"国产玻璃","modeCode":"1","flag":"20","amount":carPrice+".00","kindName":"玻璃单独破碎险","kindCode":"F"})

    if insuranceType.get("carFirePremium", "0") == "1":
        if insuranceType.get("carFireBrokenBenchMarkPremium", "0") == "1":
            all_type.append({"amount": str(insuredAmount), "kindName": "自燃损失险", "flag": "21", "kindCode": "Z"})
            all_type.append({"amount": 0, "kindName": "自燃损失险不计免赔", "flag": "20", "kindCode": "MZ"})
        else:
            all_type.append({"amount": str(insuredAmount), "kindName": "自燃损失险", "flag": "20", "kindCode": "Z"})
    if insuranceType.get("engineWadingPremium", "0") == "1":
        if insuranceType.get("engineWadingBenchMarkPremium", "") == "1":
            all_type.append({"amount": 0, "kindName": "发动机涉水损失险", "flag": "21", "kindCode": "X1"})
            all_type.append({"amount": 0, "kindName": "发动机涉水损失险不计免赔", "flag": "20", "kindCode": "MX1"})
        else:
            all_type.append({"amount": 0, "kindName": "发动机涉水损失险", "flag": "20", "kindCode": "X1"})

    if insuranceType.get("carTheftPremium", "0") == "1":
        if insuranceType.get("carTheftBenchMarkPremium", "0") == "1":
            all_type.append({"amount": 0, "kindName": "机动车盗抢险不计免赔", "flag": "20", "kindCode": "MG"})
            all_type.append({"amount": str(insuredAmount), "kindName": "全车盗抢险", "flag": "11", "kindCode": "G"})
        else:
            all_type.append({"amount": str(insuredAmount), "kindName": "全车盗抢险", "flag": "10", "kindCode": "G"})

    if insuranceType.get("carDamagePremium", "0") == "1":
        if insuranceType.get("carDamageBenchMarkPremium", "0") == "1":
            all_type.append({"amount": str(insuredAmount), "kindName": "机动车损失险", "flag": "11", "kindCode": "A", "deductible": "0"})
            all_type.append({"amount": 0, "kindName": "机动车损失险不计免赔", "flag": "20", "kindCode": "MA"})
        else:
            all_type.append({"amount": str(insuredAmount), "kindName": "机动车损失险", "flag": "10", "kindCode": "A", "deductible": "0"})

    if insuranceType.get("otherHurtPremium", {}).get("isCheck", "0") == "1":
        otherHurtAmount = insuranceType.get("otherHurtPremium", {}).get("Amount", "500000") + ".00"
        if insuranceType.get("otherHurtBenchMarkPremium", "0") == "1":
            all_type.append({"amount": 0, "kindName": "第三者责任险不计免赔", "flag": "20", "kindCode": "MB"})
            all_type.append({"amount": otherHurtAmount, "kindName": "第三者责任险", "flag": "11", "kindCode": "B"})
        else:
            all_type.append({"amount": otherHurtAmount, "kindName": "第三者责任险", "flag": "10", "kindCode": "B"})

    if insuranceType.get("carNickPremium", {}).get("isCheck", "0") == "1":
        carNickAmount = (insuranceType.get("carNickPremium", {}).get("Amount", "2000")) + ".00"

        if insuranceType.get("carNickBenchMarkPremium", "0") == "1":
            all_type.append({"amount": carNickAmount, "kindName": "车身划痕损失险", "flag": "21", "kindCode": "L"})
            all_type.append({"amount": 0, "kindName": "车身划痕损失险不计免赔", "flag": "20", "kindCode": "ML"})
        else:
            all_type.append({"amount": carNickAmount, "kindName": "车身划痕损失险", "flag": "20", "kindCode": "L"})
    if insuranceType.get("driverDutyPremium", {}).get("isCheck", "0") == "1":
        driverDutyAmount = insuranceType.get("driverDutyPremium", {}).get("Amount", "10000") + ".00"
        if insuranceType.get("driverDutyBenchMarkPremium", "0") == "1":
            all_type.append({"amount": 0, "kindName": "车上人员(驾驶员)责任不计免赔", "flag": "20", "kindCode": "MD3"})
            all_type.append({"amount": driverDutyAmount, "kindName": "车上人员责任险：驾驶员", "flag": "11", "kindCode": "D3"})
        else:
            all_type.append({"amount": driverDutyAmount, "kindName": "车上人员责任险：驾驶员", "flag": "10", "kindCode": "D3"})

    if insuranceType.get("passengerDutyPremium", {}).get("isCheck", "0") == "1":
        passengerAmount = int(insuranceType.get("passengerDutyPremium", {}).get("Amount", "10000"))
        passengerAllAmount = passengerAmount * (seats - 1)
        seatspassage = str(seats - 1)
        if insuranceType.get("passengerBenchMarkPremium", "0") == "1":
            all_type.append({"amount": 0, "kindName": "车上人员(乘客)责任不计免赔", "flag": "20", "kindCode": "MD4"})
            all_type.append({"unitAmount": str(passengerAmount) + ".00", "amount": passengerAllAmount, "flag": "11",
                         "kindName": "车上人员责任险：乘客", "kindCode": "D4", "quantity": seatspassage})
        else:
            all_type.append({"unitAmount": str(passengerAmount) + ".00", "amount": passengerAllAmount, "flag": "10",
                         "kindName": "车上人员责任险：乘客", "kindCode": "D4", "quantity": seatspassage})

    return json.loads(json.dumps(all_type))


if __name__ == "__main__":

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
    import json
    print json.dumps(get_hn_insurance_type(insuranceType,80000,5,"10000"),ensure_ascii=False)

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

    print get_hn_insurance_type(insuranceType,80000,5,"10000")
