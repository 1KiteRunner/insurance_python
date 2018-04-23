# -*- coding:utf-8 -*-
__author__ = 'weikai'
import re, json, locale, sys
from bs4 import BeautifulSoup
from common.log import Logger
from common.business.insurance_premium import get_car_main_premium, get_car_fire_premium, get_car_nick_premium
from common.business.insurance_premium import BenchMarkPremium

reload(sys)
sys.setdefaultencoding('utf8')
log = Logger()


def parse_vin_car(html):
    try:
        permium_dict = {}
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find(name="table")
        trs = table.find_all("tr", attrs={"class": "listtrd"})
        c = sorted(trs, key=lambda x: int(
            float(x.find_all(name='td')[10].get_text().replace('\r', '').replace('\n', '').replace('\t', ''))),
                   reverse=False)
        car_tds = c[0].find_all(name='td')
        brandNameBC = car_tds[0].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 车型名称
        carclassName = car_tds[1].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 车型别名
        jqName = car_tds[4].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 交强险名称
        syName = car_tds[5].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 商业险名称
        seatCountBC = car_tds[6].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 座位数
        cartonnage = car_tds[9].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 吨位
        compromisePrice = car_tds[12].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 新车购置价
        completeKerbMassNewBC = car_tds[17].get_text().replace('\r', '').replace('\n', '').replace('\t',
                                                                                                   '')  # 整备质量（最大值）
        exhaustScaleBC = car_tds[15].get_text().replace('\r', '').replace('\n', '').replace('\t', '')  # 排量

        car_list = c[0].attrs['onclick'].replace("submitForm", "").replace("(", "").replace(");", "").replace("\r\n ",
                                                                                                              "").replace(
            "'", "").split(",")
        permium_dict['exhaustScaleBC'] = exhaustScaleBC
        permium_dict['jqName'] = jqName
        permium_dict['syName'] = syName
        permium_dict['completeKerbMassNewBC'] = completeKerbMassNewBC
        permium_dict['compromisePrice'] = compromisePrice
        permium_dict['seatCountBC'] = seatCountBC
        permium_dict['brandNameBC'] = brandNameBC
        permium_dict['carclassName'] = carclassName
        permium_dict['cartonnage'] = cartonnage
        permium_dict['VEHICLEMODEL'] = car_list[0]
        permium_dict['BrandCode'] = car_list[12]
        log.info(json.dumps(permium_dict, ensure_ascii=False))
        return permium_dict
    except Exception as e:
        log.error(e)


def xd_parse_actualValue(html):
    permium_dict = {}
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find(name="table")
    trs = table.find_all("tr", attrs={"class": "listodd"})
    alcar = trs[0].attrs['onclick'].replace("submitForm", "").replace("(", "").replace(");", "").replace("\r\n ",
                                                                                                         "").replace(
        "'", "").split(",")

    actualValueBC = \
        re.findall(re.compile('<input type="hidden" name="purchasePriceSign" value="(.+?)"/>'), html)[0]
    riskPremium = re.findall(re.compile('<td>(.+?)</td>'), html)[7]
    carKind = re.findall(re.compile('<td>(.+?)</td>'), html)[5]

    searchSequenceNoBC = ""
    if len(alcar) != 0:
        searchSequenceNoBC = alcar[3]
        modelCodeBC = alcar[1]
    return {"actualValueBC": actualValueBC, "printBrandNameBC": actualValueBC, "riskPremium": riskPremium,
            "carKind": carKind, 'searchSequenceNoBC': searchSequenceNoBC, "modelCodeBC": modelCodeBC}


