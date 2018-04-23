# -*- coding:utf-8 -*-
__author__ = 'weikai'

import re
import jsonpath
from bs4 import BeautifulSoup
from request_cic.utils import getlatedate


# 获取车辆信息转换dict
def parseCarInfo(pagesource):
    # html.parser
    soup = BeautifulSoup(pagesource, "lxml")
    text = soup.select('#bodyhidden')[0].select('#zhcx')[0]
    tr = text.findAll('tr')
    list2 = []
    for i in range(1, len(tr)):
        onedict = {}
        vehicleId = tr[i].input.get('value').replace(u'\xa0', u'').replace(' ', '').replace(u'\t', '').replace(u'\n',
                                                                                                               '').replace(
            u'\r', '')
        vehicleName = tr[i].findAll('td')[1].getText().replace(u'\xa0', u'').replace(u'\t', '').replace(u'\n',
                                                                                                        '').replace(
            u'\r', '')  # .replace(' ', '')
        insuranceJqName = tr[i].findAll('td')[2].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t',
                                                                                                          '').replace(
            u'\n', '').replace(u'\r', '')
        vehicleCode = tr[i].findAll('td')[3].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t',
                                                                                                      '').replace(u'\n',
                                                                                                                  '').replace(
            u'\r', '')
        factoryName = tr[i].findAll('td')[4].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t',
                                                                                                      '').replace(u'\n',
                                                                                                                  '').replace(
            u'\r', '')
        seat = tr[i].findAll('td')[5].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t', '').replace(u'\n',
                                                                                                                  '').replace(
            u'\r', '')
        displacementtr = tr[i].findAll('td')[6].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t',
                                                                                                         '').replace(
            u'\n', '').replace(u'\r', '')
        purchasePriceTax = tr[i].findAll('td')[8].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t',
                                                                                                           '').replace(
            u'\n', '').replace(u'\r', '')
        kindredPrice = tr[i].findAll('td')[9].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t',
                                                                                                       '').replace(
            u'\n', '').replace(u'\r', '')
        marketDate = tr[i].findAll('td')[10].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t',
                                                                                                      '').replace(u'\n',
                                                                                                                  '').replace(
            u'\r', '')
        demo = tr[i].findAll('td')[11].getText().replace(u'\xa0', u'').replace(' ', '').replace(u'\t', '').replace(
            u'\n', '').replace(u'\r', '')
        # print vehicleId,vehicleCode,vehicleName,insuranceJqName,factoryName,seat,purchasePriceTax,kindredPrice,marketDate,demo
        onedict['vehicleId'] = vehicleId
        onedict['gCIndustryModelName'] = vehicleName  # 雅阁HG7240A(ACCORD2.4i-VTEC)轿车
        onedict['insuranceJqName'] = insuranceJqName
        onedict['vehicleCode'] = vehicleCode
        onedict['factoryName'] = factoryName
        onedict['seat'] = seat
        onedict['purchasePriceTax'] = int(purchasePriceTax.replace(" ", "").split(u"【")[0])  # 购置价【含税】purchasePriceTax
        onedict['kindredPrice'] = kindredPrice
        onedict['marketDate'] = marketDate
        onedict['demo'] = demo
        list2.append(onedict)
    # 按照价格排序

    # list2.sort(key=lambda obj:obj.get('purchasePriceTax'))
    list2 = sorted(list2, key=lambda x: x["purchasePriceTax"], reverse=True)
    return list2


