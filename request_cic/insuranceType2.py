# -*- coding:utf-8 -*-
__author__ = 'weikai'
import copy
from string import Template


# lNSeqNo=index="1" #保险数组的序列号
# lCCvrgNo="036001" #保险编号
# lNAmt="229415.00" #车辆金额
# lCDductMrk="369004"#不计免赔 如果没有设置为空 交强险的为空
# lNDductRate="0.15" #不知道什么参数 交强险为空 其他为0.15
# lNAmt_be="500000"
# seats=5
# insuredAmount,seats
def get_insurance_type(insuranceType, lNAmt, seats, vino):
    seats = int(seats)
    dataObjVoList = '''"dataObjVoList": ['''

    attributeVoList = '''
    {
        "index": "${index}",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            _-a"_-lCCancelMrk",
            _-b"0"
          },
          {
            _-a"_-lNSeqNo",
            _-b"${lNSeqNo}"
          },
          {
            _-a"_-lCPkId",
            _-b""
          },
          {
            _-a"_-lCCvrgNo",
            _-b"${lCCvrgNo}"
          },
          {
            _-a"_-lNAmt",
            _-b"${lNAmt}"
          },
          {
            _-a"_-lCDductMrk",
            _-b"${lCDductMrk}"
          },
          {
            _-a"_-lNBasePrm",
            _-b"${lNBasePrm}"
          },
          {
            _-a"_-lNPrm",
            _-b"${lNPrm}"
          },
          {
            _-a"_-lNPerAmt",
            _-b"${lNPerAmt}"
          },
          {
            _-a"_-lNLiabDaysLmt",
            _-b"${lNLiabDaysLmt}"
          },
          {
            _-a"_-lNIndemLmt",
            _-b"${lNIndemLmt}"
          },
          {
            _-a"_-lNRate",
            _-b"${lNRate}"
          },
          {
            _-a"_-lCRowId",
            _-b""
          },
          {
            _-a"_-lCCrtCde",
            _-b""
          },
          {
            _-a"_-lTCrtTm",
            _-b""
          },
          {
            _-a"_-lNDeductible",
            _-b""
          },
          {
            _-a"_-lCUpdCde",
            _-b""
          },
          {
            _-a"_-lTUpdTm",
            _-b""
          },
          {
            _-a"_-lTBgnTm",
            _-b""
          },
          {
            _-a"_-lTEndTm",
            _-b""
          },
          {
            _-a"_-lNDisCoef",
            _-b""
          },
          {
            _-a"_-l_-s30",
            _-b"${s30}"
          },
          {
            _-a"_-l_-s29",
            _-b"${s29}"
          },
          {
            _-a"_-l_-s12",
            _-b""
          },
          {
            _-a"_-l_-s1",
            _-b""
          },
          {
            _-a"_-lCIndemLmtLvl",
            _-b"${lCIndemLmtLvl}"
          },
          {
            _-a"_-lNDductRate",
            _-b"${lNDductRate}"
          },
          {
            _-a"_-l_-u1",
            _-b""
          },
          {
            _-a"_-lNPerPrm",
            _-b""
          },
          {
            _-a"_-lNDductPrm",
            _-b""
          },
          {
            _-a"_-lNBefPrm",
            _-b""
          },
          {
            _-a"_-lNVhlActVal",
            _-b"${lNVhlActVal}"
          }
        ]
      }
    '''

    if insuranceType.get("glassBrokenPremium", "0") == "1":
        b_s30 = "303011001"
        if vino[0] == "L":
            b_s30 = "303011001"
        else:
            b_s30 = "303011002"
        glassBrokenPremium = copy.deepcopy(attributeVoList)
        glassBrokenPremium = Template(glassBrokenPremium)
        glassBrokenPremium = glassBrokenPremium.substitute(
            index="6",
            lCIndemLmtLvl="",
            lNBasePrm="",
            lNAmt="",
            lNPrm="",
            lNIndemLmt="",
            lNSeqNo="6",
            lNDductRate="",
            s30=b_s30,  # 303011002 进口玻璃
            lNVhlActVal="",
            lNLiabDaysLmt="",
            lNRate="0",
            lNPerAmt="",
            s29="0",
            lCCvrgNo="036006",  #
            lCDductMrk="")

        dataObjVoList = dataObjVoList + glassBrokenPremium

    if insuranceType.get("carFirePremium", "0") == "1":
        carFirePremium = copy.deepcopy(attributeVoList)
        carFirePremium = Template(carFirePremium)
        lCDductMrk = ""
        if insuranceType.get("carFireBrokenBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        carFirePremium = carFirePremium.substitute(index="7",
                                                   lCIndemLmtLvl="",
                                                   lNBasePrm="",
                                                   lNAmt=lNAmt,
                                                   lNPrm="",
                                                   lNIndemLmt="",
                                                   lNSeqNo="7",
                                                   lNDductRate="0.2",
                                                   s30="",
                                                   lNVhlActVal=lNAmt,
                                                   lNLiabDaysLmt="",
                                                   lNRate="2",
                                                   lNPerAmt="",
                                                   s29="",
                                                   lCCvrgNo="036007",
                                                   lCDductMrk=lCDductMrk)
        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + carFirePremium
        else:
            dataObjVoList = dataObjVoList + "," + carFirePremium

    if insuranceType.get("engineWadingPremium", "0") == "1":
        engineWadingPremium = copy.deepcopy(attributeVoList)
        engineWadingPremium = Template(engineWadingPremium)
        lCDductMrk = ""
        if insuranceType.get("engineWadingBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        engineWadingPremium = engineWadingPremium.substitute(index="12",
                                                             lCIndemLmtLvl="",
                                                             lNBasePrm="",
                                                             lNAmt="",
                                                             lNPrm="",
                                                             lNIndemLmt="",
                                                             lNSeqNo="12",
                                                             lNDductRate="0.2",
                                                             s30="",
                                                             lNVhlActVal="",
                                                             lNLiabDaysLmt="",
                                                             lNRate="2",
                                                             lNPerAmt="",
                                                             s29="",
                                                             lCCvrgNo="036012",
                                                             lCDductMrk=lCDductMrk)

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + engineWadingPremium
        else:
            dataObjVoList = dataObjVoList + "," + engineWadingPremium

    if insuranceType.get("carTheftPremium", "0") == "1":
        carTheftPremium = copy.deepcopy(attributeVoList)
        carTheftPremium = Template(carTheftPremium)
        lCDductMrk = ""
        if insuranceType.get("carTheftBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        carTheftPremium = carTheftPremium.substitute(index="5",
                                                     lCIndemLmtLvl="",
                                                     lNBasePrm="",
                                                     lNAmt=lNAmt,
                                                     lNPrm="",
                                                     lNIndemLmt="",
                                                     lNSeqNo="5",
                                                     lNDductRate="0.2",
                                                     s30="",
                                                     lNVhlActVal=lNAmt,
                                                     lNLiabDaysLmt="",
                                                     lNRate="0",
                                                     lNPerAmt="",
                                                     s29="",
                                                     lCCvrgNo="036005",
                                                     lCDductMrk=lCDductMrk)

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + carTheftPremium
        else:
            dataObjVoList = dataObjVoList + "," + carTheftPremium

    # # 车辆损失保险
    if insuranceType.get("carDamagePremium", "0") == "1":
        carDamagePremium = copy.deepcopy(attributeVoList)
        carDamagePremium = Template(carDamagePremium)
        lCDductMrk = ""
        if insuranceType.get("carDamageBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        carDamagePremium = carDamagePremium.substitute(index="1",
                                                       lCIndemLmtLvl="",
                                                       lNBasePrm="",
                                                       lNAmt=lNAmt,
                                                       lNPrm="",
                                                       lNIndemLmt="",
                                                       lNSeqNo="1",
                                                       lNDductRate="0.15",
                                                       s30="",
                                                       lNVhlActVal=lNAmt,
                                                       lNLiabDaysLmt="",
                                                       lNRate="0",
                                                       lNPerAmt="",
                                                       s29="",
                                                       lCCvrgNo="036001",
                                                       lCDductMrk=lCDductMrk)

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + carDamagePremium
        else:
            dataObjVoList = dataObjVoList + "," + carDamagePremium

    # 第三方责任险
    if insuranceType.get("otherHurtPremium", {}).get("isCheck", "0") == "1":
        otherHurtPremium = copy.deepcopy(attributeVoList)
        otherHurtPremium = Template(otherHurtPremium)
        lCDductMrk = ""
        if insuranceType.get("otherHurtBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        amount1 = insuranceType.get("otherHurtPremium", {}).get("Amount", "500000")
        otherHurtPremium = otherHurtPremium.substitute(index="2",
                                                       lCIndemLmtLvl="306006009",
                                                       lNBasePrm="",
                                                       lNAmt=amount1,
                                                       lNPrm="",
                                                       lNIndemLmt=amount1,
                                                       lNSeqNo="2",
                                                       lNDductRate="0.15",
                                                       s30="",
                                                       lNVhlActVal="",
                                                       lNLiabDaysLmt="",
                                                       lNRate="",
                                                       lNPerAmt="",
                                                       s29="",
                                                       lCCvrgNo="036002",
                                                       lCDductMrk=lCDductMrk)

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + otherHurtPremium
        else:
            dataObjVoList = dataObjVoList + "," + otherHurtPremium

    if insuranceType.get("carNickPremium", {}).get("isCheck", "0") == "1":
        carNickPremium = copy.deepcopy(attributeVoList)
        carNickPremium = Template(carNickPremium)
        lCDductMrk = ""
        if insuranceType.get("carNickBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        amount2 = insuranceType.get("carNickPremium", {}).get("Amount", "2000")
        carNickPremium = carNickPremium.substitute(index="13",
                                                   lCIndemLmtLvl="N03001001",
                                                   lNBasePrm="",
                                                   lNAmt=amount2,
                                                   lNPrm="",
                                                   lNIndemLmt=amount2,
                                                   lNSeqNo="13",
                                                   lNDductRate="0.15",
                                                   s30="",
                                                   lNVhlActVal="",
                                                   lNLiabDaysLmt="",
                                                   lNRate="",
                                                   lNPerAmt="",
                                                   s29="",
                                                   lCCvrgNo="036013",
                                                   lCDductMrk=lCDductMrk)

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + carNickPremium
        else:
            dataObjVoList = dataObjVoList + "," + carNickPremium

    if insuranceType.get("driverDutyPremium", {}).get("isCheck", "0") == "1":
        driverDutyPremium = copy.deepcopy(attributeVoList)
        driverDutyPremium = Template(driverDutyPremium)
        lCDductMrk = ""
        if insuranceType.get("driverDutyBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        amount3 = insuranceType.get("driverDutyPremium", {}).get("Amount", "10000")
        driverDutyPremium = driverDutyPremium.substitute(index="3",
                                                         lCIndemLmtLvl="",
                                                         lNBasePrm="",
                                                         lNAmt=amount3,
                                                         lNPrm="",
                                                         lNIndemLmt="",
                                                         lNSeqNo="3",
                                                         lNDductRate="0.15",
                                                         s30="",
                                                         lNVhlActVal="",
                                                         lNLiabDaysLmt="1",
                                                         lNRate="0",
                                                         lNPerAmt=amount3,
                                                         s29="",
                                                         lCCvrgNo="036003",
                                                         lCDductMrk=lCDductMrk)

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + driverDutyPremium
        else:
            dataObjVoList = dataObjVoList + "," + driverDutyPremium

    if insuranceType.get("passengerDutyPremium", {}).get("isCheck", "0") == "1":
        passengerDutyPremium = copy.deepcopy(attributeVoList)
        passengerDutyPremium = Template(passengerDutyPremium)
        lCDductMrk = ""
        if insuranceType.get("passengerBenchMarkPremium", "0") == "1":
            lCDductMrk = "369003"
        else:
            lCDductMrk = ""
        amount4 = insuranceType.get("passengerDutyPremium", {}).get("Amount", "10000")
        steats2 = str(seats - 1)
        amount5 = str(int(amount4) * int(steats2))

        passengerDutyPremium = passengerDutyPremium.substitute(index="4",
                                                               lCIndemLmtLvl="",
                                                               lNBasePrm="",
                                                               lNAmt=amount5,
                                                               lNPrm="",
                                                               lNIndemLmt="",
                                                               lNSeqNo="4",
                                                               lNDductRate="0.15",
                                                               s30="",
                                                               lNVhlActVal="",
                                                               lNLiabDaysLmt=steats2,
                                                               lNRate="0",
                                                               lNPerAmt=amount4,
                                                               s29="",
                                                               lCCvrgNo="036004",
                                                               lCDductMrk=lCDductMrk)

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + passengerDutyPremium
        else:
            dataObjVoList = dataObjVoList + "," + passengerDutyPremium

    # 交通强制险
    if insuranceType.get("compulsoryInsurance", "1") == "1":
        compulsoryInsurance = copy.deepcopy(attributeVoList)
        compulsoryInsurance = Template(compulsoryInsurance)
        compulsoryInsurance = compulsoryInsurance.substitute(index="21",
                                                             lCIndemLmtLvl="",
                                                             lNBasePrm="",
                                                             lNAmt="122000",
                                                             lNPrm="",
                                                             lNIndemLmt="",
                                                             lNSeqNo="21",
                                                             lNDductRate="",
                                                             s30="",
                                                             lNVhlActVal="",
                                                             lNLiabDaysLmt="",
                                                             lNRate="0",
                                                             lNPerAmt="",
                                                             s29="",
                                                             lCCvrgNo="033201",
                                                             lCDductMrk="")

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + compulsoryInsurance
        else:
            dataObjVoList = dataObjVoList + "," + compulsoryInsurance

    # 指定修理厂
    if insuranceType.get("repairFactoryPremium", {}).get("isCheck", "0") == "1":
        rate = insuranceType.get("repairFactoryPremium", {}).get("rate", "15")
        rate = str(float(15) / 100)
        repairFactoryPremium = copy.deepcopy(attributeVoList)
        repairFactoryPremium = Template(repairFactoryPremium)
        repairFactoryPremium = repairFactoryPremium.substitute(index="22",
                                                               lCIndemLmtLvl="",
                                                               lNBasePrm="",
                                                               lNAmt="",
                                                               lNPrm="",
                                                               lNIndemLmt="",
                                                               lNSeqNo="22",
                                                               lNDductRate="",
                                                               s30="",
                                                               lNVhlActVal="",
                                                               lNLiabDaysLmt="",
                                                               lNRate=rate,
                                                               lNPerAmt="",
                                                               s29="",
                                                               lCCvrgNo="036022",
                                                               lCDductMrk="")

        if dataObjVoList.replace("\n", "").replace(" ", "")[-1] == "[":
            dataObjVoList = dataObjVoList + repairFactoryPremium
        else:
            dataObjVoList = dataObjVoList + "," + repairFactoryPremium

    dataObjVoList = dataObjVoList + "]"
    return dataObjVoList.replace("\n", "").replace(" ", "")


if __name__ == "__main__":
    insuranceType = {
        'compulsoryInsurance': "1",  # 交通事故强制责任险
        'nAggTax': '1',  # 车船税
        "repairFactoryPremium": {"rate": "15", "isCheck": "1"},
        'otherHurtPremium': {"isCheck": "1", "Amount": "500000"},  # 第三者责任保险
        'carNickPremium': {"isCheck": "1", "Amount": "2000"},  # 车身划痕损失险
        'driverDutyPremium': {"isCheck": "1", "Amount": "10000"},  # 车上人员责任保险（司机）
        'passengerDutyPremium': {"isCheck": "1", "Amount": "10000"},  # 车上人员责任保险（乘客）

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

    print get_insurance_type(insuranceType, "8888.00", "5")