def parse_vehicle_info(html):
    try:
        permium_dict = {}
        # 解析车管信息
        carOwnerBC = re.findall(re.compile("parent.fraInterface.fm.carOwnerBC.value = '(.+?)';"), html)[0]  # 车主姓名
        enrollDateBC = re.findall(re.compile("parent.fraInterface.fm.enrollDateBC.value = '(.+?)';"), html)[0]  # 初登日期
        licenseCategoryBC = re.findall(re.compile("parent.fraInterface.fm.licenseCategoryBC.value = '(.+?)';"), html)[0]
        countryNatureBC = re.findall(re.compile("parent.fraInterface.fm.countryNatureBC.value = '(.+?)';"), html)[0]
        tonCountBC = re.findall(re.compile("parent.fraInterface.fm.tonCountBC.value = '(.+?)';"), html)[0]
        haulageCI = re.findall(re.compile("parent.fraInterface.fm.haulageCI.value = '(.+?)';"), html)[0]
        if tonCountBC == "0.0" or tonCountBC == "":
            tonCountBC = str(float(haulageCI) / 1000)
        EngineNo = re.findall(re.compile("parent.fraInterface.fm.engineNoBC.value = '(.+?)';"), html)[0]
        pmUseNatureCodeBC = re.findall(re.compile("parent.fraInterface.fm.pmUseNatureCodeBC.value = '(.+?)';"), html)[
            0]  # 使用性质

        seatCountBC = re.findall(re.compile("parent.fraInterface.fm.seatCountBC.value = '(.+?)';"), html)  # 座位数
        # 货车或者其他有可能座位数不存在
        if len(seatCountBC) != 0:
            seatCountBC = seatCountBC[0]
        else:
            seatCountBC = "0"
        madeFactoryBI = re.findall(re.compile("parent.fraInterface.fm.madeFactoryBI.value = '(.+?)';"), html)[0]  # 生产商
        vehicle_modelCI = re.findall(re.compile("parent.fraInterface.fm.vehicle_modelCI.value = '(.+?)';"), html)[
            0]  # 车辆型号
        vehicleBrandTemp = re.findall(re.compile("parent.fraInterface.fm.vehicleBrandTemp.value = '(.+?)';"), html)[
            0]  #
        vehicle_brand_2CI = re.findall(re.compile("parent.fraInterface.fm.vehicle_brand_2CI.value = '(.+?)';"), html)  #
        if len(vehicle_brand_2CI) == 0:
            vehicle_brand_2CI = \
                re.findall(re.compile("parent.fraInterface.fm.vehicle_brand_1CI.value = '(.+?)';"), html)[0]
        licenseKindCodeBC = re.findall(re.compile("parent.fraInterface.fm.licenseKindCodeBC.value = '(.+?)';"), html)[
            0]  #
        exhaustScaleBC = re.findall(re.compile("parent.fraInterface.fm.exhaustScaleBC.value = '(.+?)';"), html)[0]  # 排量
        carTypeCodeBC = re.findall(re.compile("parent.fraInterface.fm.carTypeCodeBC.value = '(.+?)';"), html)[0]  # 车辆类型
        frameNoBC = re.findall(re.compile("parent.fraInterface.fm.frameNoBC.value = '(.+?)';"), html)[0]  # 车架号
        licenseNoBC = re.findall(re.compile("parent.fraInterface.fm.licenseNoBC.value = '(.+?)';"), html)[0]  # 车牌号
        completeKerbMassNewBC = \
            re.findall(re.compile("parent.fraInterface.fm.completeKerbMassNewBC.value = '(.+?)';"), html)[0]  # 车牌号
        carOwnerNature1BC = "1"
        carOwnerIdentifyTypeCI = "01"  # 证件类型 01 身份证  10 组织机构代码
        appliNatureBC = "3"  # 自然人 4是 法人或者组织
        insuredNatureBC = "3"
        if len(carOwnerBC) >= 5:
            # 名字长度大于5个字说明是企业用车
            carOwnerNature1BC = "2"
            carOwnerIdentifyTypeCI = "10"
            appliNatureBC = "4"
            insuredNatureBC = "4"
        permium_dict['insuredNatureBC'] = insuredNatureBC
        permium_dict['appliNatureBC'] = appliNatureBC
        permium_dict['carOwnerIdentifyTypeCI'] = carOwnerIdentifyTypeCI
        permium_dict['carOwnerNature1BC'] = carOwnerNature1BC
        permium_dict['completeKerbMassNewBC'] = completeKerbMassNewBC
        permium_dict['madeFactoryBI'] = madeFactoryBI
        permium_dict['frameNoBC'] = frameNoBC
        permium_dict['licenseNoBC'] = licenseNoBC
        permium_dict['vehicle_modelCI'] = vehicle_modelCI
        permium_dict['vehicleBrandTemp'] = vehicleBrandTemp
        permium_dict['vehicle_brand_2CI'] = vehicle_brand_2CI
        permium_dict['exhaustScaleBC'] = exhaustScaleBC
        permium_dict['carTypeCodeBC'] = carTypeCodeBC
        permium_dict['countryNatureBC'] = countryNatureBC
        permium_dict['EngineNo'] = EngineNo
        permium_dict['licenseCategoryBC'] = licenseCategoryBC
        permium_dict['carOwnerBC'] = carOwnerBC
        permium_dict['enrollDateBC'] = enrollDateBC
        permium_dict['tonCountBC'] = tonCountBC
        permium_dict['pmUseNatureCodeBC'] = pmUseNatureCodeBC
        permium_dict['seatCountBC'] = seatCountBC
        permium_dict['licenseKindCodeBC'] = licenseKindCodeBC
        log.info(json.dumps(permium_dict, ensure_ascii=False))
        return permium_dict
    except Exception as e:
        import traceback
        log.error(traceback.format_exc())
        log.error(e)
        return "xd  parse vehicle info"


def parse_first_html(html):
    permium_dict = {}
    query_sequence_noBI = re.findall(re.compile("mainfm.query_sequence_noBI.value = '(.+?)';"), html)[
        0]  # query_sequence_noBI
    query_codeBI = re.findall(re.compile("mainfm.query_codeBI.value = '(.+?)';"), html)[0]  # query_codeBI
    modelCodeBC = re.findall(re.compile("mainfm.modelCodeBC.value = '(.+?)';"), html)[0]  # modelCodeBC
    pureRiskPremium = re.findall(re.compile("mainfm.pureRiskPremium.value = '(.+?)';"), html)[0]  # pureRiskPremium

    ClaimAdjustValueBI = re.findall(re.compile("mainfm.ClaimAdjustValueBI.value = '(.+?)';"), html)[
        0]  # ClaimAdjustValueBI
    ClaimAdjustReasonBI = re.findall(re.compile("mainfm.ClaimAdjustReasonBI.value = '(.+?)';"), html)[
        0]  # ClaimAdjustReasonBI
    PeccancyAdjustValueBI = re.findall(re.compile("mainfm.PeccancyAdjustValueBI.value = '(.+?)';"), html)[
        0]  # PeccancyAdjustValueBI
    PeccancyAdjustReasonBI = re.findall(re.compile("mainfm.PeccancyAdjustReasonBI.value = '(.+?)';"), html)[
        0]  # PeccancyAdjustReasonBI 累计违法系数不超过5%或仅存在不上浮的违法行为，不浮动
    claimInfoSize = re.findall(re.compile("mainfm.claimInfoSize.value = '(.+?)';"), html)[0]  # PeccancyAdjustValueBI

    lossConditionBI = re.findall(re.compile("mainfm.lossConditionBI.value = '(.+?)';"), html)[
        0]  # lossConditionBI 2年未出险
    comLossConditionBI = re.findall(re.compile("mainfm.comLossConditionBI.value = '(.+?)';"), html)[
        0]  # comLossConditionBI2年未出险
    lossConditionCodeBI = re.findall(re.compile("mainfm.lossConditionCodeBI.value = '(.+?)';"), html)[
        0]  # lossConditionCodeBI 02
    comLossConditionCI = re.findall(re.compile("mainfm.comLossConditionCI.value = '(.+?)';"), html)[
        0]  # comLossConditionCI2年未出险

    count = len(re.findall(re.compile("parent.fraInterface.insertRow"), html))
    if count == 0:
        permium_dict['illegal_list'] = ''
    else:
        illegal_list = []
        illegal_kind = (
            'BIDemandFeccTypeName', 'BIDemandPeccancy_type', 'BIDemandPeccancy_name', 'BIDemandPeccancy_time',
            'BIDemandPeccancy_place', 'BIDemandPeccancy_code', 'DecisionCode')
        for i in range(1, count + 1):
            illegal_info = {}
            for key in illegal_kind:
                illegal_info[key] = \
                    re.findall("mainfm." + key + "\[" + str(i) + "\]" + ".value\s*=\s*'(\s*|.+?)'", html, re.S)[0]
            illegal_list.append(illegal_info)
        permium_dict['illegal_list'] = _get_illegal_list_str(illegal_list)
    # print(json.dumps(permium_dict,ensure_ascii=False))
    # print(_get_illegal_list_str(illegal_list))
    permium_dict['query_sequence_noBI'] = query_sequence_noBI
    permium_dict['query_codeBI'] = query_codeBI
    permium_dict['modelCodeBC'] = modelCodeBC
    permium_dict['pureRiskPremium'] = pureRiskPremium
    permium_dict['ClaimAdjustValueBI'] = ClaimAdjustValueBI
    permium_dict['ClaimAdjustReasonBI'] = ClaimAdjustReasonBI
    permium_dict['PeccancyAdjustValueBI'] = PeccancyAdjustValueBI
    permium_dict['PeccancyAdjustReasonBI'] = PeccancyAdjustReasonBI
    permium_dict['lossConditionBI'] = lossConditionBI
    permium_dict['claimInfoSize'] = claimInfoSize
    permium_dict['comLossConditionBI'] = comLossConditionBI
    permium_dict['comLossConditionCI'] = comLossConditionCI
    permium_dict['lossConditionCodeBI'] = lossConditionCodeBI

    return permium_dict