# 参数车牌号 返回这个车牌号的信息dict
def parsedataObjs(pagesource):
    dt = {}
    # pagesource=pagesource.replace(' ','')
    dataObjs = re.findall(r"DATA:\[(.+?)\],", pagesource, re.S)[0]
    dataObjs = dataObjs.strip().lstrip().rstrip("'").strip("'")
    soup = BeautifulSoup(dataObjs, "xml")
    dataObj = soup.findAll('dataObj')
    i = dataObj[0]
    # for i in dataObj:
    CPlateNo = i.findAll(attrs={"name": "CPlateNo"})[0].getText()
    # if CPlateNo==unicode(cplateno,'utf-8'):
    CPlateTyp = i.findAll(attrs={"name": "CPlateTyp"})[0].get("value")
    pmUseType = i.findAll(attrs={"name": "pmUseType"})[0].getText()
    CFrmNo = i.findAll(attrs={"name": "CFrmNo"})[0].getText()
    CEngNo = i.findAll(attrs={"name": "CEngNo"})[0].getText()
    color = i.findAll(attrs={"name": "color"})[0].getText()
    COwnerNme = i.findAll(attrs={"name": "COwnerNme"})[0].getText()
    CFstRegYm = i.findAll(attrs={"name": "CFstRegYm"})[0].getText()
    RLimitLoadPerson = i.findAll(attrs={"name": "RLimitLoadPerson"})[0].getText()
    RVehlcleTonnage = i.findAll(attrs={"name": "RVehlcleTonnage"})[0].getText()
    IneffectualDate = i.findAll(attrs={"name": "IneffectualDate"})[0].getText()
    MadeFactory = i.findAll(attrs={"name": "MadeFactory"})[0].getText()
    Model = i.findAll(attrs={"name": "Model"})[0].getText()
    BrandCN = i.findAll(attrs={"name": "BrandCN"})[0].getText()
    BrandEN = i.findAll(attrs={"name": "BrandEN"})[0].getText()
    CVhlTyp = i.findAll(attrs={"name": "CVhlTyp"})[0].get("value")
    LastCheckDate = i.findAll(attrs={"name": "LastCheckDate"})[0].getText()
    RejectDate = i.findAll(attrs={"name": "RejectDate"})[0].getText()
    status = i.findAll(attrs={"name": "status"})[0].getText()
    Haulage = i.findAll(attrs={"name": "Haulage"})[0].getText()
    TransferDate = i.findAll(attrs={"name": "TransferDate"})[0].getText()
    NCurbWt = i.findAll(attrs={"name": "NCurbWt"})[0].getText()
    NDisplacement = i.findAll(attrs={"name": "NDisplacement"})[0].getText()
    SalesChannl = i.findAll(attrs={"name": "SalesChannl"})[0].getText()
    VehlclePrice = i.findAll(attrs={"name": "VehlclePrice"})[0].getText()
    EngineType = i.findAll(attrs={"name": "EngineType"})[0].getText()
    RImportFlag = i.findAll(attrs={"name": "RImportFlag"})[0].getText()
    useType = i.findAll(attrs={"name": "useType"})[0].getText()
    dt = {'gCPlateNo': CPlateNo,  # 车牌
          'licenseNo': CPlateNo,
          'gCPlateTyp': CPlateTyp,
          'pmUseType': pmUseType,
          'gCFrmNo': CFrmNo,  # 车架
          'CEngNo': CEngNo,  # 发动机
          'color': color,
          'hCAppNme': COwnerNme,
          'CFstRegYm': CFstRegYm,
          'gNSeatNum': RLimitLoadPerson,  # 座位数
          'RVehlcleTonnage': RVehlcleTonnage,
          'IneffectualDate': IneffectualDate,
          'MadeFactory': MadeFactory,
          'gCNoticeType': Model,  # 行业公告车型
          'gCBrandId': BrandCN,
          'BrandEN': BrandEN,
          'gCRegVhlTyp': CVhlTyp,  # K33  轿车 K31小型轿车
          'LastCheckDate': LastCheckDate,
          'RejectDate': RejectDate,
          'status': status,
          'Haulage': Haulage,
          'TransferDate': TransferDate,
          'NCurbWt': NCurbWt,
          'gNDisplacement': NDisplacement,  # 排量
          'SalesChannl': SalesChannl,
          'VehlclePrice': VehlclePrice,
          'EngineType': EngineType,  # A 汽油 B柴油 O混合动力
          'RImportFlag': RImportFlag,  # 六座以下客车 11  #六座至十座客车 12 十座至二十座以下客车 13
          'useType': useType
          }
    # print(dt)
    return dt


