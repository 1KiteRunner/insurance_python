# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
import  copy
#lNSeqNo=index="1" #保险数组的序列号
#lCCvrgNo="036001" #保险编号
#lNAmt="229415.00" #车辆金额
#lCDductMrk="369004"#不计免赔 如果没有设置为空 交强险的为空
#lNDductRate="0.15" #不知道什么参数 交强险为空 其他为0.15
#lNAmt_be="500000"
#seats=5
#insuredAmount,seats
def get_insurance_type(insuranceType,insuredAmount,seats,chassisNo):
    seats =int(seats)
    kindsInfo=[]
    kind={
            "adjustRate": "",
            "modeCode": "",
            "serialNo": 1,
            "unitAmount": "",
            "rate": "",
            "value": "",
            "deductibleRate": "",
            "disCount": "",
            "amount": "",
            "unCommon": "",
            "benchmarkPremium": "",
            "premium": "",
            "kindName": "",
            "kindFlag": 0,
            "kindCode": "",
            "quantity": ""
         }

    if insuranceType.get("glassBrokenPremium","0")=="1":
        glassBrokenPremium=copy.deepcopy(kind)
        glassBrokenPremium["kindCode"]="F"
        glassBrokenPremium["kindFlag"]=0
        glassBrokenPremium["kindName"]="玻璃单独破碎险"
        if chassisNo[0:1] != 'L':
            glassBrokenPremium["modeCode"] = "2"
        else:
            glassBrokenPremium["modeCode"]="1"
        kindsInfo.append(glassBrokenPremium)


    if insuranceType.get("carFirePremium","0")=="1":
        carFirePremium=copy.deepcopy(kind)
        carFirePremium["amount"]=insuredAmount
        carFirePremium["kindCode"]="Z"
        carFirePremium["kindName"]="自燃损失险"

        if insuranceType.get("carFireBrokenBenchMarkPremium","0")=="1":
            carFirePremium['kindFlag']=1
        else:
            carFirePremium['kindFlag']=0
        kindsInfo.append(carFirePremium)

    if insuranceType.get("engineWadingPremium","0")=="1":
        engineWadingPremium=copy.deepcopy(kind)
        engineWadingPremium["kindCode"]="X1"
        engineWadingPremium["kindName"]="发动机涉水损失险"
        engineWadingPremium["unCommon"]="X1"

        if insuranceType.get("engineWadingBenchMarkPremium","")=="1":
            engineWadingPremium['kindFlag']=1
        else:
            engineWadingPremium['kindFlag']=0
        kindsInfo.append(engineWadingPremium)

    if insuranceType.get("carTheftPremium","0")=="1":
        carTheftPremium=copy.deepcopy(kind)
        carTheftPremium['amount']=insuredAmount
        carTheftPremium['deductibleRate']=100
        carTheftPremium['kindCode']="G1"
        carTheftPremium['kindName']="全车盗抢保险"

        if insuranceType.get("carTheftBenchMarkPremium","0")=="1":
            carTheftPremium['kindFlag']=1
        else:
            carTheftPremium['kindFlag']=0
        kindsInfo.append(carTheftPremium)
    # # 车辆损失保险
    if insuranceType.get("carDamagePremium","0")=="1":
        carDamagePremium=copy.deepcopy(kind)
        carDamagePremium['amount']=insuredAmount
        carDamagePremium['kindCode']="A"
        carDamagePremium['kindName']="车辆损失保险"
        if insuranceType.get("carDamageBenchMarkPremium","0")=="1":
            carDamagePremium['kindFlag']=1
        else:
            carDamagePremium['kindFlag']=0
        kindsInfo.append(carDamagePremium)

    if insuranceType.get("repairFactoryPremium",{}).get("isCheck","0")=="1":
        carDamagePremium = copy.deepcopy(kind)
        carDamagePremium['deductibleRate'] = str(insuranceType.get("repairFactoryPremium",{}).get("rate","15"))

    #第三方责任险
    if insuranceType.get("otherHurtPremium",{}).get("isCheck","0")=="1":
        otherHurtPremium=copy.deepcopy(kind)
        otherHurtPremium['amount']=str(insuranceType.get("otherHurtPremium",{}).get("Amount","500000"))
        otherHurtPremium['kindCode']="B"
        otherHurtPremium['kindName']="第三者责任保险"
        if insuranceType.get("otherHurtBenchMarkPremium","0")=="1":
            otherHurtPremium['kindFlag']=1
        else:
            otherHurtPremium['kindFlag']=0
        kindsInfo.append(otherHurtPremium)


    if insuranceType.get("carNickPremium",{}).get("isCheck","0")=="1":
        carNickPremium=copy.deepcopy(kind)
        carNickPremium["amount"]=insuranceType.get("carNickPremLium",{}).get("Amount","2000")
        carNickPremium["kindCode"]="L"
        carNickPremium["kindName"]="车身划痕损失险"
        if insuranceType.get("carNickBenchMarkPremium","0")=="1":
            carNickPremium['kindFlag']=1
        else:
            carNickPremium['kindFlag']=0
        kindsInfo.append(carNickPremium)



    if insuranceType.get("driverDutyPremium",{}).get("isCheck","0")=="1":
        driverDutyPremium=copy.deepcopy(kind)
        driverDutyPremium['amount']=insuranceType.get("driverDutyPremium",{}).get("Amount","10000")
        driverDutyPremium['kindCode']="D3"
        driverDutyPremium['kindName']="车上人员责任保险（司机）"
        driverDutyPremium['quantity']=1
        driverDutyPremium['unitAmount']=insuranceType.get("driverDutyPremium",{}).get("Amount","10000")

        if insuranceType.get("driverDutyBenchMarkPremium","0")=="1":
            driverDutyPremium['kindFlag']=1
        else:
            driverDutyPremium['kindFlag']=0
        kindsInfo.append(driverDutyPremium)

    if insuranceType.get("passengerDutyPremium",{}).get("isCheck","0")=="1":
        #passengerDutyPremium['insuredAmount']=int(insuranceType.get("passengerDutyPremium",{}).get("Amount","10000"))
        #passengerDutyPremium["seats"]=seats-1
        passengerDutyPremium=copy.deepcopy(kind)
        passengerDutyPremium['amount']=str(int(insuranceType.get("passengerDutyPremium",{}).get("Amount","10000"))*(seats-1))
        passengerDutyPremium['kindCode']="D4"
        passengerDutyPremium['kindName']="车上人员责任保险（乘客）"
        passengerDutyPremium['quantity']=str(seats-1)
        passengerDutyPremium['unitAmount']=insuranceType.get("passengerDutyPremium",{}).get("Amount","10000")
        if insuranceType.get("passengerBenchMarkPremium","0")=="1":
            passengerDutyPremium['kindFlag']=1
        else:
            passengerDutyPremium['kindFlag']=0
        kindsInfo.append(passengerDutyPremium)
    #交通强制险
    if insuranceType.get("compulsoryInsurance","1")=="1":
        compulsoryInsurance=copy.deepcopy(kind)
        compulsoryInsurance['amount']="122000"
        compulsoryInsurance['kindCode']="BZ"
        compulsoryInsurance['kindFlag']=0
        compulsoryInsurance['kindName']="交通事故强制责任险"
        kindsInfo.append(compulsoryInsurance)
    #kindsInfo=json.loads(json.dumps(kindsInfo,ensure_ascii=False))


    if insuranceType.get("carDamageBenchMarkPremium","0")=="1" or insuranceType.get("otherHurtBenchMarkPremium","0")=="1" or insuranceType.get("carTheftBenchMarkPremium","0")=="1"  or insuranceType.get("driverDutyBenchMarkPremium","0")=="1" or insuranceType.get("passengerBenchMarkPremium","0")=="1" or insuranceType.get("carNickBenchMarkPremium","0")=="1"  or insuranceType.get("carFireBrokenBenchMarkPremium","0")=="1" or insuranceType.get("engineWadingBenchMarkPremium","0")=="1":
        bujimianpei=copy.deepcopy(kind)
        bujimianpei["kindCode"]="M"
        bujimianpei["kindFlag"]=0
        bujimianpei["kindName"]="不计免赔额特约"
        kindsInfo.append(bujimianpei)
    return kindsInfo

if __name__=="__main__":
     insuranceType = {
        'compulsoryInsurance': "1",  # 交通事故强制责任险
        'nAggTax': '1',  # 车船税

        'otherHurtPremium': {"isCheck": "1", "Amount": "500000"},  # 第三者责任保险
       'carNickPremium': {"isCheck": "1", "Amount": "2000"},  # 车身划痕损失险
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
       'carNickBenchMarkPremium': '1',  # 不计免赔——车身划痕损失险
        'carFireBrokenBenchMarkPremium': '1',  # 不计免赔——自燃损失险
        'engineWadingBenchMarkPremium': '1'  # 不计免赔——发动机涉水损失险
         }
     import json
     aa=get_insurance_type(insuranceType,"8888.00","5")
     print((json.dumps(aa,ensure_ascii=False)))