def _get_illegal_list_str(illegal_list):
    illegal_str = ""
    for dic in illegal_list:
        illegal_str = illegal_str + "&BIDemandFecc_Flag="
        illegal_str = illegal_str + "&BIDemandFeccTypeName=" + dic['BIDemandFeccTypeName']
        illegal_str = illegal_str + "&BIDemandPeccancy_type=" + dic['BIDemandPeccancy_type']
        illegal_str = illegal_str + "&BIDemandPeccancy_name=" + dic['BIDemandPeccancy_name']
        illegal_str = illegal_str + "&BIDemandPeccancy_time=" + dic['BIDemandPeccancy_time']
        illegal_str = illegal_str + "&BIDemandPeccancy_place=" + dic['BIDemandPeccancy_place']
        illegal_str = illegal_str + "&BIDemandPeccancy_code=" + dic['BIDemandPeccancy_code']
        illegal_str = illegal_str + "&DecisionCode=" + dic['DecisionCode']
    return illegal_str


# 第二个请求返回的参数
def parse_xd_RulesBI(html):
    permium_dict = {}
    channelLowerRateBI = re.findall(re.compile("fm.channelLowerRateBI.value = \"(.+?)\";"), html)[
        0]  # channelLowerRateBI
    channelTopRateBI = re.findall(re.compile("fm.channelTopRateBI.value = \"(.+?)\";"), html)[0]  # channelTopRateBI
    adjustTopRateBI = re.findall(re.compile("fm.adjustTopRateBI.value = \"(.+?)\";"), html)[0]  # adjustTopRateBI
    adjustLowerRateBI = re.findall(re.compile("fm.adjustLowerRateBI.value = \"(.+?)\";"), html)[0]  # adjustLowerRateBI
    rateFactorsTotalMaxBI = re.findall(re.compile("fm.rateFactorsTotalMaxBI.value = \"(.+?)\";"), html)[
        0]  # rateFactorsTotalMaxBI
    rateFactorsTotalMinBI = re.findall(re.compile("fm.rateFactorsTotalMinBI.value = \"(.+?)\";"), html)[
        0]  # rateFactorsTotalMinBI
    rateFactorsTotalOriginBI = re.findall(re.compile("fm.rateFactorsTotalOriginBI.value = \"(.+?)\";"), html)[
        0]  # rateFactorsTotalOriginBI
    rateFactorsTotalBI = re.findall(re.compile("fm.rateFactorsTotalBI.value = \"(.+?)\";"), html)[
        0]  # rateFactorsTotalBI
    deductiblesCoefficient = re.findall(re.compile("fm.deductiblesCoefficient.value = \"(.+?)\";"), html)[
        0]  # deductiblesCoefficient
    sumChannelRateBI = re.findall(re.compile("fm.sumChannelRateBI.value = \"(.+?)\";"), html)[0]  # sumChannelRateBI
    sumAdjustRateBI = re.findall(re.compile("fm.sumAdjustRateBI.value = \"(.+?)\";"), html)[0]  # sumAdjustRateBI

    additionalCostRateBI = re.findall(re.compile("fm.additionalCostRateBI\[i\].value = \"(.+?)\";"), html)[
        0]  # additionalCostRateBI
    channelRateBI = re.findall(re.compile("fm.channelRateBI\[i\].value = \"(.+?)\";"), html)[0]  # channelRateBI
    adjustRateBI = re.findall(re.compile("fm.adjustRateBI\[i\].value = \"(.+?)\";"), html)[0]  # channelRateBI
    RateFactorsImfTemp = re.findall(re.compile("fm.RateFactorsImfTemp.value = \"(.+?)\";"), html)[
        0]  # RateFactorsImfTemp

    permium_dict['channelLowerRateBI'] = channelLowerRateBI
    permium_dict['channelTopRateBI'] = channelTopRateBI
    permium_dict['adjustTopRateBI'] = adjustTopRateBI
    permium_dict['adjustLowerRateBI'] = adjustLowerRateBI
    permium_dict['rateFactorsTotalMaxBI'] = rateFactorsTotalMaxBI
    permium_dict['rateFactorsTotalMinBI'] = rateFactorsTotalMinBI
    permium_dict['rateFactorsTotalOriginBI'] = rateFactorsTotalOriginBI
    permium_dict['rateFactorsTotalBI'] = rateFactorsTotalBI
    permium_dict['deductiblesCoefficient'] = deductiblesCoefficient

    permium_dict['sumChannelRateBI'] = sumChannelRateBI
    permium_dict['sumAdjustRateBI'] = sumAdjustRateBI
    permium_dict['additionalCostRateBI'] = additionalCostRateBI
    permium_dict['channelRateBI'] = channelRateBI
    permium_dict['adjustRateBI'] = adjustRateBI
    permium_dict['RateFactorsImfTemp'] = RateFactorsImfTemp

    return permium_dict