html = '''
<input type='hidden' name='hvinRoot' value='LMVHEKFD6EA029484' />
<input type='hidden' name='vehicleCode' value='HMD1061YQH' />
<input type='hidden' name='vehicleCode' value='HMD1061YQH' />
<input type='hidden' name='vehicleName' value='海马HMA7161GA4W轿车' />
<input type='hidden' name='brandName' value='海马' />
<input type='hidden' name='familyName' value='海马S5' />
<input type='hidden' name='vehicleFgwCode' value='HMA7161GA4W' />
<input type='hidden' name='seat' value='5' />
<input type='hidden' name='tonnage' value='' />
<input type='hidden' name='gearboxType' value='手动档' />
<input type='hidden' name='absFlag' value='有' />
<input type='hidden' name='antiTheft' value='有' />
<input type='hidden' name='airbagNum' value='2' />
<input type='hidden' name='remark' value='手动档 智乐型 国Ⅳ' />
<input type='hidden' name='displacement' value='1591' />
<input type='hidden' name='factoryName' value='一汽海马汽车有限公司' />
<input type='hidden' name='importF' value='国产' />
<input type='hidden' name='purchasePrice' value='92800' />
<input type='hidden' name='purchasePriceTax' value='96766' />
<input type='hidden' name='kindredPrice' value='0' />
<input type='hidden' name='kindredPriceTax' value='0' />
<input type='hidden' name='marketDate' value='201404' />
<input type='hidden' name='insuranceSyCode' value='01' />
<input type='hidden' name='insuranceSyName' value='六座以下客车' />
<input type='hidden' name='insuranceJqCode' value='KA' />
<input type='hidden' name='insuranceJqName' value='六座以下客车' />
<input type='hidden' name='searchCode' value='HM-HMA7161GA4W' />
<input type='hidden' name='factoryCode' value='MK0888' />
<input type='hidden' name='familyCode' value='HMB0AL' />
<input type='hidden' name='brandCode' value='HMB0' />
<input type='hidden' name='vehiclealise' value='海马S5 1.6L MT智乐型' />
<input type='hidden' name='vehicleClassName' value='越野车类' />
<input type='hidden' name='status' value='0' />
<input type='hidden' name='powertype' value='汽油' />
<input type='hidden' name='wheelbase' value='2630' />
<input type='hidden' name='groupname' value='海马S5(14/04-)' />
<input type='hidden' name='groupcode' value='HMB0AL01' />
<input type='hidden' name='createddate' value='2014-03-31 16:49:29.0' />
<input type='hidden' name='updateddate' value='2015-03-12 11:10:28.0' />
<input type='hidden' name='seatmin' value='' />
<input type='hidden' name='seatmax' value='' />
<input type='hidden' name='fullweightmax' value='1.35' />
<input type='hidden' name='fullweightmin' value='1.35' />
<input type='hidden' name='searchcode1' value='HM-S51.6LMT' />
<input type='hidden' name='hfcode' value='0' />
<input type='hidden' name='hfname' value='正常' />
<input type='hidden' name='hyVehicleCode' value='BHMESXUB0001' />
<input type='hidden' name='hyVehicleName' value='%25E6%25B5%25B7%25E9%25A9%25ACHMA7161GA4W%2B%25E6%2599%25BA%25E4%25B9%2590%25E5%259E%258B' />
'''


def parseCardata(html):
    soup = BeautifulSoup(html, "html.parser")
    dt = {}
    for i in soup.findAll("input"):
        dt[i.get("name")] = i.get("value")
    return dt


