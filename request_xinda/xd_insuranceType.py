# -*- coding:utf-8 -*-
__author__ = 'weikai'
from string import Template
import copy
from xd_parse import format_number


def get_xd_insurance(insuranceType, permium_dict):
    body = '''  &itemKind_FlagBI=
                &withdraw_FlagBI=
                &itemKindNoBI=${itemKindNoBI}
                &kindShortRateBI=
                &mS_FlagBI=${mS_FlagBI}
                &itemKindFlag6FlagBI=
                &itemKindFlag5BI=
                &kindCodeBI=${kindCodeBI}
                &kindNameBI=${kindNameBI}
                &modelBI=${modelBI}
                &q3ValueBI=
                &valueTitleBI=每次事故绝对免赔额
                &valueBI=0
                &deductibleRate1TitleBI=绝对免赔系数
                &deductibleRate1BI=1
                &riskLevelTitleBI=绝对免赔率保费优待特约
                &riskLevelBI=0
                &lastCompanyTitleBI=原责任公司
                &lastCompanyBI=1
                &lastAmountTitleBI=原责任限额
                &lastAmountBI=
                &totalProfit1BI=${totalProfit1BI}
                &totalProfit2BI=${totalProfit2BI}
                &itemKind_StartDateBI=
                &itemKind_EndDateBI=
                &itemKindCalculateFlagBI=${itemKindCalculateFlagBI}
                &itemKindFlag3To4BI=
                &attachFlagBI=${attachFlagBI}
                &itemKindFlag5FlagBI=${itemKindFlag5FlagBI}
                &deductibleBI=0
                &deductibleRateBI=0
                &currencyBI=CNY
                &currencyNameBI=人民币
                &currencyNameMainBI=人民币
                &exchangeRateMainBI=
                &preUnitAmountNameBI=
                &unitAmountBI=${unitAmountBI}
                &unitAmountNameBI=元/座
                &quantityBI=${quantityBI}
                &quantityNameBI=座
                &amountBI=${amountBI}
                &basePremiumBI=${basePremiumBI}
                &basePureRiskPremiumBI=
                &rateBI=
                &benchMarkPremiumBI=
                &additionalCostRateBI=${additionalCostRateBI}
                &standardPremiumBI=
                &discountBI=${discountBI}

                ${checkboxChooselist}

                &channelRateBI=${channelRateBI}
                &adjustRateBI=${adjustRateBI}
                ${RateFactorsImfTemp}
                &premiumRateBI=0.00%
                &premiumBI=
                &noTaxPremiumBI=
                &taxfeeBI=
                &taxflagBI=
                &taxrateBI=
                '''

    seats = float(permium_dict['vehicle']['seatCountBC'])
    RateFactorsImfTemp = permium_dict.get("Rules", {}).get("RateFactorslist", "")
    additionalCostRateBI = permium_dict.get("Rules", {}).get("additionalCostRateBI", "")
    caramount = permium_dict.get("actualValue", {}).get("actualValueBC", "0")  # 车辆价值
    caramount = format_number(caramount)
    adjustRateBI = permium_dict.get("Rules", {}).get("sumAdjustRateBI", "")
    channelRateBI = permium_dict.get("Rules", {}).get("sumChannelRateBI", "")
    modelBI = ""
    # 获取客户分类按钮 请求保费返回的消息
    checkboxChooselist = permium_dict.get("premium", {}).get("profitDetailEncodeBI_list", [])

    otherHurtPremium = otherHurtBenchMarkPremium = carDamagePremium \
        = carDamageBenchMarkPremium = driverDutyPremium = driverDutyBenchMarkPremium = passengerDutyPremium \
        = passengerBenchMarkPremium = carTheftPremium = carTheftBenchMarkPremium = carNickPremium \
        = carNickBenchMarkPremium = glassBrokenPremium = carFirePremium = carFireBrokenBenchMarkPremium \
        = engineWadingPremium = engineWadingBenchMarkPremium = repairFactoryPremium = ""
    dataObjVoList = ""

    if insuranceType.get("engineWadingPremium", "0") == "1":
        engineWadingPremium = copy.deepcopy(body)
        engineWadingPremium = Template(engineWadingPremium)
        engineWadingPremium = engineWadingPremium.substitute(itemKindNoBI="19", mS_FlagBI="S", kindCodeBI="X3",
                                                             kindNameBI="发动机涉水损失险", totalProfit1BI="0",
                                                             totalProfit2BI='0', itemKindCalculateFlagBI="N",
                                                             attachFlagBI="A", itemKindFlag5FlagBI="1", unitAmountBI="",
                                                             amountBI="", basePremiumBI="0",
                                                             additionalCostRateBI=additionalCostRateBI,
                                                             discountBI="1.0", channelRateBI=channelRateBI,
                                                             adjustRateBI=adjustRateBI, quantityBI="",
                                                             RateFactorsImfTemp=RateFactorsImfTemp, modelBI=modelBI,
                                                             checkboxChooselist=get_CustomerTypeFlag(checkboxChooselist,
                                                                                                     "发动机涉水损失险"))
        # dataObjVoList = dataObjVoList + engineWadingPremium
        if insuranceType.get("engineWadingBenchMarkPremium", "0") == "1":
            engineWadingBenchMarkPremium = copy.deepcopy(body)
            engineWadingBenchMarkPremium = Template(engineWadingBenchMarkPremium)
            engineWadingBenchMarkPremium = engineWadingBenchMarkPremium.substitute(itemKindNoBI="20", mS_FlagBI="S",
                                                                                   kindCodeBI="MX3",
                                                                                   kindNameBI="不计免赔率险(发动机涉水损失险)",
                                                                                   totalProfit1BI="0",
                                                                                   totalProfit2BI='0',
                                                                                   itemKindCalculateFlagBI="N",
                                                                                   attachFlagBI="A",
                                                                                   itemKindFlag5FlagBI="0",
                                                                                   unitAmountBI="",
                                                                                   amountBI="", basePremiumBI="0",
                                                                                   additionalCostRateBI=additionalCostRateBI,
                                                                                   discountBI="1.0",
                                                                                   channelRateBI=channelRateBI,
                                                                                   adjustRateBI=adjustRateBI,
                                                                                   quantityBI="",
                                                                                   RateFactorsImfTemp=RateFactorsImfTemp,
                                                                                   modelBI=modelBI,
                                                                                   checkboxChooselist=get_CustomerTypeFlag(
                                                                                       checkboxChooselist,
                                                                                       "不计免赔率险(发动机涉水损失险)"))
            # dataObjVoList = dataObjVoList + engineWadingBenchMarkPremium

    if insuranceType.get("glassBrokenPremium", "0") == "1":
        # modelBI 1 国产 2进口
        glassBrokenPremium = copy.deepcopy(body)
        glassBrokenPremium = Template(glassBrokenPremium)
        RateFactorsImfTemp_glass = RateFactorsImfTemp.replace("UndwrtFactor_KindCodeBI=B", "UndwrtFactor_KindCodeBI=F")
        glassBrokenPremium = glassBrokenPremium.substitute(itemKindNoBI="13", mS_FlagBI="S", kindCodeBI="F",
                                                           kindNameBI="玻璃单独破碎险", totalProfit1BI="",
                                                           totalProfit2BI='', itemKindCalculateFlagBI="N",
                                                           attachFlagBI="A", itemKindFlag5FlagBI="0",
                                                           unitAmountBI="0.00",
                                                           amountBI="0.00", basePremiumBI="",
                                                           additionalCostRateBI=additionalCostRateBI, discountBI="1.0",
                                                           channelRateBI=channelRateBI,
                                                           adjustRateBI=adjustRateBI, quantityBI="",
                                                           RateFactorsImfTemp=RateFactorsImfTemp_glass, modelBI="1",
                                                           checkboxChooselist=get_CustomerTypeFlag(
                                                               checkboxChooselist,
                                                               "玻璃单独破碎险"))

        # dataObjVoList = dataObjVoList + glassBrokenPremium

    if insuranceType.get("carFirePremium", "0") == "1":
        carFirePremium = copy.deepcopy(body)
        carFirePremium = Template(carFirePremium)
        carFirePremium = carFirePremium.substitute(itemKindNoBI="15", mS_FlagBI="S", kindCodeBI="Z", kindNameBI="自燃损失险",
                                                   totalProfit1BI="0",
                                                   totalProfit2BI='0', itemKindCalculateFlagBI="N", attachFlagBI="A",
                                                   itemKindFlag5FlagBI="1", unitAmountBI="",
                                                   amountBI=caramount, basePremiumBI="",
                                                   additionalCostRateBI=additionalCostRateBI, discountBI="1.0",
                                                   channelRateBI=channelRateBI,
                                                   adjustRateBI=adjustRateBI, quantityBI="",
                                                   RateFactorsImfTemp=RateFactorsImfTemp, modelBI=modelBI,
                                                   checkboxChooselist=get_CustomerTypeFlag(
                                                       checkboxChooselist,
                                                       "自燃损失险"))
        # dataObjVoList = dataObjVoList + carFirePremium

        if insuranceType.get("carFireBrokenBenchMarkPremium", "0") == "1":
            carFireBrokenBenchMarkPremium = copy.deepcopy(body)
            carFireBrokenBenchMarkPremium = Template(carFireBrokenBenchMarkPremium)
            carFireBrokenBenchMarkPremium = carFireBrokenBenchMarkPremium.substitute(itemKindNoBI="16", mS_FlagBI="S",
                                                                                     kindCodeBI="MZ",
                                                                                     kindNameBI="不计免赔率险(自燃损失险)",
                                                                                     totalProfit1BI="0",
                                                                                     totalProfit2BI='0',
                                                                                     itemKindCalculateFlagBI="N",
                                                                                     attachFlagBI="A",
                                                                                     itemKindFlag5FlagBI="0",
                                                                                     unitAmountBI="",
                                                                                     amountBI="", basePremiumBI="0",
                                                                                     additionalCostRateBI=additionalCostRateBI,
                                                                                     discountBI="1.0",
                                                                                     channelRateBI=channelRateBI,
                                                                                     adjustRateBI=adjustRateBI,
                                                                                     quantityBI="",
                                                                                     RateFactorsImfTemp=RateFactorsImfTemp,
                                                                                     modelBI=modelBI,
                                                                                     checkboxChooselist=get_CustomerTypeFlag(
                                                                                         checkboxChooselist,
                                                                                         "不计免赔率险(自燃损失险)"))
            # dataObjVoList = dataObjVoList + carFireBrokenBenchMarkPremium
    if insuranceType.get("carTheftPremium", "0") == "1":
        carTheftPremium = copy.deepcopy(body)
        carTheftPremium = Template(carTheftPremium)

        carTheftPremium = carTheftPremium.substitute(itemKindNoBI="09", mS_FlagBI="M", kindCodeBI="G1",
                                                     kindNameBI="机动车盗抢保险", totalProfit1BI="",
                                                     totalProfit2BI='', itemKindCalculateFlagBI="N", attachFlagBI="",
                                                     itemKindFlag5FlagBI="1", unitAmountBI="0.00",
                                                     amountBI=caramount, basePremiumBI="",
                                                     additionalCostRateBI=additionalCostRateBI, discountBI="",
                                                     channelRateBI=channelRateBI,
                                                     adjustRateBI=adjustRateBI, quantityBI="",
                                                     RateFactorsImfTemp=RateFactorsImfTemp, modelBI=modelBI,
                                                     checkboxChooselist=get_CustomerTypeFlag(checkboxChooselist,
                                                                                             "机动车盗抢保险"))
        # dataObjVoList = dataObjVoList + carTheftPremium
        if insuranceType.get("carTheftBenchMarkPremium", "0") == "1":
            carTheftBenchMarkPremium = copy.deepcopy(body)
            carTheftBenchMarkPremium = Template(carTheftBenchMarkPremium)

            carTheftBenchMarkPremium = carTheftBenchMarkPremium.substitute(itemKindNoBI="10", mS_FlagBI="S",
                                                                           kindCodeBI="MG1", kindNameBI="不计免赔率险(盗抢险)",
                                                                           totalProfit1BI="0",
                                                                           totalProfit2BI='0',
                                                                           itemKindCalculateFlagBI="N",
                                                                           attachFlagBI="G1", itemKindFlag5FlagBI="0",
                                                                           unitAmountBI="",
                                                                           amountBI="", basePremiumBI="0",
                                                                           additionalCostRateBI=additionalCostRateBI,
                                                                           discountBI="", channelRateBI=channelRateBI,
                                                                           adjustRateBI=adjustRateBI, quantityBI="",
                                                                           RateFactorsImfTemp=RateFactorsImfTemp,
                                                                           modelBI=modelBI,
                                                                           checkboxChooselist=get_CustomerTypeFlag(
                                                                               checkboxChooselist, "不计免赔率险(盗抢险)"))
            # dataObjVoList = dataObjVoList + carTheftBenchMarkPremium



    # # 车辆损失保险
    if insuranceType.get("carDamagePremium", "0") == "1":
        carDamagePremium = copy.deepcopy(body)
        carDamagePremium = Template(carDamagePremium)
        carDamagePremium = carDamagePremium.substitute(itemKindNoBI="03", mS_FlagBI="M", kindCodeBI="A",
                                                       kindNameBI="机动车损失保险", totalProfit1BI="",
                                                       totalProfit2BI='', itemKindCalculateFlagBI="Y", attachFlagBI="0",
                                                       itemKindFlag5FlagBI="1", unitAmountBI="0.00",
                                                       amountBI=caramount, basePremiumBI="",
                                                       additionalCostRateBI=additionalCostRateBI, discountBI="",
                                                       channelRateBI=channelRateBI,
                                                       adjustRateBI=adjustRateBI, quantityBI="",
                                                       RateFactorsImfTemp=RateFactorsImfTemp, modelBI=modelBI,
                                                       checkboxChooselist=get_CustomerTypeFlag(checkboxChooselist,
                                                                                               "机动车损失保险"))
        # dataObjVoList = dataObjVoList + carDamagePremium
        if insuranceType.get("carDamageBenchMarkPremium", "0") == "1":
            carDamageBenchMarkPremium = copy.deepcopy(body)
            carDamageBenchMarkPremium = Template(carDamageBenchMarkPremium)
            carDamageBenchMarkPremium = carDamageBenchMarkPremium.substitute(itemKindNoBI="04", mS_FlagBI="S",
                                                                             kindCodeBI="MA",
                                                                             kindNameBI="不计免赔率险(机动车损失险)",
                                                                             totalProfit1BI="0",
                                                                             totalProfit2BI='0',
                                                                             itemKindCalculateFlagBI="N",
                                                                             attachFlagBI="A", itemKindFlag5FlagBI="0",
                                                                             unitAmountBI="",
                                                                             amountBI="", basePremiumBI="0",
                                                                             additionalCostRateBI=additionalCostRateBI,
                                                                             discountBI="1.0",
                                                                             channelRateBI=channelRateBI,
                                                                             adjustRateBI=adjustRateBI, quantityBI="",
                                                                             RateFactorsImfTemp=RateFactorsImfTemp,
                                                                             modelBI=modelBI,
                                                                             checkboxChooselist=get_CustomerTypeFlag(
                                                                                 checkboxChooselist, "不计免赔率险(机动车损失险)"))
            # dataObjVoList = dataObjVoList + carDamageBenchMarkPremium


    # 第三方责任险
    if insuranceType.get("otherHurtPremium", {}).get("isCheck", "0") == "1":
        amount1 = insuranceType.get("otherHurtPremium", {}).get("Amount", "500000")
        otherHurtPremium = copy.deepcopy(body)
        otherHurtPremium = Template(otherHurtPremium)
        amount1 = format_number(amount1)
        otherHurtPremium = otherHurtPremium.substitute(itemKindNoBI="01", mS_FlagBI="M", kindCodeBI="B",
                                                       kindNameBI="机动车第三者责任保险", totalProfit1BI="",
                                                       totalProfit2BI='', itemKindCalculateFlagBI="Y", attachFlagBI="",
                                                       itemKindFlag5FlagBI="1", unitAmountBI="0.00",
                                                       amountBI=amount1, basePremiumBI="",
                                                       additionalCostRateBI=additionalCostRateBI, discountBI="",
                                                       channelRateBI=channelRateBI,
                                                       adjustRateBI=adjustRateBI, RateFactorsImfTemp=RateFactorsImfTemp,
                                                       quantityBI="", modelBI=modelBI,
                                                       checkboxChooselist=get_CustomerTypeFlag(checkboxChooselist,
                                                                                               "机动车第三者责任保险"))
        # dataObjVoList = dataObjVoList + otherHurtPremium
        if insuranceType.get("otherHurtBenchMarkPremium", "0") == "1":
            otherHurtBenchMarkPremium = copy.deepcopy(body)
            otherHurtBenchMarkPremium = Template(otherHurtBenchMarkPremium)
            otherHurtBenchMarkPremium = otherHurtBenchMarkPremium.substitute(itemKindNoBI="02", mS_FlagBI="S",
                                                                             kindCodeBI="MB",
                                                                             kindNameBI="不计免赔率险(机动车第三者责任险)",
                                                                             totalProfit1BI="0",
                                                                             totalProfit2BI='0',
                                                                             itemKindCalculateFlagBI="N",
                                                                             attachFlagBI="B", itemKindFlag5FlagBI="0",
                                                                             unitAmountBI="",
                                                                             amountBI="", basePremiumBI="0",
                                                                             additionalCostRateBI=additionalCostRateBI,
                                                                             discountBI="1.0",
                                                                             channelRateBI=channelRateBI,
                                                                             adjustRateBI=adjustRateBI,
                                                                             RateFactorsImfTemp=RateFactorsImfTemp,
                                                                             quantityBI="", modelBI=modelBI,
                                                                             checkboxChooselist=get_CustomerTypeFlag(
                                                                                 checkboxChooselist,
                                                                                 "不计免赔率险(机动车第三者责任险)"))
            # dataObjVoList = dataObjVoList + otherHurtBenchMarkPremium

    if insuranceType.get("carNickPremium", {}).get("isCheck", "0") == "1":
        carNickPremium = copy.deepcopy(body)
        carNickPremium = Template(carNickPremium)
        amount2 = insuranceType.get("carNickPremium", {}).get("Amount", "2000")
        amount2 = format_number(amount2)
        carNickPremium = carNickPremium.substitute(itemKindNoBI="11", mS_FlagBI="S", kindCodeBI="L",
                                                   kindNameBI="车身划痕损失险", totalProfit1BI="0",
                                                   totalProfit2BI='0', itemKindCalculateFlagBI="N", attachFlagBI="A",
                                                   itemKindFlag5FlagBI="1", unitAmountBI="",
                                                   amountBI=amount2, basePremiumBI="0",
                                                   additionalCostRateBI=additionalCostRateBI, discountBI="",
                                                   channelRateBI=channelRateBI,
                                                   adjustRateBI=adjustRateBI, RateFactorsImfTemp=RateFactorsImfTemp,
                                                   quantityBI="", modelBI=modelBI,
                                                   checkboxChooselist=get_CustomerTypeFlag(checkboxChooselist,
                                                                                           "车身划痕损失险"))

        # dataObjVoList = dataObjVoList + carNickPremium

        if insuranceType.get("carNickBenchMarkPremium", "0") == "1":
            carNickBenchMarkPremium = copy.deepcopy(body)
            carNickBenchMarkPremium = Template(carNickBenchMarkPremium)
            carNickBenchMarkPremium = carNickBenchMarkPremium.substitute(itemKindNoBI="12", mS_FlagBI="S",
                                                                         kindCodeBI="ML", kindNameBI="不计免赔率险(车身划痕损失险)",
                                                                         totalProfit1BI="0",
                                                                         totalProfit2BI='0',
                                                                         itemKindCalculateFlagBI="N", attachFlagBI="A",
                                                                         itemKindFlag5FlagBI="0", unitAmountBI="",
                                                                         amountBI="", basePremiumBI="0",
                                                                         additionalCostRateBI=additionalCostRateBI,
                                                                         discountBI="", channelRateBI=channelRateBI,
                                                                         adjustRateBI=adjustRateBI,
                                                                         RateFactorsImfTemp=RateFactorsImfTemp,
                                                                         quantityBI="", modelBI=modelBI,
                                                                         checkboxChooselist=get_CustomerTypeFlag(
                                                                             checkboxChooselist, "不计免赔率险(车身划痕损失险)"))
            # dataObjVoList = dataObjVoList + carNickBenchMarkPremium

    if insuranceType.get("driverDutyPremium", {}).get("isCheck", "0") == "1":
        driverDutyPremium = copy.deepcopy(body)
        driverDutyPremium = Template(driverDutyPremium)
        amount3 = insuranceType.get("driverDutyPremium", {}).get("Amount", "10000")
        amount3 = format_number(amount3)
        driverDutyPremium = driverDutyPremium.substitute(itemKindNoBI="05", mS_FlagBI="M", kindCodeBI="D3",
                                                         kindNameBI="机动车车上人员责任保险（驾驶员）", totalProfit1BI="",
                                                         totalProfit2BI='', itemKindCalculateFlagBI="Y",
                                                         attachFlagBI="", itemKindFlag5FlagBI="1", unitAmountBI=amount3,
                                                         amountBI=amount3, quantityBI="1", basePremiumBI="",
                                                         additionalCostRateBI=additionalCostRateBI, discountBI="",
                                                         channelRateBI=channelRateBI,
                                                         adjustRateBI=adjustRateBI,
                                                         RateFactorsImfTemp=RateFactorsImfTemp, modelBI=modelBI,
                                                         checkboxChooselist=get_CustomerTypeFlag(checkboxChooselist,
                                                                                                 "机动车车上人员责任保险（驾驶员）"))
        # dataObjVoList = dataObjVoList + driverDutyPremium

        if insuranceType.get("driverDutyBenchMarkPremium", "0") == "1":
            driverDutyBenchMarkPremium = copy.deepcopy(body)
            driverDutyBenchMarkPremium = Template(driverDutyBenchMarkPremium)
            driverDutyBenchMarkPremium = driverDutyBenchMarkPremium.substitute(itemKindNoBI="06", mS_FlagBI="S",
                                                                               kindCodeBI="MD3",
                                                                               kindNameBI="不计免赔率险(机动车车上人员责任险（驾驶员）)",
                                                                               totalProfit1BI="0",
                                                                               totalProfit2BI='0',
                                                                               itemKindCalculateFlagBI="N",
                                                                               attachFlagBI="D3",
                                                                               itemKindFlag5FlagBI="0", unitAmountBI="",
                                                                               amountBI="", quantityBI="",
                                                                               basePremiumBI="0",
                                                                               additionalCostRateBI=additionalCostRateBI,
                                                                               discountBI="1.0",
                                                                               channelRateBI=channelRateBI,
                                                                               adjustRateBI=adjustRateBI,
                                                                               RateFactorsImfTemp=RateFactorsImfTemp,
                                                                               modelBI=modelBI,
                                                                               checkboxChooselist=get_CustomerTypeFlag(
                                                                                   checkboxChooselist,
                                                                                   "不计免赔率险(机动车车上人员责任险（驾驶员）)"))
            # dataObjVoList = dataObjVoList + driverDutyBenchMarkPremium

    if insuranceType.get("passengerDutyPremium", {}).get("isCheck", "0") == "1":
        passengerDutyPremium = copy.deepcopy(body)
        passengerDutyPremium = Template(passengerDutyPremium)
        amount4 = insuranceType.get("passengerDutyPremium", {}).get("Amount", "10000")
        steats2 = str(seats - 1)
        amount5 = str(int(amount4) * int(steats2))
        amount4 = format_number(amount4)
        amount5 = format_number(amount5)
        passengerDutyPremium = passengerDutyPremium.substitute(itemKindNoBI="07", mS_FlagBI="M", kindCodeBI="D4",
                                                               kindNameBI="机动车车上人员责任保险（乘客）", totalProfit1BI="",
                                                               totalProfit2BI='', itemKindCalculateFlagBI="Y",
                                                               attachFlagBI="", itemKindFlag5FlagBI="1",
                                                               unitAmountBI=amount4,
                                                               amountBI=amount5, quantityBI=steats2, basePremiumBI="",
                                                               additionalCostRateBI=additionalCostRateBI, discountBI="",
                                                               channelRateBI=channelRateBI,
                                                               adjustRateBI=adjustRateBI,
                                                               RateFactorsImfTemp=RateFactorsImfTemp, modelBI=modelBI,
                                                               checkboxChooselist=get_CustomerTypeFlag(
                                                                   checkboxChooselist, "机动车车上人员责任保险（乘客）"))
        # dataObjVoList = dataObjVoList + passengerDutyPremium

        if insuranceType.get("passengerBenchMarkPremium", "0") == "1":
            passengerBenchMarkPremium = copy.deepcopy(body)
            passengerBenchMarkPremium = Template(passengerBenchMarkPremium)
            passengerBenchMarkPremium = passengerBenchMarkPremium.substitute(itemKindNoBI="08", mS_FlagBI="S",
                                                                             kindCodeBI="MD4",
                                                                             kindNameBI="不计免赔率险(机动车车上人员责任保险（乘客）)",
                                                                             totalProfit1BI="0",
                                                                             totalProfit2BI='0',
                                                                             itemKindCalculateFlagBI="N",
                                                                             attachFlagBI="D4", itemKindFlag5FlagBI="0",
                                                                             unitAmountBI="",
                                                                             amountBI="", quantityBI="",
                                                                             basePremiumBI="0",
                                                                             additionalCostRateBI=additionalCostRateBI,
                                                                             discountBI="1.0",
                                                                             channelRateBI=channelRateBI,
                                                                             adjustRateBI=adjustRateBI,
                                                                             RateFactorsImfTemp=RateFactorsImfTemp,
                                                                             modelBI=modelBI,
                                                                             checkboxChooselist=get_CustomerTypeFlag(
                                                                                 checkboxChooselist,
                                                                                 "不计免赔率险(机动车车上人员责任保险（乘客）)"))
            # dataObjVoList = dataObjVoList + passengerBenchMarkPremium

    # 指定修理厂
    if insuranceType.get("repairFactoryPremium", {}).get("isCheck", "0") == "1":
        rate = insuranceType.get("repairFactoryPremium", {}).get("rate", "15")
        repairFactoryPremium = copy.deepcopy(body)
        repairFactoryPremium = Template(repairFactoryPremium)
        repairFactoryPremium = repairFactoryPremium.substitute(itemKindNoBI="25", mS_FlagBI="S", kindCodeBI="Q4",
                                                               kindNameBI="指定修理厂险", totalProfit1BI="0",
                                                               totalProfit2BI='0', itemKindCalculateFlagBI="N",
                                                               attachFlagBI="A", itemKindFlag5FlagBI="0",
                                                               unitAmountBI="",
                                                               amountBI="", basePremiumBI="0",
                                                               additionalCostRateBI=additionalCostRateBI,
                                                               discountBI="1.0", channelRateBI=channelRateBI,
                                                               adjustRateBI=adjustRateBI, quantityBI="",
                                                               RateFactorsImfTemp=RateFactorsImfTemp, modelBI=modelBI,
                                                               checkboxChooselist=get_CustomerTypeFlag(
                                                                   checkboxChooselist, "指定修理厂险"))

        # dataObjVoList = dataObjVoList + repairFactoryPremium
    dataObjVoList = otherHurtPremium + otherHurtBenchMarkPremium + carDamagePremium \
                    + carDamageBenchMarkPremium + driverDutyPremium + driverDutyBenchMarkPremium + passengerDutyPremium \
                    + passengerBenchMarkPremium + carTheftPremium + carTheftBenchMarkPremium + carNickPremium \
                    + carNickBenchMarkPremium + glassBrokenPremium + carFirePremium + carFireBrokenBenchMarkPremium \
                    + engineWadingPremium + engineWadingBenchMarkPremium + repairFactoryPremium

    return dataObjVoList