def parse_split_str(RateFactorsImfTemp):
    vartmp = RateFactorsImfTemp.split("|_|")
    varstr = ""
    print(len(vartmp))
    for i in xrange(0, len(vartmp)):
        arrTemp = vartmp[i].split("@_@")
        # print(json.dumps(arrTemp,ensure_ascii=False))
        if i == 0:
            varstr = "&RateProjectNameBI=" + arrTemp[0]
            varstr = varstr + "&RateFactorsMaxBI=" + arrTemp[1]
            varstr = varstr + "&RateFactorsMinBI=" + arrTemp[2]
            varstr = varstr + "&RateContentDescBI=" + arrTemp[3]
            varstr = varstr + "&RateProjectCodeBI=" + arrTemp[4]
        if i > 0:
            varstr = varstr + "&UndwrtFactor_KindCodeBI=B"
            varstr = varstr + "&UndwrtFactor_SerialnoBI=" + str(i)
            varstr = varstr + "&RateProjectNameBI=" + arrTemp[0]
            varstr = varstr + "&RateFactorsMaxBI=" + arrTemp[1]
            varstr = varstr + "&RateFactorsMinBI=" + arrTemp[2]
            varstr = varstr + "&RateContentDescBI=" + arrTemp[3]
            varstr = varstr + "&RateProjectCodeBI=" + arrTemp[4]

    varstr = varstr + "&UndwrtFactor_KindCodeBI=B&UndwrtFactor_SerialnoBI=" + str(len(vartmp))
    return varstr


def format_number(str_num):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format("%.2f", float(str_num), 1)


def xd_parse_premuim(html, premuim_dict):
    # 根据险种的选择进行判断 html中第一个是三者 三者不计免赔 车损 车损不计免赔
    # 如果选择了三者和不计免赔 车损是第数组第三个
    # 如果选择了三者没有不计免赔 车损是第二个
    # 如果全没全  那车损是第一个 基准保费需要除以0.65
    insuranceType = premuim_dict['insuranceType']
    benchMarkPremiumBI = re.findall(re.compile("var vStandardPremuim = \'(.+?)\';"), html)
    if insuranceType['otherHurtPremium']['isCheck'] == "1" and insuranceType['otherHurtBenchMarkPremium'] == "1":
        carDamagePremium = benchMarkPremiumBI[2]
    elif insuranceType['otherHurtPremium']['isCheck'] == "1" and insuranceType['otherHurtBenchMarkPremium'] == "0":
        carDamagePremium = benchMarkPremiumBI[1]
    elif insuranceType['otherHurtPremium']['isCheck'] == "0" and insuranceType['otherHurtBenchMarkPremium'] == "0":
        carDamagePremium = benchMarkPremiumBI[0]

    # 解析返回报文中的出险情况
    profitDetailEncodeBI_list = re.findall(re.compile("mainfm.profitDetailEncodeBI\[0\].value = \'(.+?)\';"), html)

    return {"carDamagePremium": float(carDamagePremium), "profitDetailEncodeBI_list": profitDetailEncodeBI_list}