"""
PHCC_VHL_CVHLTYP_302001001_="302001001";//六座以下
PHCC_VHL_CVHLTYP_302001003_="302001003";//二十座以上
PHCC_VHL_CVHLTYP_302001008_="302001008";//六座至十座以下客车
PHCC_VHL_CVHLTYP_302001011_="302001011";//十座至二十座以下客车
PHCC_VHL_CVHLTYP_302001014_="302001014";//二十座至三十六座以下
PHCC_VHL_CVHLTYP_302001015_="302001015";//三十六座及三十六座以上
PHCC_VHL_CVHLTYP_302001016_="302001016";//十座及十座以上
PHCC_VHL_CVHLTYP_302001017_="302001017";//六座至十座客车
PHCC_VHL_CVHLTYP_302001022_="302001022";//六座以上
PHCC_VHL_CVHLTYP_302004005_="302004005";//摩托车50CC及以下
PHCC_VHL_CVHLTYP_302004006_="302004006";//摩托车50CC至250CC
"""


# 返回的保费解析 返回字典
# "036001"/>机动车损失保险（主险
# 036002机动车第三者责任保险（主险
# 036003机动车车上人员责任保险（司机）
# 036004机动车车上人员责任保险（乘客）
# 036005机动车全车盗抢险（主险
# 036006玻璃单独破碎险
# 036007自燃损失险
# 036012发动机涉水损失险
# 036013 车身划痕损失险
# 033201机动车交通事故强制责任险