def choose_jq_sy(insuranceType):
    '''
    :param insuranceType: 入参险种类型
    :return:选择交强和商业险的情况
    '''
    otherHurtPremium = insuranceType.get("otherHurtPremium", {}).get("isCheck", "0")
    carDamagePremium = insuranceType.get("carDamagePremium", "0")
    carTheftPremium = insuranceType.get("carTheftPremium", "0")
    glassBrokenPremium = insuranceType.get("glassBrokenPremium", "0")
    carFirePremium = insuranceType.get("carFirePremium", "0")
    engineWadingPremium = insuranceType.get("engineWadingPremium", "0")
    passengerDutyPremium = insuranceType.get("passengerDutyPremium", {}).get("isCheck", "0")
    driverDutyPremium = insuranceType.get("driverDutyPremium", {}).get("isCheck", "0")
    carNickPremium = insuranceType.get("carNickPremium", {}).get("isCheck", "0")
    repairFactoryPremium = insuranceType.get("repairFactoryPremium", {}).get("isCheck", "0")

    compulsory_insurance = insuranceType.get("compulsoryInsurance", "0")
    sy_flag = jq_flag = 0
    if otherHurtPremium == "1" or carDamagePremium == "1" or carTheftPremium == "1" \
            or glassBrokenPremium == "1" or carFirePremium == "1" or engineWadingPremium == "1" \
            or passengerDutyPremium == "1" or driverDutyPremium == "1" or carNickPremium == "1" \
            or repairFactoryPremium == "1":
        sy_flag = 1
    if compulsory_insurance == "1":
        jq_flag = 1

    if sy_flag == 1 and jq_flag == 0:
        return "1"  # 只选了商业险
    if sy_flag == 1 and jq_flag == 1:
        return "3"  # 商业交强险全部选了
    if sy_flag == 0 and jq_flag == 1:
        return "2"  # 只选择了交强险