def xd_parse_get_premuim(premuim_dict):
    insuranceType = premuim_dict['insuranceType']
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

    actualValue = premuim_dict['actualValue']['actualValueBC'].replace(",", "")  # 协商价格
    riskPremium = premuim_dict['actualValue']['riskPremium']
    compromisePrice = premuim_dict['carVinInfo']['compromisePrice']  # 实际价格
    frameNoBC = premuim_dict['vehicle']['frameNoBC']
    seatCountBC = premuim_dict['vehicle']['seatCountBC']
    useNatureCode = premuim_dict['vehicle']['pmUseNatureCodeBC']  # 使用性质 车管所返回 以后要修改为人工传入
    carTypeCodeBC = premuim_dict['vehicle']['carTypeCodeBC']
    useyear = premuim_dict['actualValue']['useYears']
    # 商车费改优惠系数调整
    ClaimAdjustValueBI = premuim_dict['SubmitBI']['ClaimAdjustValueBI']
    PeccancyAdjustValueBI = premuim_dict['SubmitBI']['PeccancyAdjustValueBI']
    # 渠道系数
    channelRateBI = premuim_dict['Rules']['sumChannelRateBI']
    adjustRateBI = premuim_dict['Rules']['sumAdjustRateBI']
    rate = (float(ClaimAdjustValueBI) + 1) * (float(PeccancyAdjustValueBI) + 1) * (float(channelRateBI)) * (
        float(adjustRateBI))
    if carTypeCodeBC == "02":
        if float(seatCountBC) < 6:
            carTypeCodeBC = "1"
        elif float(seatCountBC) >= 6 and float(seatCountBC) < 10:
            carTypeCodeBC = "2"
        elif float(seatCountBC) >= 10 and float(seatCountBC) < 20:
            carTypeCodeBC = "4"
            # if carTypeCodeBC == "01":
            # 货车 根据吨数来传
            #   pass

    otherHurtPremiumBe = insuranceType['otherHurtPremium']['Amount']
    driverDutyPremiumBe = insuranceType['driverDutyPremium']['Amount']
    passengerDutyPremiumBe = insuranceType['passengerDutyPremium']['Amount']

    otherHurtPremiumBe = otherHurtPremiumBe.replace(",", "") if otherHurtPremiumBe != "0" else "500000"
    driverDutyPremiumBe = driverDutyPremiumBe.replace(",", "") if driverDutyPremiumBe != "0" else "10000"
    passengerDutyPremiumBe = passengerDutyPremiumBe.replace(",", "") if passengerDutyPremiumBe != "0" else "10000"
    seatCountBC = seatCountBC if seatCountBC != "0" else "5"
    passengerDutyPremiumBe = (float(seatCountBC) - 1) * float(passengerDutyPremiumBe)

    # 通过车架号判断是否为国产
    if frameNoBC[0] == "L":
        produced = "A"
    else:
        produced = "B"

    myCarTypeCodeBC = premuim_dict['vehicle']['myCarTypeCodeBC']
    useNatureCodeBC = premuim_dict.get("carVinInfo", {}).get("useNatureCodeBC", "8A")
    NatureCodeBC = "A"
    if useNatureCodeBC == "8A":
        NatureCodeBC = "A"
    elif useNatureCodeBC == "9D":
        NatureCodeBC = "H"

    Premium_tmp = get_car_main_premium(NatureCodeBC, myCarTypeCodeBC, otherHurtPremiumBe, driverDutyPremiumBe,
                                       passengerDutyPremiumBe,
                                       produced, compromisePrice, actualValue, rate)

    if carDamagePremium == "1":
        carDamagePremium_baofei = float(float(riskPremium) / 0.65) * rate

    repair_rate = 0.15

    if repairFactoryPremium == "1":
        repair_rate = insuranceType.get("repairFactoryPremium", {}).get("rate", "15")
        repair_rate = float(repair_rate) / 100

    if carNickPremium == "1":
        carNickPremiumBe = insuranceType.get("carNickPremium", {}).get("Amount", "2000")

    Premium = {
        "compulsory_insurance": False,  # 交强险
        "NAggTax": False,  # 车船税
        "carDamagePremium": carDamagePremium_baofei,  # 车损险
        "carTheftPremium": Premium_tmp['carTheftPremium'] if carTheftPremium != "0" else False,  # 盗抢险
        "otherHurtPremium": Premium_tmp['otherHurtPremium'] if otherHurtPremium != "0" else False,  # 三者险
        "driverDutyPremium": Premium_tmp['driverDutyPremium'] if driverDutyPremium != "0" else False,  # 车上人员险（司机）
        "passengerDutyPremium": Premium_tmp['passengerDutyPremium'] if passengerDutyPremium != "0" else False,
        # 车上人员险(乘客)
        "carNickPremium": get_car_nick_premium(useyear, compromisePrice, carNickPremiumBe,
                                               rate) if carNickPremium != "0" else False,  # 划痕险
        "glassBrokenPremium": Premium_tmp['glassBrokenPremium'] if glassBrokenPremium != "0" else False,  # 玻璃破碎险
        "carFirePremium": get_car_fire_premium(useNatureCode, useyear, actualValue,
                                               rate) if carFirePremium != "0" else False,  # 自燃损失险
        "engineWadingPremium": float(carDamagePremium_baofei) * 0.05 if engineWadingPremium != "0" else False,
        "repairFactoryPremium": float(carDamagePremium_baofei) * repair_rate if engineWadingPremium != "0" else False
        # ,"seatCount": seatCountBC
    }

    BaoE = {
        "carTheftBaoE": actualValue if carTheftPremium != "0" else False,
        "carDamageBaoE": actualValue if carDamagePremium != "0" else False,
        "otherHurtBaoE": otherHurtPremiumBe if otherHurtPremium != "0" else False,
        "driverDutyBaoE": driverDutyPremiumBe if driverDutyPremium != "0" else False,
        "passengerDutyBaoe": passengerDutyPremiumBe if passengerDutyPremium != "0" else False,
        "carNickBaoE": carNickPremiumBe if carNickPremium != "0" else False,
    }

    carDamageBenchMarkPremium = insuranceType.get("carDamageBenchMarkPremium", "0")
    carTheftBenchMarkPremium = insuranceType.get("carTheftBenchMarkPremium", "0")
    otherHurtBenchMarkPremium = insuranceType.get("otherHurtBenchMarkPremium", "0")
    driverDutyBenchMarkPremium = insuranceType.get("driverDutyBenchMarkPremium", "0")
    passengerBenchMarkPremium = insuranceType.get("passengerBenchMarkPremium", "0")
    carNickBenchMarkPremium = insuranceType.get("carNickBenchMarkPremium", "0")
    carFireBrokenBenchMarkPremium = insuranceType.get("carFireBrokenBenchMarkPremium", "0")
    engineWadingBenchMarkPremium = insuranceType.get("engineWadingBenchMarkPremium", "0")

    MarkPremium = {
        "carDamageBenchMarkPremium": float(Premium['carDamagePremium']) * BenchMarkPremium[
            'carDamagePremium'] if carDamageBenchMarkPremium != "0" else False,  # 车损险不计免赔
        "carTheftBenchMarkPremium": float(Premium['carTheftPremium']) * BenchMarkPremium[
            'carTheftPremium'] if carTheftBenchMarkPremium != "0" else False,  # 盗抢险不计免赔
        "otherHurtBenchMarkPremium": float(Premium['otherHurtPremium']) * BenchMarkPremium[
            'otherHurtPremium'] if otherHurtBenchMarkPremium != "0" else False,  # 三者责任险的不计免赔
        "driverDutyBenchMarkPremium": float(Premium['driverDutyPremium']) * BenchMarkPremium[
            'driverDutyPremium'] if driverDutyBenchMarkPremium != "0" else False,  # 车上人员责任险（司机）不计免赔含税保费
        "passengerBenchMarkPremium": float(Premium['passengerDutyPremium']) * BenchMarkPremium[
            'passengerDutyPremium'] if passengerBenchMarkPremium != "0" else False,  # 车上人员责任险（乘客）不计免赔含税保费
        "carNickBenchMarkPremium": float(Premium['carNickPremium']) * BenchMarkPremium[
            'carNickPremium'] if carNickBenchMarkPremium != "0" else False,  # 划痕险不计免赔含税保费
        "carFireBrokenBenchMarkPremium": float(Premium['carFirePremium']) * BenchMarkPremium[
            'carFirePremium'] if carFireBrokenBenchMarkPremium != "0" else False,  # 自燃损失险不计免赔含税保费
        "engineWadingBenchMarkPremium": float(Premium['engineWadingPremium']) * BenchMarkPremium[
            'engineWadingPremium'] if engineWadingBenchMarkPremium != "0" else False  # 发动机涉水险不计免赔含税保费
    }
    disCount = {
        "sy_disCount": rate,
        "jq_disCount": False
    }
    Premium2 = {}
    BaoE2 = {}
    MarkPremium2 = {}
    disCount2 = {}
    sum_premium = 0
    for i in Premium:
        if Premium[i] != False:
            Premium2[i] = round(float(Premium[i]) + 0.004, 2)
            sum_premium = sum_premium + Premium2[i]
    Premium2['sum_premium'] = sum_premium
    for i in BaoE:
        if BaoE[i] != False:
            BaoE2[i] = BaoE[i]

    for i in MarkPremium:
        if MarkPremium[i] != False:
            MarkPremium2[i] = round(float(MarkPremium[i]) + 0.004, 2)
    for i in disCount:
        if disCount[i] != False:
            disCount2[i] = disCount[i]
    PremiumInfo = [Premium2, BaoE2, MarkPremium2, disCount2]
    return PremiumInfo