def parseFee(body):
    Cvrg_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Cvrg_DW')]")[0]
    Base_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Base_DW')]")[0]
    VsTax_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.VsTax_DW')]")[0]
    PrmCoef_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.PrmCoef_DW')]")[0]
    dataObjVoList = jsonpath.jsonpath(Cvrg_DW, "$.dataObjVoList")
    Base_DW_dataObjVoList = jsonpath.jsonpath(Base_DW, "$.dataObjVoList")
    VsTax_DW_dataObjVoList = jsonpath.jsonpath(VsTax_DW, "$.dataObjVoList")
    PrmCoef_DW_dataObjVoList = jsonpath.jsonpath(PrmCoef_DW, "$.dataObjVoList")
    # print dataObjVoList[0][0]
    ls = dataObjVoList[0]
    dtall = {}
    for i in ls:
        dtone = {}
        CCvrgNo = i['attributeVoList']['Cvrg.CCvrgNo']['value']
        dtone['CCvrgNo'] = CCvrgNo
        if CCvrgNo == '036001':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            dtone['NAmt'] = NAmt
        elif CCvrgNo == '036002':
            NIndemLmt = i['attributeVoList']['Cvrg.NIndemLmt']['value']  # 保额
            dtone['NIndemLmt'] = NIndemLmt
        elif CCvrgNo == '036003':
            NPerAmt = i['attributeVoList']['Cvrg.NPerAmt']['value']  # 保额
            dtone['NPerAmt'] = NPerAmt
        elif CCvrgNo == '036004':
            NLiabDaysLmt = i['attributeVoList']['Cvrg.NLiabDaysLmt']['value']  # 人数
            NPerAmt = i['attributeVoList']['Cvrg.NPerAmt']['value']
            NAmt = int(NLiabDaysLmt) * int(NPerAmt)
            dtone['NAmt'] = NAmt
        elif CCvrgNo == '036005':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            dtone['NAmt'] = NAmt
        elif CCvrgNo == '036006':
            pass
        elif CCvrgNo == '036007':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            dtone['NAmt'] = NAmt
        elif CCvrgNo == '036012':
            pass
        elif CCvrgNo == '036013':
            NIndemLmt = i['attributeVoList']['Cvrg.NIndemLmt']['value']  # 保额
            dtone['NIndemLmt'] = NIndemLmt
        elif CCvrgNo == '033201':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            dtone['NAmt'] = NAmt
        elif CCvrgNo == '036022':
            pass

        NPrm = i['attributeVoList']['Cvrg.NPrm']['value']  # 含税保费
        NBefPrm = i['attributeVoList']['Cvrg.NPerPrm']['value']  # 险别保费(元)
        NDductPrm = i['attributeVoList']['Cvrg.NDductPrm']['value']  # 不计免赔保费(元
        NPureRiskPremium = i['attributeVoList']['Cvrg.NPureRiskPremium']['value']  # 基准纯风险保费(元)
        NNonDeductPureRiskPrm = i['attributeVoList']['Cvrg.NNonDeductPureRiskPrm']['value']  # 不计免赔基准纯风险保费(元)

        dtone['NPrm'] = NPrm
        dtone['NBefPrm'] = NBefPrm
        dtone['NDductPrm'] = NDductPrm
        dtone['NPureRiskPremium'] = NPureRiskPremium
        dtone['NNonDeductPureRiskPrm'] = NNonDeductPureRiskPrm
        dtall[CCvrgNo] = dtone
    SYdt = {}
    ls_Base_DW = Base_DW_dataObjVoList[0][0]['attributeVoList']
    SY_Base_NAmt = ls_Base_DW['SY_Base.NAmt']['value']  # 商业险信息保额
    SY_Base_NPrm = ls_Base_DW['SY_Base.NPrm']['value']  # 商业保费
    SY_Base_NNoTaxPrm = ls_Base_DW['SY_Base.NNoTaxPrm']['value']  # 商业不含税保费
    SY_Base_NAddedTax = ls_Base_DW['SY_Base.NAddedTax']['value']  # 商业增值税额
    SYdt['SY_Base_NAmt'] = SY_Base_NAmt
    SYdt['SY_Base_NPrm'] = SY_Base_NPrm
    SYdt['SY_Base_NNoTaxPrm'] = SY_Base_NNoTaxPrm
    SYdt['SY_Base_NAddedTax'] = SY_Base_NAddedTax
    # 交强险信息
    JQdt = {}
    JQ_Base_NAmt = ls_Base_DW['JQ_Base.NAmt']['value']  # JQ保额
    JQ_Base_NPrm = ls_Base_DW['JQ_Base.NPrm']['value']  # jq保费
    JQ_Base_NNoTaxPrm = ls_Base_DW['JQ_Base.NNoTaxPrm']['value']  # 不含税保费
    JQ_Base_NAddedTax = ls_Base_DW['JQ_Base.NAddedTax']['value']  # 增值税额
    JQdt['JQ_Base_NAmt'] = JQ_Base_NAmt
    JQdt['JQ_Base_NPrm'] = JQ_Base_NPrm
    JQdt['JQ_Base_NNoTaxPrm'] = JQ_Base_NNoTaxPrm
    JQdt['JQ_Base_NAddedTax'] = JQ_Base_NAddedTax
    # 车船税

    # ls_VsTax_DW = VsTax_DW_dataObjVoList[0][0]['attributeVoList']  # NAggTax
    ls_VsTax_DW = jsonpath.jsonpath(VsTax_DW_dataObjVoList, "$..attributeVoList")
    VsTax_NAggTax = ls_VsTax_DW[0]['VsTax.NAggTax']['value'] if ls_VsTax_DW is not False else ""  # 车船税
    JQdt['VsTax_NAggTax'] = VsTax_NAggTax


    # 系数
    ls_PrmCoef_DW = PrmCoef_DW_dataObjVoList[0][0]['attributeVoList']
    SY_PrmCoef_NCoef = ls_PrmCoef_DW['SY_PrmCoef.NCoef']['value']
    SYdt['SY_PrmCoef_NCoef'] = SY_PrmCoef_NCoef  # 商业系数
    JQ_PrmCoef_NCoef = ls_PrmCoef_DW['JQ_PrmCoef.NCoef']['value']
    JQdt['JQ_PrmCoef_NCoef'] = JQ_PrmCoef_NCoef  # 交强系数

    dtall['SY'] = SYdt
    dtall['JQ'] = JQdt
    # print(dtall)
    return dtall