def get_CustomerTypeFlag(coulist, inserancetype):
    # 最后一个请求获取客户分类
    # test = "^0518^1^1^1^B^机动车第三者责任保险^C29^无赔款优待及上年赔款记录^1^无赔款优待-新保或上年发生1次赔款^^0.00^^^^0.00^0.00^"
    if len(coulist) == 0:
        return ""
    c29_str_tmp = ""
    c33_str_tmp = ""
    for i in coulist:
        if (inserancetype in i) and ("C29" in i):
            c29_str_tmp = i
        if (inserancetype in i) and ("C33" in i):
            c33_str_tmp = i
    c29_str_tmp_list = c29_str_tmp.split("^")
    # print json.dumps(test_list, ensure_ascii=False)
    if len(c29_str_tmp_list) != 0:
        checkboxChooseFlagBI = profitDetail_ItemKindNoBI = c29_str_tmp_list[4]
        profitDetailEncodeBI = c29_str_tmp
        profitDetail_KindCodeBI = c29_str_tmp_list[5]
        profitDetail_RiskCodeBI = c29_str_tmp_list[1]
        profitDetail_ProfitCodeBI = c29_str_tmp_list[7]
    c33_str_tmp_list = c33_str_tmp.split("^")
    if len(c29_str_tmp_list) != 0:
        c33checkboxChooseFlagBI = profitDetail_ItemKindNoBI = c33_str_tmp_list[4]
        c33profitDetailEncodeBI = c33_str_tmp
        c33profitDetail_KindCodeBI = c33_str_tmp_list[5]
        c33profitDetail_RiskCodeBI = c33_str_tmp_list[1]
        c33profitDetail_ProfitCodeBI = c33_str_tmp_list[7]

    out = """
    &checkboxChooseFlagBI=${checkboxChooseFlagBI}
    &chooseFlagBI=1
    &profitCodeBI=${profitDetail_ProfitCodeBI}
    &profitRateBI=0.0
    &profitDetail_ItemKindNoBI=${checkboxChooseFlagBI}
    &profitDetail_FieldValueBI=
    &profitDetailEncodeBI=${profitDetailEncodeBI}
    &profitDetail_FlagBI=
    &profitDetail_ConditionCodeBI=
    &profitDetail_KindCodeBI=${profitDetail_KindCodeBI}
    &profitDetail_RiskCodeBI=${profitDetail_RiskCodeBI}
    &profitDetail_ProfitCodeBI=${profitDetail_ProfitCodeBI}

    &checkboxChooseFlagBI=${c33checkboxChooseFlagBI}
    &chooseFlagBI=1
    &profitCodeBI=${c33profitDetail_ProfitCodeBI}
    &profitRateBI=0.0
    &profitDetail_ItemKindNoBI=${c33checkboxChooseFlagBI}
    &profitDetail_FieldValueBI=
    &profitDetailEncodeBI=${c33profitDetailEncodeBI}
    &profitDetail_FlagBI=
    &profitDetail_ConditionCodeBI=
    &profitDetail_KindCodeBI=${c33profitDetail_KindCodeBI}
    &profitDetail_RiskCodeBI=${c33profitDetail_RiskCodeBI}
    &profitDetail_ProfitCodeBI=${c33profitDetail_ProfitCodeBI}
    """
    result = Template(out)
    result = result.substitute(checkboxChooseFlagBI=checkboxChooseFlagBI,
                               profitDetail_KindCodeBI=profitDetail_KindCodeBI,
                               profitDetail_RiskCodeBI=profitDetail_RiskCodeBI,
                               profitDetail_ProfitCodeBI=profitDetail_ProfitCodeBI,
                               profitDetailEncodeBI=profitDetailEncodeBI,

                               c33checkboxChooseFlagBI=c33checkboxChooseFlagBI,
                               c33profitDetail_ProfitCodeBI=c33profitDetail_ProfitCodeBI,
                               c33profitDetail_KindCodeBI=c33profitDetail_KindCodeBI,
                               c33profitDetail_RiskCodeBI=c33profitDetail_RiskCodeBI,
                               c33profitDetailEncodeBI=c33profitDetailEncodeBI
                               )
    return result


if __name__ == "__main__":
    insuranceType = {
        'driverDutyPremium': {
            'Amount': '10000',
            'isCheck': '1'
        },
        'carDamagePremium': '1',
        'otherHurtBenchMarkPremium': '1',
        'passengerBenchMarkPremium': '1',
        'compulsoryInsurance': '1',
        'carFirePremium': '0',
        'otherHurtPremium': {
            'Amount': '500000',
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
            'isCheck': '1'
        },
        'driverDutyBenchMarkPremium': '1',
        'carTheftBenchMarkPremium': '1',
        'carNickPremium': {
            'Amount': '',
            'isCheck': '0'
        }}

    print(choose_jq_sy(insuranceType))