def xd_parse_jq_premuim(html):
    premiumCI = re.findall(re.compile("mainfm.premiumCI\s*.value\s*= \'(.+?)\';"), html)[0]
    discountCI = re.findall(re.compile("mainfm.discountCI\s*.value\s*= \'(.+?)\';"), html)[0]
    NAggTax = re.findall(re.compile("mainfm.sumTaxCICS\s*.value\s*= \'(.+?)\';"), html)[0]
    query_sequence_noCI = re.findall(re.compile("mainfm.query_sequence_noCI\s*.value\s*= \'(.+?)\';"), html)[0]
    query_codeCI = re.findall(re.compile("mainfm.query_codeCI\s*.value\s*= \'(.+?)\';"), html)[0]
    reInsureFlagCI = re.findall(re.compile("mainfm.reInsureFlagCI\s*.value\s*= \'(.+?)\';"), html)[0]
    lastBillDateCI = re.findall(re.compile("mainfm.lastBillDateCI\s*.value\s*= \'(.+?)\';"), html)[0]
    return {'jq_disCount': discountCI, 'compulsory_insurance': premiumCI, "NAggTax": NAggTax,
            "query_codeCI": query_codeCI, "reInsureFlagCI": reInsureFlagCI, "lastBillDateCI": lastBillDateCI,
            "query_sequence_noCI": query_sequence_noCI}


def xd_parse_tmp_no(html):
    # 存储临时单号
    if "暂存成功" in html:
        tempProposalNoCI = \
            re.findall(re.compile('input type="hidden" name="tempProposalNoCI" value=\"(.+?)\">'), html)[
                0]
        tempProposalNoBI = \
            re.findall(re.compile('input type="hidden" name="tempProposalNoBI" value=\"(.+?)\">'), html)[
                0]
        return {"tempProposalNoCI": tempProposalNoCI, "tempProposalNoBI": tempProposalNoBI}
    return "暂存单失败重试"


def xd_parse_no(html):
    # 解析投保单号
    innerHTML = ""
    if "投保单保存成功" in html:
        ProposalNoCI = \
            re.findall(re.compile('parent.fraInterface.fm.ProposalNoCI.value = \"(.+?)\";'), html)[0]
        ProposalNoBI = \
            re.findall(re.compile('parent.fraInterface.fm.ProposalNoBI.value = \"(.+?)\";'), html)[0]
        innerHTML = re.findall(re.compile('parent.fraInterface.saveNewImageMsg.innerHTML = \"(.+?)\"'), html)[0]
        log.info(innerHTML)
        return {"ProposalNoCI": ProposalNoCI, "ProposalNoBI": ProposalNoBI}
    if "alert" in html:
        return html
    return "投保失败"