# 解析续保用户的数据
def parse_renewal_data(body):
    dataObjs = re.findall(r"DATA:\[(.+?)\],", body, re.S)[0]
    dataObjs = dataObjs.strip().lstrip().rstrip("'").strip("'")
    soup = BeautifulSoup(dataObjs, "xml")
    attributenames = soup.findAll('attribute')
    # print(attributenames)
    dt = {}
    for i in attributenames:
        text = i.getText()
        key = i.attrs['name']
        value = i.attrs['value']
        dt[key] = value
    # print(json.dumps(dt, ensure_ascii=False, indent=4))
    return dt


"""
return
{
    "CAppTyp": "A",
    "TInsrncEndTm": "2016-12-31 23:59:59", #保险结束时间
    "CEngNo": "K24A42563601",               #发动机号码
    "TInsrncBgnTm": "2016-01-01 00:00:00", #保险开始时间
    "CProdNo": "0335",
    "CAppNo": "0515320201000335000590",
    "CPlateNo": "苏BG027F",
    "CVhlTyp": "302001001",
    "CFrmNo": "LHGCM567852063612",
    "NAmt": "300000",                      #保额合计
    "CModelCde": "BTAALD0010",              #车辆型号
    "CVin": "LHGCM567852063612",            #车架号
    "CPlyNo": "0115320201000335000069",    #保单号
    "CModelNme": "雅阁HG7240",             #车型名称
    "NPrm": "941.5",                     #保费合计
    "CDptCde": "32020101"
}
"""


# parse_renewal_data(renewal_data_demo)




# 解析续保用户的个人信息
def parse_renewal_data_userinfo(body):
    dt = {}
    Insured_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Insured_DW')]")[0]
    Insured_DW_dataObjVoList = jsonpath.jsonpath(Insured_DW, "$.dataObjVoList")
    CInsuredNme = Insured_DW_dataObjVoList[0][0]['attributeVoList']['Insured.CInsuredNme']['value']  # 用户名
    idCard = Insured_DW_dataObjVoList[0][0]['attributeVoList']['Insured.CCertfCde']['value']  # 身份证号码
    CMobile = Insured_DW_dataObjVoList[0][0]['attributeVoList']['Insured.CMobile']['value']  # 手机号
    Addr = Insured_DW_dataObjVoList[0][0]['attributeVoList']['Insured.CSuffixAddr']['value']  # 家庭住址

    Vhl_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Vhl_DW')]")[0]
    Vhl_DW_dataObjVoList = jsonpath.jsonpath(Vhl_DW, "$.dataObjVoList")
    CFrmNo = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.CFrmNo']['value']
    CPlateNo = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.CPlateNo']['value']
    CEngNo = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.CEngNo']['value']
    CModelCde = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.CModelCde']['value']
    CModelNme = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.CModelNme']['value']
    NNewPurchaseValue = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.NNewPurchaseValue']['value']
    CUsageCde = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['JQ_Vhl.CUsageCde']['value']
    CFstRegYm = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.CFstRegYm']['value']  # 注册时间
    NSeatNum = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.NSeatNum']['value']  # 座位数
    CCardDetail = Vhl_DW_dataObjVoList[0][0]['attributeVoList']['Vhl.CCardDetail']['value']  # k33
    # 获取交强险与商业险的开始结束时间
    Base_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Base_DW')]")[0]
    Base_DW_dataObjVoList = jsonpath.jsonpath(Base_DW, "$.dataObjVoList")
    syStart = Base_DW_dataObjVoList[0][0]['attributeVoList']['SY_Base.TInsrncBgnTm']['value']
    syEnd = Base_DW_dataObjVoList[0][0]['attributeVoList']['SY_Base.TInsrncEndTm']['value']
    jqStart = Base_DW_dataObjVoList[0][0]['attributeVoList']['JQ_Base.TInsrncBgnTm']['value']
    jqEnd = Base_DW_dataObjVoList[0][0]['attributeVoList']['JQ_Base.TInsrncEndTm']['value']
    SY_JQ_TIME = {}
    SY_JQ_TIME['syStart'] = getlatedate(-365, syStart.split(" ")[0])
    SY_JQ_TIME['syEnd'] = getlatedate(-365, syEnd.split(" ")[0])
    SY_JQ_TIME['jqStart'] = getlatedate(-365, jqStart.split(" ")[0])
    SY_JQ_TIME['jqEnd'] = getlatedate(-365, jqEnd.split(" ")[0])
    dt['insuredName'] = CInsuredNme
    dt['insuredAddress'] = Addr
    dt['identifyNumber'] = idCard
    dt['mobile'] = CMobile
    dt['vinNo'] = CFrmNo
    dt['licenseNo'] = CPlateNo
    dt['engineNo'] = CEngNo
    dt['CModelCde'] = CModelCde
    dt['brandName'] = CModelNme
    dt['NNewPurchaseValue'] = NNewPurchaseValue
    dt['CUsageCde'] = CUsageCde
    dt['enrollDate'] = CFstRegYm
    dt['NSeatNum'] = NSeatNum
    dt['CCardDetail'] = CCardDetail
    dt['insuranceTime'] = SY_JQ_TIME
    return dt


