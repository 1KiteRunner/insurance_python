# -*- coding:utf-8 -*-
import jsonpath
import json
def getPriumeInf(result,insuranceType):
    BZ = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='BZ')]")
    carDamage = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='A')]")  # 车辆损失保险
    otherHurt = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='B')]")  # 第三者责任保险
    carTheft = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='G1')]")  # 全车盗抢保险
    driverDuty = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='D3')]")  # 车上人员责任保险（司机）
    passengerDuty = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='D4')]")  # 车上人员责任保险（乘客）
    glassBroken = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='F')]")  # 玻璃单独破碎险没有不计免赔
    carNick = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='L')]")  # 车身划痕损失险
    carFire = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='Z')]")  # 自燃损失险
    engineWading = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='X1')]")  # 发动机涉水险
    repairFactory = jsonpath.jsonpath(result, "$.result[0].kinds.[?(@.kindCode=='A4')]")  # 指定修理厂

    Premium = {}
    BaoE = {}
    MarkPremium = {}
    disCount = {}
    # print json.dumps(result,ensure_ascii=False,indent=4)

    if BZ is not False:
        Premium["compulsory_insurance"] =  BZ[0]['premium']
        disCount['jq_disCount'] = (1- float(BZ[0].get('adjustRate',"0"))/100)

    if result['result'][0].get('carTax.sumPayment',"") != "":
        Premium["NAggTax"] = result['result'][0].get('carTax.sumPayment',"")

    if carDamage is not False:
        Premium["carDamagePremium"] = carDamage[0]["premium"]
        BaoE['carDamageBaoE'] = carDamage[0]["amount"]
        disCount['sy_disCount'] = (1 - float(carDamage[0]['disCount'])/ 100) *( 1- float(carDamage[0].get('adjustRate',"0"))/100)
        if insuranceType.get("carDamageBenchMarkPremium", "0") == "1":
            MarkPremium['carDamageBenchMarkPremium'] =round(float(carDamage[0]["premium"]) * 0.15, 2)

    if carTheft is not False:
        Premium["carTheftPremium"] = carTheft[0]["premium"]
        disCount['sy_disCount'] = (1 - float(carTheft[0]['disCount'])/ 100) *( 1- float(carTheft[0].get('adjustRate',"0"))/100)
        if insuranceType.get("carTheftBenchMarkPremium", "0") == "1":
            MarkPremium['carTheftBenchMarkPremium'] = round(float(carTheft[0]["premium"])*0.2, 2)

    if otherHurt is not False:
        Premium["otherHurtPremium"] = otherHurt[0]["premium"]
        BaoE["otherHurtBaoE"] =  otherHurt[0]["amount"]
        disCount['sy_disCount'] = (1 - float(otherHurt[0]['disCount'])/ 100) *( 1- float(otherHurt[0].get('adjustRate',"0"))/100)
        if insuranceType.get("otherHurtBenchMarkPremium","0")=="1":
            MarkPremium['otherHurtBenchMarkPremium'] = round(float(otherHurt[0]["premium"]) * 0.15, 2)

    if driverDuty is not False:
        Premium["driverDutyPremium"] = driverDuty[0]["premium"]
        BaoE['driverDutyBaoE'] = driverDuty[0]["amount"]
        disCount['sy_disCount'] = (1 - float(driverDuty[0]['disCount'])/ 100) *( 1- float(driverDuty[0].get('adjustRate',"0"))/100)
        if insuranceType.get("driverDutyBenchMarkPremium","0")=="1":
            MarkPremium['driverDutyBenchMarkPremium'] = round(float(driverDuty[0]["premium"]) * 0.15, 2)



    if passengerDuty is not False:
        Premium["passengerDutyPremium"] = passengerDuty[0]["premium"]
        BaoE['passengerDutyBaoe'] = passengerDuty[0]["amount"]
        disCount['sy_disCount'] = (1 - float(passengerDuty[0]['disCount'])/ 100) *( 1- float(passengerDuty[0].get('adjustRate',"0"))/100)
        if insuranceType.get("passengerBenchMarkPremium","0")=="1":
            MarkPremium['passengerBenchMarkPremium'] = round(float(passengerDuty[0]["premium"]) * 0.15, 2)

    if carNick is not False:
        Premium["carNickPremium"] = carNick[0]["premium"]
        BaoE['carNickBaoE'] = carNick[0]["amount"]
        disCount['sy_disCount'] = (1 - float(carNick[0]['disCount'])/ 100) *( 1- float(carNick[0].get('adjustRate',"0"))/100)
        if insuranceType.get("carNickBenchMarkPremium","0")=="1":
            MarkPremium['carNickBenchMarkPremium'] = round(float(carNick[0]["premium"]) * 0.15, 2)

    if glassBroken is not False:
        Premium["glassBrokenPremium"] = glassBroken[0]["premium"]
        disCount['sy_disCount'] = (1 - float(glassBroken[0]['disCount'])/ 100) *( 1- float(glassBroken[0].get('adjustRate',"0"))/100)

    if repairFactory is not False:
        Premium["repairFactoryPremium"] = repairFactory[0]["premium"]
        disCount['sy_disCount'] = (1 - float(repairFactory[0]['disCount'])/ 100) *( 1- float(repairFactory[0].get('adjustRate',"0"))/100)

    if carFire is not False:
        Premium["carFirePremium"] = carFire[0]["premium"]
        disCount['sy_disCount'] = (1 - float(carFire[0]['disCount'])/ 100) *( 1- float(carFire[0].get('adjustRate',"0"))/100)
        if insuranceType.get("carFireBrokenBenchMarkPremium","0")=="1":
            MarkPremium['carFireBrokenBenchMarkPremium'] = round(float(carFire[0]["premium"]) * 0.2, 2)

    if engineWading is not False:
        Premium["engineWadingPremium"] = engineWading[0]["premium"]
        disCount['sy_disCount'] = (1 - float(engineWading[0]['disCount'])/ 100) *( 1- float(engineWading[0].get('adjustRate',"0"))/100)
        if insuranceType.get("engineWadingBenchMarkPremium","")=="1":
            MarkPremium['engineWadingBenchMarkPremium'] = round(float(engineWading[0]["premium"]) * 0.15, 2)
    if disCount.get('sy_disCount') is not None:
        disCount['sy_disCount'] = round(disCount['sy_disCount'],4)
    PremiumInfo = [Premium, BaoE, MarkPremium,disCount]
    return PremiumInfo