def xd_parse_riskLevelFlag(html):
    info_dict = {}
    riskLevelFlag = re.findall(re.compile("theform.riskLevelFlag.value=\"(.+?)\";"), html)[0]
    businessClassBC = re.findall(re.compile("theform.businessClassBC.value=\"(.+?)\";"), html)[0]
    inQuiryNoBC = re.findall(re.compile("theform.inQuiryNoBC.value=\"(.+?)\";"), html)[0]
    businessClassNameBC = re.findall(re.compile("theform.businessClassNameBC.value=\"(.+?)\";"), html)[0]
    BusinessRemark1 = re.findall(re.compile("theform.BusinessRemark1.value=\"(.+?)\";"), html)[0]
    businessClassNameBC = re.findall(re.compile("theform.businessClassNameBC.value=\"(.+?)\";"), html)[0]
    sellingExpensesRateCI = re.findall(re.compile("theform.sellingExpensesRateCI.value=\"(.+?)\";"), html)[0]
    disRateCI = re.findall(re.compile("theform.disRateCI.value=\"(.+?)\";"), html)[0]
    maxDisRateCI = re.findall(re.compile("theform.maxDisRateCI.value=\"(.+?)\";"), html)[0]
    maxAllowanceRateCI = re.findall(re.compile("theform.maxAllowanceRateCI.value=\"(.+?)\";"), html)[0]
    businessCategoryCI = re.findall(re.compile("theform.businessCategoryCI.value=\"(.+?)\";"), html)[0]
    chargeNumberCI = re.findall(re.compile("theform.chargeNumberCI.value=\"(.+?)\";"), html)[0]
    businessPromoteRateCI = re.findall(re.compile("theform.businessPromoteRateCI.value=\"(.+?)\";"), html)[0]
    maxBusinessPromoteRateCI = re.findall(re.compile("theform.maxBusinessPromoteRateCI.value=\"(.+?)\";"), html)[0]
    sellRateCI = re.findall(re.compile("theform.sellRateCI.value=\"(.+?)\";"), html)[0]
    coefficient1CI = re.findall(re.compile("theform.coefficient1CI.value=\"(.+?)\";"), html)[0]
    coefficient2CI = re.findall(re.compile("theform.coefficient2CI.value=\"(.+?)\";"), html)[0]
    # maxSalesSalaryRateCI = re.findall(re.compile("theform.maxSalesSalaryRateCI.value=\"(.+?)\";"), html)[0]
    # salesSalaryRateCI = re.findall(re.compile("theform.salesSalaryRateCI.value=\"(.+?)\";"), html)[0]
    coefficient3CI = re.findall(re.compile("theform.coefficient3CI.value=\"(.+?)\";"), html)[0]
    coefficient4CI = re.findall(re.compile("theform.coefficient4CI.value=\"(.+?)\";"), html)[0]
    coefficient5CI = re.findall(re.compile("theform.coefficient5CI.value=\"(.+?)\";"), html)[0]
    coefficient6CI = re.findall(re.compile("theform.coefficient6CI.value=\"(.+?)\";"), html)[0]
    coefficient7CI = re.findall(re.compile("theform.coefficient7CI.value=\"(.+?)\";"), html)[0]
    coefficient8CI = re.findall(re.compile("theform.coefficient8CI.value=\"(.+?)\";"), html)[0]
    coefficient9CI = re.findall(re.compile("theform.coefficient9CI.value=\"(.+?)\";"), html)[0]
    coefficient10CI = re.findall(re.compile("theform.coefficient10CI.value=\"(.+?)\";"), html)[0]
    coefficient11CI = re.findall(re.compile("theform.coefficient11CI.value=\"(.+?)\";"), html)[0]
    disrateYCI = re.findall(re.compile("theform.disrateYCI.value\s*=\s*\"(.+?)\";"), html)[0]
    allowancerateYCI = re.findall(re.compile("theform.allowancerateYCI.value\s*=\s*\"(.+?)\";"), html)[0]
    teammaintenancerateYCI = re.findall(re.compile("theform.teammaintenancerateYCI.value\s*=\s*\"(.+?)\";"), html)[0]
    businesspromoterateYCI = re.findall(re.compile("theform.businesspromoterateYCI.value\s*=\s*\"(.+?)\";"), html)[0]
    displayrateYCI = re.findall(re.compile("theform.displayrateYCI.value\s*=\s*\"(.+?)\";"), html)[0]
    othermarketrateYCI = re.findall(re.compile("theform.othermarketrateYCI.value\s*=\s*\"(.+?)\";"), html)[0]
    sumbudgetYCI = re.findall(re.compile("theform.sumbudgetYCI.value\s*=\s*\"(.+?)\";"), html)[0]
    sumFeeCI = re.findall(re.compile("theform.sumFeeCI.value\s*=\s*\"(.+?)\";"), html)[0]
    sumNoTaxFeeCI = re.findall(re.compile("theform.sumNoTaxFeeCI.value\s*=\s*\"(.+?)\";"), html)[0]
    VATtaxRateCI = re.findall(re.compile("theform.VATtaxRateCI.value\s*=\s*\"(.+?)\";"), html)[0]
    VATdutyRatioCI = re.findall(re.compile("theform.VATdutyRatioCI.value\s*=\s*\"(.+?)\";"), html)[0]
    VATtransferTaxCI = re.findall(re.compile("theform.VATtransferTaxCI.value\s*=\s*\"(.+?)\";"), html)[0]
    sumFeeBI = re.findall(re.compile("theform.sumFeeBI.value\s*=\s*\"(.+?)\";"), html)[0]
    sumNoTaxFeeBI = re.findall(re.compile("theform.sumNoTaxFeeBI.value\s*=\s*\"(.+?)\";"), html)[0]
    VATtaxRateBI = re.findall(re.compile("theform.VATtaxRateBI.value\s*=\s*\"(.+?)\";"), html)[0]
    VATdutyRatioBI = re.findall(re.compile("theform.VATdutyRatioBI.value\s*=\s*\"(.+?)\";"), html)[0]
    VATtransferTaxBI = re.findall(re.compile("theform.VATtransferTaxBI.value\s*=\s*\"(.+?)\";"), html)[0]
    sellingExpensesRateBI = re.findall(re.compile("theform.sellingExpensesRateBI.value=\"(.+?)\";"), html)[0]
    disRateBI = re.findall(re.compile("theform.disRateBI.value=\"(.+?)\";"), html)[0]
    maxDisRateBI = re.findall(re.compile("theform.maxDisRateBI.value=\"(.+?)\";"), html)[0]
    maxAllowanceRateBI = re.findall(re.compile("theform.maxAllowanceRateBI.value=\"(.+?)\";"), html)[0]
    allowanceRateBI = re.findall(re.compile("theform.allowanceRateBI.value=\"(.+?)\";"), html)[0]
    businessCategoryBI = re.findall(re.compile("theform.businessCategoryBI.value=\"(.+?)\";"), html)[0]
    chargeNumberBI = re.findall(re.compile("theform.chargeNumberBI.value=\"(.+?)\";"), html)[0]
    businessPromoteRateBI = re.findall(re.compile("theform.businessPromoteRateBI.value=\"(.+?)\";"), html)[0]
    maxBusinessPromoteRateBI = re.findall(re.compile("theform.maxBusinessPromoteRateBI.value=\"(.+?)\";"), html)[0]
    sellRateBI = re.findall(re.compile("theform.sellRateBI.value=\"(.+?)\";"), html)[0]
    coefficient1BI = re.findall(re.compile("theform.coefficient1BI.value=\"(.+?)\";"), html)[0]
    coefficient2BI = re.findall(re.compile("theform.coefficient2BI.value=\"(.+?)\";"), html)[0]
    coefficient3BI = re.findall(re.compile("theform.coefficient3BI.value=\"(.+?)\";"), html)[0]
    coefficient4BI = re.findall(re.compile("theform.coefficient4BI.value=\"(.+?)\";"), html)[0]
    coefficient5BI = re.findall(re.compile("theform.coefficient5BI.value=\"(.+?)\";"), html)[0]
    coefficient6BI = re.findall(re.compile("theform.coefficient6BI.value=\"(.+?)\";"), html)[0]
    coefficient7BI = re.findall(re.compile("theform.coefficient7BI.value=\"(.+?)\";"), html)[0]
    coefficient8BI = re.findall(re.compile("theform.coefficient8BI.value=\"(.+?)\";"), html)[0]
    coefficient9BI = re.findall(re.compile("theform.coefficient9BI.value=\"(.+?)\";"), html)[0]
    coefficient10BI = re.findall(re.compile("theform.coefficient10BI.value=\"(.+?)\";"), html)[0]
    coefficient11BI = re.findall(re.compile("theform.coefficient11BI.value=\"(.+?)\";"), html)[0]
    disrateYBI = re.findall(re.compile("theform.disrateYBI.value\s*=\s*\"(.+?)\";"), html)[0]
    allowancerateYBI = re.findall(re.compile("theform.allowancerateYBI.value\s*=\s*\"(.+?)\";"), html)[0]
    teammaintenancerateYBI = re.findall(re.compile("theform.teammaintenancerateYBI.value\s*=\s*\"(.+?)\";"), html)[0]
    businesspromoterateYBI = re.findall(re.compile("theform.businesspromoterateYBI.value\s*=\s*\"(.+?)\";"), html)[0]
    displayrateYBI = re.findall(re.compile("theform.displayrateYBI.value\s*=\s*\"(.+?)\";"), html)[0]
    othermarketrateYBI = re.findall(re.compile("theform.othermarketrateYBI.value\s*=\s*\"(.+?)\";"), html)[0]
    sumbudgetYBI = re.findall(re.compile("theform.sumbudgetYBI.value\s*=\s*\"(.+?)\";"), html)[0]

    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['riskLevelFlag'] = riskLevelFlag
    info_dict['businessClassBC'] = businessClassBC;
    info_dict['businessClassNameBC'] = businessClassNameBC
    info_dict['sellingExpensesRateBI'] = sellingExpensesRateBI;
    info_dict['sellingExpensesRateCI'] = sellingExpensesRateCI
    info_dict['BusinessRemark1'] = BusinessRemark1;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['sellRateCI'] = sellRateCI;
    info_dict['chargeNumberCI'] = chargeNumberCI
    info_dict['chargeNumberCI'] = chargeNumberCI;
    info_dict['sumFeeCI'] = sumFeeCI
    info_dict['sumNoTaxFeeCI'] = sumNoTaxFeeCI;
    info_dict['VATtaxRateCI'] = VATtaxRateCI
    info_dict['VATdutyRatioCI'] = VATdutyRatioCI;
    info_dict['VATtransferTaxCI'] = VATtransferTaxCI
    info_dict['sellRateBI'] = sellRateBI;
    info_dict['chargeNumberBI'] = chargeNumberBI
    info_dict['businessCategoryBI'] = businessCategoryBI;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    # info_dict['premiumDisRateBI'] = premiumDisRateBI;
    info_dict['VATtaxRateBI'] = VATtaxRateBI
    info_dict['VATdutyRatioBI'] = VATdutyRatioBI;
    info_dict['VATtransferTaxBI'] = VATtransferTaxBI
    info_dict['sumbudgetYCI'] = sumbudgetYCI;
    info_dict['sumbudgetYBI'] = sumbudgetYBI
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['inQuiryNoBC'] = inQuiryNoBC;
    info_dict['inQuiryNoBC'] = inQuiryNoBC
    info_dict['businessCategoryCI'] = businessCategoryCI
    info_dict['disRateCI'] = disRateCI



    log.info("riskLevelFlag %s", riskLevelFlag)
    return info_dict


if __name__ == "__main__":
    # print parsedataObjs(demo)
    f = open("C:\Users\weikai\Desktop\\222.html", "r")
    html = f.read()
    # var = "在我司续保年限@_@1.0@_@0.95@_@新车、平台新保、转保及其他@_@A2-在我司续保年限|_|商业险险别组合@_@1.0@_@0.5@_@单保三者及附加险@_@A1-商业险险别组合|_|上年出险情况@_@1.0@_@0.9@_@连续2年没有发生赔款@_@A3-上年出险情况|_|性别@_@1.0@_@1.0@_@男@_@A5-性别|_|年龄@_@1.1@_@0.85@_@≥35@_@A4-年龄|_|车系@_@1.1@_@0.95@_@车系三@_@A6-车系"
    # print format_number()
    print(xd_parse_riskLevelFlag(html))
    # #xd_parse_premuim
    # xd_parse_jq_premuim(html)
    # xd_parse_actualValue(html)
    from string import Template