def cic_parse_lastyear_premium(body):
    # f=open("C:\Users\weikai\Desktop\\1","r")
    # body=eval(f.read())
    Cvrg_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Cvrg_DW')]")[0]
    dataObjVoList = jsonpath.jsonpath(Cvrg_DW, "$.dataObjVoList")[0]
    dtall = []
    for i in dataObjVoList:
        dtone = {}
        CCvrgNo = i['attributeVoList']['Cvrg.CCvrgNo']['value']
        dtone['CCvrgNo'] = CCvrgNo
        if CCvrgNo == '036001':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtone['NAmt'] = NAmt
            dtall.append(dtone)
        elif CCvrgNo == '036002':
            NIndemLmt = i['attributeVoList']['Cvrg.NIndemLmt']['value']  # 保额
            dtone['NIndemLmt'] = NIndemLmt
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtall.append(dtone)
        elif CCvrgNo == '036003':
            NPerAmt = i['attributeVoList']['Cvrg.NPerAmt']['value']  # 保额
            dtone['NPerAmt'] = NPerAmt
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtall.append(dtone)
        elif CCvrgNo == '036004':
            NLiabDaysLmt = i['attributeVoList']['Cvrg.NLiabDaysLmt']['value']  # 人数
            NPerAmt = i['attributeVoList']['Cvrg.NPerAmt']['value']
            NAmt = int(NLiabDaysLmt) * int(NPerAmt)
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtone['NAmt'] = NAmt
            dtall.append(dtone)
        elif CCvrgNo == '036005':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            dtone['NAmt'] = NAmt
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtall.append(dtone)
        elif CCvrgNo == '036006':
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
        elif CCvrgNo == '036022':
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
        elif CCvrgNo == '036007':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            dtone['NAmt'] = NAmt
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtall.append(dtone)
        elif CCvrgNo == '036012':
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
        elif CCvrgNo == '036013':
            NIndemLmt = i['attributeVoList']['Cvrg.NIndemLmt']['value']  # 保额
            dtone['NIndemLmt'] = NIndemLmt
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtall.append(dtone)
        elif CCvrgNo == '033201':
            NAmt = i['attributeVoList']['Cvrg.NAmt']['value']  # 保额
            dtone['NAmt'] = NAmt
            dtone['NPerPrm'] = i['attributeVoList']['Cvrg.NPerPrm']['value']
            CDductMrk = i['attributeVoList']['Cvrg.CDductMrk']['value']
            if CDductMrk != "":
                CDductMrk = "1"
            else:
                CDductMrk = "0"
            dtone['CDductMrk'] = CDductMrk
            dtall.append(dtone)

        carNickPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036013')")
        carDamagePremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036001')")
        carTheftPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036005')")
        otherHurtPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036002')")
        driverDutyPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036003')")
        passengerDutyPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036004')")
        glassBrokenPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036006')")
        carFirePremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036007')")
        engineWadingPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036012')")
        repairFactoryPremium = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='036022')")
        jq = jsonpath.jsonpath(dtall, "$.[?(@.CCvrgNo=='033201')]")

        Base_DW = jsonpath.jsonpath(body, "$.WEB_DATA[?(@.dwName=='prodDef.vhl.Base_DW')]")[0]
        Base_DW_dataObjVoList = jsonpath.jsonpath(Base_DW, "$.dataObjVoList")
        ls_Base_DW = Base_DW_dataObjVoList[0][0]['attributeVoList']
        SY_Base_NNoTaxPrm = ls_Base_DW['SY_Base.NNoTaxPrm']['value']  # 商业不含税保费
        SY_Base_NAddedTax = ls_Base_DW['SY_Base.NAddedTax']['value']  # 商业增值税额
        allamount = float(SY_Base_NNoTaxPrm if SY_Base_NNoTaxPrm != "" else "0") + float(
            SY_Base_NAddedTax if SY_Base_NAddedTax != "" else "0")
    msg2 = {
        'compulsoryInsurance': ("1" if jq != False else "0"), 'nAggTax': ("1" if jq != False else "0"),
        'otherHurtPremium': {"isCheck": ("1" if otherHurtPremium != False else "0"),
                             "Amount": (otherHurtPremium[0]['NIndemLmt'] if otherHurtPremium != False else "0")},
        'carNickPremium': {"isCheck": ("1" if carNickPremium != False else "0"),
                           "Amount": (carNickPremium[0]['NIndemLmt'] if carNickPremium != False else "0")},
        'driverDutyPremium': {"isCheck": ("1" if driverDutyPremium != False else "0"),
                              "Amount": (driverDutyPremium[0]['NPerAmt'] if driverDutyPremium != False else "0")},
        'passengerDutyPremium': {"isCheck": ("1" if passengerDutyPremium != False else "0"),
                                 "Amount": (passengerDutyPremium[0]['NAmt'] if passengerDutyPremium != False else "0")},
        'glassBrokenPremium': ("1" if glassBrokenPremium != False else "0"),
        'carFirePremium': ("1" if carFirePremium != False else "0"),
        'engineWadingPremium': ("1" if engineWadingPremium != False else "0"),
        'carTheftPremium': ("1" if carTheftPremium != False else "0"),
        'carDamagePremium': ("1" if carDamagePremium != False else "0"),
        'carDamageBenchMarkPremium': (carDamagePremium[0]['CDductMrk'] if carDamagePremium != False else "0"),
        'otherHurtBenchMarkPremium': (otherHurtPremium[0]['CDductMrk'] if otherHurtPremium != False else "0"),
        'carTheftBenchMarkPremium': (carTheftPremium[0]['CDductMrk'] if carTheftPremium != False else "0"),
        'driverDutyBenchMarkPremium': (driverDutyPremium[0]['CDductMrk'] if driverDutyPremium != False else "0"),
        'passengerBenchMarkPremium': (passengerDutyPremium[0]['CDductMrk'] if passengerDutyPremium != False else "0"),
        'carNickBenchMarkPremium': (carNickPremium[0]['CDductMrk'] if carNickPremium != False else "0"),
        'carFireBrokenBenchMarkPremium': (carFirePremium[0]['CDductMrk'] if carFirePremium != False else "0"),
        'engineWadingBenchMarkPremium': (engineWadingPremium[0]['CDductMrk'] if engineWadingPremium != False else "0"),
        'repairFactoryPremium': ("1" if repairFactoryPremium != False else "0"),
        'SySumPremium': allamount,
        'JqSumPremium': (jq[0]['NPerPrm'] if jq != False else "0")
    }
    return msg2


if __name__ == "__main__":
    # print parsedataObjs(demo)
    f = open("C:\Users\weikai\Desktop\\1.json", "r")
    body = eval(f.read())
    print parseFee(body)
    #print cic_parse_lastyear_premium(body)
    pass
