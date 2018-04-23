# -*- coding:utf-8 -*-
__author__ = 'weikai'
import urllib
import json
from request_cic import utils
from datetime import date
from datetime import datetime
from request_cic.insuranceType2 import get_insurance_type
from getUseYearCode import calc_user_years


# 日期比较 返回值 为大的日期
def compare_date(str_date1, str_date2):
    str_date1 = str_date1.split(" ")[0]
    str_date2 = str_date2.split(" ")[0]
    str_date1 = datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2 = datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date() >= str_date2.date():
        return str(str_date1.date())
    else:
        return str(str_date2.date())


def getFeebody(fee):
    insuranceType = fee.get("insuranceType", {})
    # endDate = JQ_fTInsrncBgnTm = fee.get("endDate", "")
    '''
    if endDate != "":
        # 保险结束时间与当前时间比较
        datestr = compare_date(endDate, utils.getlatedate(0))
        TLastSaliEndDate = ""
        SY_fTInsrncBgnTm = utils.getlatedate(1, datestr) + ' 00:00:00'  # 保险起止期(商)
        SY_fTInsrncEndTm = utils.getlatedate(365, datestr) + " 23:59:59"  # 保险起止期(商)
        JQ_fTInsrncBgnTm = utils.getlatedate(1, datestr) + " 00:00:00"  # 保险起止期(交)
        JQ_fTInsrncEndTm = utils.getlatedate(365, datestr) + " 23:59:59"  # 保险起止期(交)
    else:
        TLastSaliEndDate = utils.getlatedate(0)  ##当前日期
        SY_fTInsrncBgnTm = utils.getlatedate(1) + ' 00:00:00'  # 保险起止期(商)
        SY_fTInsrncEndTm = utils.getlatedate(365) + " 23:59:59"  # 保险起止期(商)
        JQ_fTInsrncBgnTm = utils.getlatedate(1) + " 00:00:00"  # 保险起止期(交)
        JQ_fTInsrncEndTm = utils.getlatedate(365) + " 23:59:59"  # 保险起止期(交)
    '''
    SY_fTInsrncBgnTm = fee.get("syStart", utils.getlatedate(1)) + ' 00:00:00'  # 保险起止期(商)
    SY_fTInsrncEndTm = utils.getlatedate(364, SY_fTInsrncBgnTm.split(" ")[0]) + " 23:59:59"  # 保险起止期(商)
    JQ_fTInsrncBgnTm = fee.get("jqStart", utils.getlatedate(1)) + " 00:00:00"  # 保险起止期(交)
    JQ_fTInsrncEndTm = utils.getlatedate(364, SY_fTInsrncBgnTm.split(" ")[0]) + " 23:59:59"  # 保险起止期(交)

    JQ__fCTmSysCde = "365"  # 默认间隔
    SY__fCTmSysCde = "365"  # 默认间隔
    fTOprTm = fTAppTm = utils.getlatedate(0)  ##当前日期
    fCOprCde = "ex_fanglulu001"  # 用户名

    JQgCVhlTyp = fee['JQgCVhlTyp']
    SYgCVhlTyp = fee['SYgCVhlTyp']
    gNNewPurchaseTaxValue = fee['gNNewPurchaseTaxValue']  # 新车购置价(含税)
    gNKindredPrice = fee['gNKindredPrice']  # 类比价格
    gNKindredPriceTax = fee['gNKindredPriceTax']  # 类比价(含税)
    gNNewPurchaseValue = fee['gNNewPurchaseValue']  # >新车购置价
    gNDiscussActualValue = fee['gNDiscussActualValue']  # 协商实际价值
    gCFrmNo = gCVin = fee['gCFrmNo']  # 车架号
    gCMonDespRate = fee['gCMonDespRate']  # 月折旧率
    gNActualValue = fee['gNActualValue']  # <!-- 车辆实际价值 -->
    gNOfferPurChasePriceMax = fee['gNOfferPurChasePriceMax']  # 新车购置价浮动上限
    gNOfferPurChasePriceMin = fee['gNOfferPurChasePriceMin']  # 新车购置价浮动下
    gCIndustryModelCode = fee['gCIndustryModelCode']  # 行业车型编码
    gCIndustryModelName = fee['gCIndustryModelName']  # 行业车型名称
    gCNoticeType = fee['gCNoticeType']  # 行业公告车型
    gCProdPlace = "0"  # 系别名称"0";//国产 "1";//进口 "2";//合资 fee['gCProdPlace']=
    gCFamilyCode = fee['gCFamilyCode']  # 车系编码
    gCFamilyName = fee['gCFamilyName']  # 车系名称
    gCFstRegYm = fee['gCFstRegYm']  # 初登日期
    gCModelNme = fee['gCModelNme']  # 车型名称
    gCBrandId = fee['gCBrandId']
    gCModelCde = fee['gCModelCde']  # 精友车型代码
    gCSearchCode = fee['gCSearchCode']  # code查询码
    gCValidateCode = fee['gCValidateCode']  # 验证码
    gCPlateNo = fee['gCPlateNo']  # 车牌
    gCEngNo = fee['gCEngNo']  # 发动机
    gNDisplacement = NExhaustCapacity = fee['gNDisplacement']  # 排气量
    gCPlateTyp = fee['gCPlateTyp']  # 号牌种类
    try:
        gCCarAge = calc_user_years(SY_fTInsrncBgnTm.split(" ")[0], gCFstRegYm)
        fee['gCCarAge'] = gCCarAge
    except:
        fee['gCCarAge'] = gCCarAge = "306007"
    # 车龄等级???????????????????????????
    gNSeatNum = fee['gNSeatNum']  # 座位数
    gNPoWeight = fee['gNPoWeight']  # 整备质量
    gNTonage = fee['RVehlcleTonnage']
    # 机动车损失保险（主险）#保额-----------------------------------------
    lNVhlActVal = lNAmt_036001 = fee['lNVhlActVal']  # 机动车损失保险（主险）#保额
    fee['lNDeductible_036001'] = lNDeductible_036001 = "2000"  # 免赔额
    fee[
        'lNDductRate_036001'] = lNDductRate_036001 = "0.15"  # http://carply.cic.cn/pcis/policy/universal/quickapp/vhl_quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0&id=479A78C22656FB9CAFE2C29B6280C930
    # 玻璃单独破碎险##################################################
    # fee['lNAmt_036002']=lNAmt_036002="036002" #玻璃单独破碎险
    # fee['lNAmt_036002']=lNAmt_036002=lNIndemLmt_036002="500000"
    # fee['lCIndemLmtLvl_036002']=lCIndemLmtLvl_036002="306006009" #50万
    # fee['lNDductRate__036002']=lNDductRate__036002="0.15"
    ####################机动车车上人员责任保险（司机）###############
    # fee['lNDductRate_036003']=lNDductRate_036003="0.15"
    ####################机动车车上人员责任保险（乘客）###############
    lNLiabDaysLmt_036004 = int(fee['gNSeatNum']) - 1  # 座位数-1
    ######################机动车全车盗窃保险（主险）</################
    lNVhlActVal_036005 = lNAmt_036005 = fee['lNVhlActVal_036005']
    # fee['lNDductRate_036005']=lNDductRate_036005="0.2"
    ########################机动车交通事故强制责任险@#####################
    # fee['lNAmt_033201']=lNAmt_033201='122000'
    ########玻璃单独破碎险
    fee['_l_s30'] = _l_s30 = "303011001"  # 国产
    # 自燃损失险
    lNVhlActVal_036007 = NAmt_036007 = fee['lNVhlActVal_036007']  # 自燃损失险
    # fee['lNDductRate_036007']=lNDductRate_036007="0.2"
    ##########发动机涉水损失险#############
    ###############车身划痕损失险##############
    # fee['lNAmt_036013']=lNAmt_036013="2000"
    # fee['lCIndemLmtLvl_306013']=lCIndemLmtLvl_306013="N03001001" #// 2000元
    # lNDductRate_306013="0.15"
    ###交通违法次数
    hCAppNme = iCInsuredNme = jCOwnerNme = fee['hCAppNme']
    jCGender = fee['jCGender']  # "1061"#男
    jCOwnerAge = fee['jCOwnerAge']  # ="341060"#年龄阶段
    # fee['NExhaustCapacity']=NExhaustCapacity="2.354" #排气量

    NCurbWt = fee['NCurbWt']  # 整备质量(吨)
    CTaxItemCde = '398014'
    gCRegVhlTyp = gCCardDetail = fee['gCRegVhlTyp']  # ='K33'
    """
    PHCC_VHL_CARAGE_341023="341023";//1年以下
    PHCC_VHL_CARAGE_341024="341024";//	1-2年
    PHCC_VHL_CARAGE_341025="341025";//	2-6年
    PHCC_VHL_CARAGE_341026="341026";//	6年以上
    PHCC_VHL_CARAGE_341027="341027";//	2年以下
    PHCC_VHL_CARAGE_341029="341029";//	2-3年
    PHCC_VHL_CARAGE_341030="341030";//	3-4年
    PHCC_VHL_CARAGE_341031="341031";//	4年以上
    """
    # http://carply.cic.cn/pcis/core/js/compress/vhl_offer_app.js?version=704557
    # 9900行 判断税目
    if int(gNSeatNum) <= 9 and int(float(gNDisplacement) * 1000) <= 1000:
        CTaxItemCde = "398013"  # ["398013", "乘用车9人（含）以下排量1.0升（含）以下的"]
    elif int(gNSeatNum) <= 9 and int(float(gNDisplacement) * 1000) > 1000 and int(float(gNDisplacement) * 1000) <= 1600:
        CTaxItemCde = "398014"  # ["398014", "乘用车9人（含）以下排量1.0升以上至1.6升（含）的"]);
    elif int(gNSeatNum) <= 9 and int(float(gNDisplacement) * 1000) > 1600 and int(float(gNDisplacement) * 1000) <= 2000:
        CTaxItemCde = "398015"  # ["398015", "乘用车9人（含）以下排量1.6升以上至2.0升（含）的"]);
    elif int(gNSeatNum) <= 9 and int(float(gNDisplacement) * 1000) > 2000 and int(float(gNDisplacement) * 1000) <= 2500:
        CTaxItemCde = "398016"  # ["398016", "乘用车9人（含）以下排量2.0升以上至2.5升（含）的"]);
    elif int(gNSeatNum) <= 9 and int(float(gNDisplacement) * 1000) > 2500 and int(float(gNDisplacement) * 1000) <= 3000:
        CTaxItemCde = "398017"  # ["398017", "乘用车9人（含）以下排量2.5升以上至3.0升（含）的"]);
    elif int(gNSeatNum) <= 9 and int(float(gNDisplacement) * 1000) > 3000 and int(float(gNDisplacement) * 1000) <= 4000:
        CTaxItemCde = "398018"  # ["398017", "乘用车9人（含）以下排量2.5升以上至3.0升（含）的"]);
    elif int(gNSeatNum) <= 9 and int(float(gNDisplacement) * 1000) > 4000:
        CTaxItemCde = "398019"  # ["398017", "乘用车9人（含）以下排量2.5升以上至3.0升（含）的"]);
    elif int(gNSeatNum) > 9 and int(gNSeatNum) < 20:
        CTaxItemCde = "398020"  # ["398020", "商用车9人以上20人以下的中型客车及电车"]);
    elif int(gNSeatNum) >= 20:
        CTaxItemCde = "398021"  # ["398021", "商用车20人以上(含)的大型客车及电车"]);

    body = '''
  [
  {
    "isFilter": "false",
    "dwType": "ONLY_DATA",
    "dwName": "prodDef.vhl.Base_DW",
    "rsCount": "5",
    "pageSize": "8",
    "pageNo": "1",
    "pageCount": "1",
    "maxCount": "undefined",
    "toAddFlag": "false",
    "filterMapList": [

    ],
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "false",
        "status": "UPDATED",
        "attributeVoList": [
          {
            _-a"_-fCRenewMrk",
            _-b""
          },
          {
            _-a"SY__-fCAppNo",
            _-b""
          },
          {
            _-a"JQ__-fCAppNo",
            _-b""
          },
          {
            _-a"JQ__-fCOfferNo",
            _-b""
          },
          {
            _-a"SY__-fCOfferNo",
            _-b""
          },
          {
            _-a"JQ__-fNRiskCost",
            _-b""
          },
          {
            _-a"SY__-fNRiskCost",
            _-b""
          },
          {
            _-a"JQ__-fNTargetPrm",
            _-b""
          },
          {
            _-a"SY__-fNTargetPrm",
            _-b""
          },
          {
            _-a"JQ__-fNProfitRatio",
            _-b""
          },
          {
            _-a"SY__-fNProfitRatio",
            _-b""
          },
          {
            _-a"JQ__-fNPayRatio",
            _-b""
          },
          {
            _-a"_-fCPayRatioLevel",
            _-b""
          },
          {
            _-a"SY__-fNPayRatio",
            _-b""
          },
          {
            _-a"_-fNDoubleRiskCost",
            _-b""
          },
          {
            _-a"_-fNDoublePrm",
            _-b""
          },
          {
            _-a"_-fNDoublePayRatio",
            _-b""
          },
          {
            _-a"_-fCDoublePayRatioLevel",
            _-b""
          },
          {
            _-a"JQ__-fNCostRatio",
            _-b""
          },
          {
            _-a"SY__-fNCostRatio",
            _-b""
          },
          {
            _-a"JQ__-fNCostRate",
            _-b""
          },
          {
            _-a"SY__-fNCostRate",
            _-b""
          },
          {
            _-a"JQ__-fCCostRatioLevel",
            _-b""
          },
          {
            _-a"SY__-fCCostRatioLevel",
            _-b""
          },
          {
            _-a"_-fNDoubleCostRate",
            _-b""
          },
          {
            _-a"_-fNDoubleCostRatio",
            _-b""
          },
          {
            _-a"_-fCDoubleCostRatioLevel",
            _-b""
          },
          {
            _-a"_-fCCommonFlag",
            _-b"0"
          },
          {
            _-a"_-fCAppTyp",
            _-b"A"
          },
          {
            _-a"SY__-fCPlyNo",
            _-b""
          },
          {
            _-a"JQ__-fCPlyNo",
            _-b""
          },
          {
            _-a"_-fNEdrPrjNo",
            _-b""
          },
          {
            _-a"_-fCRelPlyNo",
            _-b""
          },
          {
            _-a"_-fCProdNo",
            _-b"${SY_JQ_fCProdNo}"
          },
          {
            _-a"_-fCDptCde",
            _-b"32010702"
          },
          {
            _-a"_-fCSlsCde",
            _-b""
          },
          {
            _-a"_-fCHandLe",
            _-b""
          },
          {
            _-a"_-fCBsnsTyp",
            _-b"1900101"
          },
          {
            _-a"_-fCChaType",
            _-b""
          },
          {
            _-a"_-fCBsnsSubtyp",
            _-b""
          },
          {
            _-a"_-fCBrkrCde",
            _-b""
          },
          {
            _-a"_-fCBrkrName",
            _-b""
          },
          {
            _-a"_-fCSaleNme",
            _-b""
          },
          {
            _-a"_-fCAgtAgrNo",
            _-b""
          },
          {
            _-a"_-fNSubCoNo",
            _-b""
          },
          {
            _-a"_-fNCommRate",
            _-b""
          },
          {
            _-a"_-fNCommissionRateUpper",
            _-b""
          },
          {
            _-a"SY__-fCRenewMrk",
            _-b""
          },
          {
            _-a"JQ__-fCRenewMrk",
            _-b""
          },
          {
            _-a"JQ__-fCTrunMrk",
            _-b"0"
          },
          {
            _-a"SY__-fCTrunMrk",
            _-b"0"
          },
          {
            _-a"_-fCPlyTyp",
            _-b""
          },
          {
            _-a"JQ__-fCOrigPlyNo",
            _-b""
          },
          {
            _-a"SY__-fCOrigPlyNo",
            _-b""
          },
          {
            _-a"_-fCOrigInsurer",
            _-b""
          },
          {
            _-a"_-fCAmtCur",
            _-b""
          },
          {
            _-a"SY__-fNAmt",
            _-b"0.00"
          },
          {
            _-a"JQ__-fNAmt",
            _-b"122000.00"
          },
          {
            _-a"_-fNAmtRmbExch",
            _-b""
          },
          {
            _-a"_-fCPrmCur",
            _-b""
          },
          {
            _-a"SY__-fNCalcPrm",
            _-b""
          },
          {
            _-a"JQ__-fNCalcPrm",
            _-b""
          },
          {
            _-a"SY__-fNPrm",
            _-b"0.00"
          },
          {
            _-a"JQ__-fNPrm",
            _-b"0.00"
          },
          {
            _-a"_-fNPrmRmbExch",
            _-b"1"
          },
          {
            _-a"_-fNIndemLmt",
            _-b""
          },
          {
            _-a"_-fCRatioTyp",
            _-b"D"
          },
          {
            _-a"SY__-fNRatioCoef",
            _-b"1"
          },
          {
            _-a"JQ__-fNRatioCoef",
            _-b"1"
          },
          {
            _-a"_-fNSavingAmt",
            _-b""
          },
          {
            _-a"_-fCPlySts",
            _-b""
          },
          {
            _-a"_-fTTermnTm",
            _-b""
          },
          {
            _-a"_-fCInwdMrk",
            _-b""
          },
          {
            _-a"_-fCCiMrk",
            _-b""
          },
          {
            _-a"_-fCCiTyp",
            _-b""
          },
          {
            _-a"_-fNCiJntAmt",
            _-b""
          },
          {
            _-a"_-fNCiJntPrm",
            _-b""
          },
          {
            _-a"_-fCLongTermMrk",
            _-b""
          },
          {
            _-a"_-fTAppTm",
            _-b"${fTOprTm}"
          },
          {
            _-a"_-fCOprTyp",
            _-b""
          },
          {
            _-a"_-fCPrnNo",
            _-b""
          },
          {
            _-a"_-fCIcCardId",
            _-b""
          },
          {
            _-a"SY__-fTInsrncBgnTm",
            _-b"${SY_fTInsrncBgnTm}"
          },
          {
            _-a"SY__-fTInsrncEndTm",
            _-b"${SY_fTInsrncEndTm}"
          },
          {
            _-a"SY__-fCTmSysCde",
            _-b"${SY__fCTmSysCde}"
          },
          {
            _-a"JQ__-fTInsrncBgnTm",
            _-b"${JQ_fTInsrncBgnTm}"
          },
          {
            _-a"JQ__-fTInsrncEndTm",
            _-b"${JQ_fTInsrncEndTm}"
          },
          {
            _-a"JQ__-fCTmSysCde",
            _-b"${JQ__fCTmSysCde}"
          },
          {
            _-a"SY__-fCUnfixSpc",
            _-b""
          },
          {
            _-a"JQ__-fCUnfixSpc",
            _-b""
          },
          {
            _-a"_-fCGrpMrk",
            _-b""
          },
          {
            _-a"_-fCListorcolMrk",
            _-b""
          },
          {
            _-a"_-fCMasterMrk",
            _-b""
          },
          {
            _-a"_-fCPkgNo",
            _-b""
          },
          {
            _-a"_-fCRegMrk",
            _-b""
          },
          {
            _-a"_-fCDecMrk",
            _-b""
          },
          {
            _-a"_-fCJuriCde",
            _-b""
          },
          {
            _-a"_-fCAgriMrk",
            _-b"0"
          },
          {
            _-a"_-fCForeignMrk",
            _-b""
          },
          {
            _-a"_-fCImporexpMrk",
            _-b""
          },
          {
            _-a"JQ__-fCManualMrk",
            _-b""
          },
          {
            _-a"SY__-fCManualMrk",
            _-b""
          },
          {
            _-a"_-fCManualMrk",
            _-b""
          },
          {
            _-a"_-fCInstMrk",
            _-b""
          },
          {
            _-a"_-fCVipMrk",
            _-b""
          },
          {
            _-a"_-fCOpenCoverNo",
            _-b""
          },
          {
            _-a"_-fCDisptSttlCde",
            _-b"007001"
          },
          {
            _-a"_-fCDisptSttlOrg",
            _-b""
          },
          {
            _-a"_-fCOprCde",
            _-b"${fCOprCde}"
          },
          {
            _-a"_-fTOprTm",
            _-b"${fTOprTm}"
          },
          {
            _-a"_-fCChkCde",
            _-b""
          },
          {
            _-a"_-fTIssueTm",
            _-b""
          },
          {
            _-a"_-fTUdrTm",
            _-b""
          },
          {
            _-a"_-fCUdrDptCde",
            _-b""
          },
          {
            _-a"_-fCUdrCde",
            _-b""
          },
          {
            _-a"_-fCUdrMrk",
            _-b""
          },
          {
            _-a"_-fCRiFacMrk",
            _-b""
          },
          {
            _-a"_-fCRiChkCde",
            _-b""
          },
          {
            _-a"_-fCRiMrk",
            _-b""
          },
          {
            _-a"_-fTNextEdrBgnTm",
            _-b""
          },
          {
            _-a"_-fTNextEdrEndTm",
            _-b""
          },
          {
            _-a"_-fTNextEdrUdrTm",
            _-b""
          },
          {
            _-a"_-fCRemark",
            _-b""
          },
          {
            _-a"_-fTEdrAppTm",
            _-b""
          },
          {
            _-a"_-fTEdrBgnTm",
            _-b""
          },
          {
            _-a"_-fTEdrEndTm",
            _-b""
          },
          {
            _-a"_-fCEdrMrk",
            _-b""
          },
          {
            _-a"_-fCEdrType",
            _-b""
          },
          {
            _-a"_-fCCrtCde",
            _-b""
          },
          {
            _-a"_-fTCrtTm",
            _-b""
          },
          {
            _-a"_-fCUpdCde",
            _-b""
          },
          {
            _-a"SY__-fTUpdTm",
            _-b""
          },
          {
            _-a"JQ__-fTUpdTm",
            _-b""
          },
          {
            _-a"_-fNRate",
            _-b""
          },
          {
            _-a"_-f_-s1",
            _-b""
          },
          {
            _-a"_-f_-s2",
            _-b""
          },
          {
            _-a"_-f_-s3",
            _-b""
          },
          {
            _-a"_-f_-s4",
            _-b""
          },
          {
            _-a"_-fCLatestMrk",
            _-b""
          },
          {
            _-a"_-fCBidMrk",
            _-b""
          },
          {
            _-a"_-fCPrmSts",
            _-b""
          },
          {
            _-a"_-fNAmtVar",
            _-b""
          },
          {
            _-a"_-fNCalcPrmVar",
            _-b""
          },
          {
            _-a"_-fNPrmVar",
            _-b""
          },
          {
            _-a"_-fNIndemLmtVar",
            _-b""
          },
          {
            _-a"_-fCAppPrsnCde",
            _-b""
          },
          {
            _-a"_-fCAppPrsnNme",
            _-b""
          },
          {
            _-a"_-fCEdrCtnt",
            _-b""
          },
          {
            _-a"_-fCOcPlyNo",
            _-b""
          },
          {
            _-a"_-fCRevertMrk",
            _-b""
          },
          {
            _-a"_-fCEdrRsnBundleCde",
            _-b""
          },
          {
            _-a"_-fNBefEdrPrjNo",
            _-b""
          },
          {
            _-a"_-fNBefEdrAmt",
            _-b""
          },
          {
            _-a"_-fNBefEdrPrm",
            _-b""
          },
          {
            _-a"_-fCEdrNo",
            _-b""
          },
          {
            _-a"JQ__-fCEdrNo",
            _-b""
          },
          {
            _-a"SY__-fCEdrNo",
            _-b""
          },
          {
            _-a"_-fNPrmDisc",
            _-b""
          },
          {
            _-a"_-fNDiscRate",
            _-b""
          },
          {
            _-a"_-fNMaxFeeProp",
            _-b""
          },
          {
            _-a"_-fCFinTyp",
            _-b"001"
          },
          {
            _-a"_-fCGrantDptCde",
            _-b""
          },
          {
            _-a"_-fCVipCus",
            _-b""
          },
          {
            _-a"_-fNOrigTimes",
            _-b""
          },
          {
            _-a"_-fCDptAttr",
            _-b""
          },
          {
            _-a"_-fCSalegrpCde",
            _-b""
          },
          {
            _-a"_-fCSlsId",
            _-b""
          },
          {
            _-a"_-fCSlsTel",
            _-b""
          },
          {
            _-a"_-fCSlsNme",
            _-b""
          },
          {
            _-a"_-fCMinUndrDpt",
            _-b""
          },
          {
            _-a"_-fCMinUndrCls",
            _-b""
          },
          {
            _-a"_-fCPkgMrk",
            _-b""
          },
          {
            _-a"_-fCAppStatus",
            _-b""
          },
          {
            _-a"JQ__-fCImmeffMrk",
            _-b""
          },
          {
            _-a"SY__-fCImmeffMrk",
            _-b""
          },
          {
            _-a"_-fCInsrncTm",
            _-b""
          },
          {
            _-a"_-fNBasePrm",
            _-b""
          },
          {
            _-a"_-fNAllPrm",
            _-b""
          },
          {
            _-a"_-fCSusBusiness",
            _-b""
          },
          {
            _-a"JQ__-fCNewFlg",
            _-b"1"
          },
          {
            _-a"SY__-fCNewFlg",
            _-b"1"
          },
          {
            _-a"_-fTInsrncTm",
            _-b""
          },
          {
            _-a"_-fCOprNm",
            _-b""
          },
          {
            _-a"_-fCSaleTeam",
            _-b""
          },
          {
            _-a"_-fCAgantPer",
            _-b""
          },
          {
            _-a"_-fCVisInsure",
            _-b""
          },
          {
            _-a"_-fCIsTender",
            _-b""
          },
          {
            _-a"_-fCTenderNo",
            _-b""
          },
          {
            _-a"_-fTRepstopExtLastEndTm",
            _-b""
          },
          {
            _-a"_-fCRepstopextStatus",
            _-b""
          },
          {
            _-a"_-fTRepStopExtBgnTm",
            _-b""
          },
          {
            _-a"_-fTRepStopExtEndTm",
            _-b""
          },
          {
            _-a"_-fCRepStopExtRleAppNo",
            _-b""
          },
          {
            _-a"_-fTUntilDate",
            _-b""
          },
          {
            _-a"_-fCMkupFlag",
            _-b""
          },
          {
            _-a"_-fCGrpBaseMrk",
            _-b""
          },
          {
            _-a"_-fCComputerIp",
            _-b""
          },
          {
            _-a"_-fCUsbKey",
            _-b""
          },
          {
            _-a"_-fCPosNo",
            _-b""
          },
          {
            _-a"_-fCChaNmeCode",
            _-b"B"
          },
          {
            _-a"_-fCChannelNme",
            _-b""
          },
          {
            _-a"_-fCNewChaType",
            _-b"B01"
          },
          {
            _-a"_-fCNewBsnsTyp",
            _-b"B0105"
          },
          {
            _-a"_-fCServiceCode",
            _-b""
          },
          {
            _-a"_-fCTeamCode",
            _-b""
          },
          {
            _-a"_-fCTeamName",
            _-b""
          },
          {
            _-a"_-fCServiceId",
            _-b""
          },
          {
            _-a"_-fCPubNetFlag",
            _-b""
          },
          {
            _-a"_-fCDeptName",
            _-b""
          },
          {
            _-a"_-fCAppointAreaCode",
            _-b""
          },
          {
            _-a"_-fCIsFullEndor",
            _-b""
          },
          {
            _-a"_-fNAdditionalCostRate",
            _-b""
          },
          {
            _-a"_-fCOfferPlan",
            _-b"A"
          },
          {
            _-a"_-fCClauseType",
            _-b"01"
          },
          {
            _-a"_-fCPrmCalcProTyp",
            _-b""
          },
          {
            _-a"_-fCPriskPremFlag",
            _-b""
          },
          {
            _-a"_-fNCarLossPrm",
            _-b""
          },
          {
            _-a"JQ__-fCOfferUseSpc",
            _-b""
          },
          {
            _-a"SY__-fCOfferUseSpc",
            _-b""
          },
          {
            _-a"_-fCOperDpt",
            _-b""
          },
          {
            _-a"_-fCPayAgreement",
            _-b""
          },
          {
            _-a"_-fNIncrementRate",
            _-b""
          },
          {
            _-a"JQ__-fNNoTaxPrm",
            _-b""
          },
          {
            _-a"SY__-fNNoTaxPrm",
            _-b""
          },
          {
            _-a"JQ__-fNAddedTax",
            _-b""
          },
          {
            _-a"SY__-fNAddedTax",
            _-b""
          },
          {
            _-a"_-fCDataSrc",
            _-b""
          },
          {
            _-a"_-fNExpectPayrate",
            _-b""
          },
          {
            _-a"_-fCFiMrk",
            _-b""
          },
          {
            _-a"_-fNJsPrm",
            _-b""
          },
          {
            _-a"_-fNJsAmt",
            _-b""
          },
          {
            _-a"_-fNJcPrm",
            _-b""
          },
          {
            _-a"_-fNJcAmt",
            _-b""
          },
          {
            _-a"_-fCPropertyMrk",
            _-b""
          },
          {
            _-a"_-fNPropertyPrm",
            _-b""
          },
          {
            _-a"_-fNPropertyAmt",
            _-b""
          },
          {
            _-a"_-fCCvrgResult",
            _-b""
          }
        ]
      }
    ]
  },
  {
    "isFilter": "false",
    "dwType": "ONLY_DATA",
    "dwName": "prodDef.vhl.Vhl_DW",
    "rsCount": "1",
    "pageSize": "10",
    "pageNo": "1",
    "pageCount": "0",
    "maxCount": "1000",
    "toAddFlag": "false",
    "filterMapList": [

    ],
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            _-a"_-gNNewPurchaseTaxValue",
            _-b"${gNNewPurchaseTaxValue}"
          },
          {
            _-a"_-gNKindredPrice",
            _-b"${gNKindredPrice}"
          },
          {
            _-a"_-gNKindredPriceTax",
            _-b"${gNKindredPriceTax}"
          },
          {
            _-a"_-gCVin",
            _-b"${gCFrmNo}"
          },
          {
            _-a"_-gCMonDespRate",
            _-b"${gCMonDespRate}"
          },
          {
            _-a"_-gNActualValue",
            _-b"${gNActualValue}"
          },
          {
            _-a"_-gCLoanVehicleFlag",
            _-b"0"
          },
          {
            _-a"JQ__-gCQryCde",
            _-b""
          },
          {
            _-a"SY__-gCQryCde",
            _-b""
          },
          {
            _-a"_-gCVehlcleFamily",
            _-b""
          },
          {
            _-a"_-gCModelDesc",
            _-b""
          },
          {
            _-a"_-gRMarketDate",
            _-b""
          },
          {
            _-a"_-gNAssignPrice",
            _-b""
          },
          {
            _-a"_-gNOfferPurChasePrice",
            _-b""
          },
          {
            _-a"_-gNOfferPurChasePriceMax",
            _-b"${gNOfferPurChasePriceMax}"
          },
          {
            _-a"_-gNOfferPurChasePriceMin",
            _-b"${gNOfferPurChasePriceMin}"
          },
          {
            _-a"_-gCSnModifyPrices",
            _-b"0"
          },
          {
            _-a"_-gCXnModifyPrices",
            _-b"0"
          },
          {
            _-a"_-gCFleetMrk",
            _-b"0"
          },
          {
            _-a"_-gCVhlPkgNO",
            _-b""
          },
          {
            _-a"_-gCIndustryModelCode",
            _-b"${gCIndustryModelCode}"
          },
          {
            _-a"_-gCIndustryModelName",
            _-b"${gCIndustryModelName}"
          },
          {
            _-a"_-gCNoticeType",
            _-b"${gCNoticeType}"
          },
          {
            _-a"_-gCProdPlace",
            _-b"${gCProdPlace}"
          },
          {
            _-a"_-gCHfcode",
            _-b"0"
          },
          {
            _-a"_-gCDragWeight",
            _-b""
          },
          {
            _-a"_-gCFamilyCode",
            _-b"${gCFamilyCode}"
          },
          {
            _-a"_-gCFamilyName",
            _-b"${gCFamilyName}"
          },
          {
            _-a"_-gCEcdemicMrk",
            _-b"0"
          },
          {
            _-a"_-gCDevice1Mrk",
            _-b"0"
          },
          {
            _-a"_-gCNewVhlFlag",
            _-b"1"
          },
          {
            _-a"_-gCNewMrk",
            _-b"0"
          },
          {
            _-a"_-gCFstRegYm",
            _-b"${gCFstRegYm}"
          },
          {
            _-a"_-gCFrmNo",
            _-b"${gCFrmNo}"
          },
          {
            _-a"_-gCModelNme",
            _-b"${gCModelNme}"
          },
          {
            _-a"CarModel",
            _-b""
          },
          {
            _-a"searcheVehicleModel",
            _-b""
          },
          {
            _-a"queryPlateCarInfo",
            _-b""
          },
          {
            _-a"_-gCBrandId",
            _-b"${gCBrandId}"
          },
          {
            _-a"_-gCModelCde",
            _-b"${gCModelCde}"
          },
          {
            _-a"_-gCModelCde2",
            _-b""
          },
          {
            _-a"CarSerachValidate",
            _-b""
          },
          {
            _-a"CarSerachConfirm",
            _-b""
          },
          {
            _-a"_-gCSearchCode",
            _-b"${gCSearchCode}"
          },
          {
            _-a"_-gCValidateCode",
            _-b"${gCValidateCode}"
          },
          {
            _-a"_-gCPlateNo",
            _-b"${gCPlateNo}"
          },
          {
            _-a"_-gCEngNo",
            _-b"${gCEngNo}"
          },
          {
            _-a"_-gNDisplacement",
            _-b"${gNDisplacement}"
          },
          {
            _-a"_-gCPlateTyp",
            _-b"${gCPlateTyp}"
          },
          {
            _-a"_-gNNewPurchaseValue",
            _-b"${gNNewPurchaseValue}"
          },
          {
            _-a"_-gNDiscussActualValue",
            _-b"${gNDiscussActualValue}"
          },
          {
            _-a"JQ__-gCUsageCde",
            _-b"309001"
          },
          {
            _-a"JQ__-gCVhlTyp",
            _-b"${JQgCVhlTyp}"
          },
          {
            _-a"_-gCCarAge",
            _-b"${gCCarAge}"
          },
          {
            _-a"SY__-gCUsageCde",
            _-b"309001"
          },
          {
            _-a"SY__-gCVhlTyp",
            _-b"${SYgCVhlTyp}"
          },
          {
            _-a"SY__-g_-s6",
            _-b"11"
          },
          {
            _-a"_-gCRegVhlTyp",
            _-b"${gCRegVhlTyp}"
          },
          {
            _-a"_-gCCardDetail",
            _-b"${gCRegVhlTyp}"
          },
          {
            _-a"_-gCNatOfBusines",
            _-b"359002"
          },
          {
            _-a"_-gNTonage",
            _-b"${gNTonage}"
          },
          {
            _-a"_-gNSeatNum",
            _-b"${gNSeatNum}"
          },
          {
            _-a"_-gTTransferDate",
            _-b""
          },
          {
            _-a"_-gCBillDate",
            _-b""
          },
          {
            _-a"_-gNPoWeight",
            _-b"${gNPoWeight}"
          },
          {
            _-a"_-gCDisplacementLvl",
            _-b""
          },
          {
            _-a"_-gCTaxItemCde",
            _-b""
          },
          {
            _-a"_-gCFuelType",
            _-b"0"
          }
        ]
      }
    ]
  },
  {
    "isFilter": "false",
    "dwType": "GRID_CVRG",
    "dwName": "prodDef.vhl.Cvrg_DW",
    "rsCount": "1",
    "pageSize": "10",
    "pageNo": "1",
    "pageCount": "0",
    "maxCount": "1000",
    "toAddFlag": "false",
    "filterMapList": [

    ],
	${dataObjVoList}
  },
  {
    "isFilter": "false",
    "dwType": "ONLY_DATA",
    "dwName": "prodDef.vhl.PrmCoef_DW",
    "rsCount": "1",
    "pageSize": "10",
    "pageNo": "1",
    "pageCount": "0",
    "maxCount": "1000",
    "toAddFlag": "false",
    "filterMapList": [

    ],
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            _-a"JQ__-mNDiscountAmount",
            _-b""
          },
          {
            _-a"JQ__-mNCoef",
            _-b""
          },
          {
            _-a"JQ__-mNPriPre",
            _-b""
          },
          {
            _-a"SY__-mCAppNo",
            _-b""
          },
          {
            _-a"SY__-mCPlyNo",
            _-b""
          },
          {
            _-a"JQ__-mCAppNo",
            _-b""
          },
          {
            _-a"JQ__-mCPlyNo",
            _-b""
          },
          {
            _-a"_-mCCrtCde",
            _-b""
          },
          {
            _-a"_-mTCrtTm",
            _-b""
          },
          {
            _-a"_-mCUpdCde",
            _-b""
          },
          {
            _-a"_-mTUpdTm",
            _-b""
          },
          {
            _-a"JQ__-mNClaimTime",
            _-b""
          },
          {
            _-a"SY__-mNClaimTime",
            _-b""
          },
          {
            _-a"JQ__-mNTotalClaimAmount",
            _-b""
          },
          {
            _-a"SY__-mNTotalClaimAmount",
            _-b""
          },
          {
            _-a"_-mNManualProduct",
            _-b""
          },
          {
            _-a"_-mNPreChannelFactor",
            _-b""
          },
          {
            _-a"_-mNPreUnderFactor",
            _-b""
          },
          {
            _-a"_-mNDrinkDriRiseRat",
            _-b"0"
          },
          {
            _-a"_-mNProcesseNum",
            _-b"0"
          },
          {
            _-a"_-mNProcesseNumB",
            _-b"0"
          },
          {
            _-a"_-mNAllDrinkRiseRat",
            _-b"0"
          },
          {
            _-a"_-mNLllegalNum",
            _-b"0"
          },
          {
            _-a"_-mNDrinkDriRiseRatB",
            _-b"0.15"
          },
          {
            _-a"_-mNLllegalNumB",
            _-b"0"
          },
          {
            _-a"_-mNUnProcesseNum",
            _-b""
          },
          {
            _-a"_-mNDrunkDri",
            _-b"0"
          },
          {
            _-a"_-mNUnProcesseNumB",
            _-b""
          },
          {
            _-a"_-mNSpeedNum",
            _-b"0"
          },
          {
            _-a"_-mNBreakRul",
            _-b"0"
          },
          {
            _-a"_-mNOverloadNum",
            _-b"0"
          },
          {
            _-a"_-mNNoGood",
            _-b"0"
          },
          {
            _-a"_-mNOtherNum",
            _-b"0"
          },
          {
            _-a"JQ__-mCNdiscRsn",
            _-b"0"
          },
          {
            _-a"_-mNDeathToll",
            _-b"0"
          },
          {
            _-a"_-mNLyRepRiseRat",
            _-b"1"
          },
          {
            _-a"_-mNOneYearNoDanger",
            _-b""
          },
          {
            _-a"_-mNRecordRiseRat",
            _-b"1"
          },
          {
            _-a"_-mCSafetyViola",
            _-b"00"
          },
          {
            _-a"_-mCAccidentInfo",
            _-b"00"
          },
          {
            _-a"_-mCDangerInfo",
            _-b"00"
          },
          {
            _-a"SY__-mNDiscountAmount",
            _-b""
          },
          {
            _-a"SY__-mNCoef",
            _-b""
          },
          {
            _-a"SY__-mNPriPre",
            _-b""
          },
          {
            _-a"_-mCOfferPlan",
            _-b"A"
          },
          {
            _-a"_-mNNoLossRat",
            _-b""
          },
          {
            _-a"SY__-mNTrafficViolateRat",
            _-b""
          },
          {
            _-a"SY__-mNCarTypeRat",
            _-b""
          },
          {
            _-a"SY__-mNChannelFactor",
            _-b""
          },
          {
            _-a"SY__-mNIndeptUnderRat",
            _-b""
          }
        ]
      }
    ]
  },
  {
    "isFilter": "false",
    "dwType": "ONLY_DATA",
    "dwName": "prodDef.vhl.Vhlowner_DW",
    "rsCount": "1",
    "pageSize": "10",
    "pageNo": "1",
    "pageCount": "0",
    "maxCount": "1000",
    "toAddFlag": "false",
    "filterMapList": [

    ],
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            _-a"_-jCOwnerCde",
            _-b""
          },
          {
            _-a"_-jCCrtCde",
            _-b""
          },
          {
            _-a"_-jTCrtTm",
            _-b""
          },
          {
            _-a"_-jCUpdCde",
            _-b""
          },
          {
            _-a"_-jTUpdTm",
            _-b""
          },
          {
            _-a"_-j_-s1",
            _-b"1"
          },
          {
            _-a"_-jCOwnerNme",
            _-b"${hCAppNme}"
          },
          {
            _-a"_-jCOwnerAge",
            _-b"${jCOwnerAge}"
          },
          {
            _-a"_-jCGender",
            _-b"${jCGender}"
          },
          {
            _-a"_-jCCertfCls",
            _-b""
          },
          {
            _-a"_-jCCertfCde",
            _-b""
          },
          {
            _-a"_-jCCOwnerTyp",
            _-b""
          }
        ]
      }
    ]
  },
  {
    "isFilter": "false",
    "dwType": "ONLY_DATA",
    "dwName": "prodDef.vhl.Applicant_DW",
    "rsCount": "1",
    "pageSize": "10",
    "pageNo": "1",
    "pageCount": "0",
    "maxCount": "1000",
    "toAddFlag": "false",
    "filterMapList": [

    ],
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            _-a"_-hCAppNme",
            _-b"${hCAppNme}"
          }
        ]
      }
    ]
  },
  {
    "isFilter": "false",
    "dwType": "ONLY_DATA",
    "dwName": "prodDef.vhl.Insured_DW",
    "rsCount": "1",
    "pageSize": "10",
    "pageNo": "1",
    "pageCount": "0",
    "maxCount": "1000",
    "toAddFlag": "false",
    "filterMapList": [

    ],
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            _-a"_-iCInsuredNme",
            _-b"${hCAppNme}"
          }
        ]
      }
    ]
  },
  {
    "isFilter": "false",
    "dwType": "ONLY_DATA",
    "dwName": "prodDef.vhl.VsTax_DW",
    "rsCount": "1",
    "pageSize": "10",
    "pageNo": "1",
    "pageCount": "0",
    "maxCount": "1000",
    "toAddFlag": "false",
    "filterMapList": [

    ],
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            _-a"VsTax.NAggTaxVar",
            _-b"0.00"
          },
          {
            _-a"VsTax.NBefEdrTax",
            _-b"0.00"
          },
          {
            _-a"VsTax.NBalanceTax",
            _-b"0.00"
          },
          {
            _-a"VsTax.CTaxUnit",
            _-b"0.00"
          },
          {
            _-a"VsTax.CVehicleNumber",
            _-b""
          },
          {
            _-a"VsTax.CVsTaxMrk",
            _-b"N"
          },
          {
            _-a"VsTax.CPaytaxTyp",
            _-b"T"
          },
          {
            _-a"VsTax.CAbateMrk",
            _-b"002"
          },
          {
            _-a"VsTax.CAbateRsn",
            _-b""
          },
          {
            _-a"VsTax.CFreeType",
            _-b""
          },
          {
            _-a"VsTax.CAbateProp",
            _-b""
          },
          {
            _-a"VsTax.CAbateAmt",
            _-b""
          },
          {
            _-a"VsTax.CTaxReliefCertNo",
            _-b""
          },
          {
            _-a"VsTax.NBeforTax",
            _-b""
          },
          {
            _-a"VsTax.CTaxItemCde",
            _-b"${CTaxItemCde}"
          },
          {
            _-a"VsTax.NAnnUnitTaxAmt",
            _-b"0"
          },
          {
            _-a"VsTax.CTaxYear",
            _-b"2017"
          },
          {
            _-a"VsTax.CLastTaxYear",
            _-b"2016"
          },
          {
            _-a"VsTax.TBillDate",
            _-b""
          },
          {
            _-a"VsTax.CTaxpayerId",
            _-b""
          },
          {
            _-a"VsTax.CTaxpayerCertTyp",
            _-b"01"
          },
          {
            _-a"VsTax.CTaxpayerCertNo",
            _-b""
          },
          {
            _-a"VsTax.CTaxpayerNme",
            _-b""
          },
          {
            _-a"VsTax.TLastSaliEndDate",
            _-b"${fTOprTm}"
          },
          {
            _-a"VsTax.CDrawbackOpr",
            _-b""
          },
          {
            _-a"VsTax.NOverdueDays",
            _-b""
          },
          {
            _-a"VsTax.NOverdueFineProp",
            _-b"0.0005"
          },
          {
            _-a"VsTax.NOverdueAmt",
            _-b""
          },
          {
            _-a"VsTax.NChargeProp",
            _-b"0.05"
          },
          {
            _-a"VsTax.NChargeAmt",
            _-b""
          },
          {
            _-a"VsTax.NLastYearTaxableMonths",
            _-b""
          },
          {
            _-a"VsTax.NLastYear",
            _-b""
          },
          {
            _-a"VsTax.NTaxableMonths",
            _-b""
          },
          {
            _-a"VsTax.NTaxableAmt",
            _-b"0.00"
          },
          {
            _-a"VsTax.TTaxEffBgnTm",
            _-b""
          },
          {
            _-a"VsTax.TTaxEffEndTm",
            _-b""
          },
          {
            _-a"VsTax.NExhaustCapacity",
            _-b"${gNDisplacement}"
          },
          {
            _-a"VsTax.NCurbWt",
            _-b"${NCurbWt}"
          },
          {
            _-a"VsTax.CTaxPaymentRecptNo",
            _-b""
          },
          {
            _-a"VsTax.CDepartmentNonLocal",
            _-b""
          },
          {
            _-a"VsTax.CTaxAuthorities",
            _-b""
          },
          {
            _-a"VsTax.CDrawbackOprMonth",
            _-b""
          },
          {
            _-a"VsTax.NAggTax",
            _-b"0"
          },
          {
            _-a"VsTax.TSaliAppDate",
            _-b""
          },
          {
            _-a"VsTax.CDeclareStatusIA",
            _-b""
          },
          {
            _-a"VsTax.TDeclareDate",
            _-b""
          },
          {
            _-a"VsTax.CCalcTaxFlag",
            _-b""
          }
        ]
      }
    ]
  }
]
  '''



    # from collections import OrderedDict
    # body=json.dumps(body, ensure_ascii=False,object_pairs_hook=OrderedDict)
    # json.loads()
    # print(body)
    dataObjVoList = get_insurance_type(insuranceType, gNDiscussActualValue, fee['gNSeatNum'], gCFrmNo)
    from string import Template
    body = Template(body)
    flag = "1"
    SY_JQ_fCProdNo = "0360_0332"  # 商业险_交强险
    if insuranceType.get("otherHurtPremium", "0") == "1" or insuranceType.get("carNickPremium",
                                                                              "0") == "1" or insuranceType.get(
        "driverDutyPremium", "0") == "1" or insuranceType.get("passengerDutyPremium",
                                                              "0") == "1" or insuranceType.get("carDamagePremium",
                                                                                               "0") == "1":
        flag = "1"
    else:
        flag = "0"
    if insuranceType.get("compulsoryInsurance", "1") == "1" and flag == "1":
        SY_JQ_fCProdNo = "0360_0332"
    elif insuranceType.get("compulsoryInsurance", "1") == "0" and flag == "1":
        SY_JQ_fCProdNo = "0360"  # 0360_0332
    elif insuranceType.get("compulsoryInsurance", "1") == "1" and flag == "0":
        SY_JQ_fCProdNo = "0332"
    body = body.substitute(dataObjVoList=dataObjVoList,
                           gNOfferPurChasePriceMin=gNOfferPurChasePriceMin,
                           gCFamilyCode=gCFamilyCode,
                           SY_fTInsrncBgnTm=SY_fTInsrncBgnTm,
                           gNOfferPurChasePriceMax=gNOfferPurChasePriceMax,
                           gCMonDespRate=gCMonDespRate,
                           JQ__fCTmSysCde=JQ__fCTmSysCde,
                           gNKindredPriceTax=gNKindredPriceTax,
                           gCPlateTyp=gCPlateTyp,
                           SYgCVhlTyp=SYgCVhlTyp,
                           gNPoWeight=gNPoWeight,
                           JQ_fTInsrncEndTm=JQ_fTInsrncEndTm,
                           gCValidateCode=gCValidateCode,
                           gNActualValue=gNActualValue,
                           fCOprCde=fCOprCde,
                           gCModelNme=gCModelNme,
                           gCProdPlace=gCProdPlace,
                           gCPlateNo=gCPlateNo,
                           CTaxItemCde=CTaxItemCde,
                           SY__fCTmSysCde=SY__fCTmSysCde,
                           gNNewPurchaseTaxValue=gNNewPurchaseTaxValue,
                           gNDiscussActualValue=gNDiscussActualValue,
                           gCIndustryModelCode=gCIndustryModelCode,
                           gNSeatNum=gNSeatNum,
                           NCurbWt=NCurbWt,
                           fTOprTm=fTOprTm,
                           NAmt_036007=NAmt_036007,
                           lNVhlActVal=lNVhlActVal,
                           gNKindredPrice=gNKindredPrice,
                           gCBrandId=gCBrandId,
                           gCIndustryModelName=gCIndustryModelName,
                           SY_fTInsrncEndTm=SY_fTInsrncEndTm,
                           gCNoticeType=gCNoticeType,
                           gCFamilyName=gCFamilyName,
                           jCGender=jCGender,
                           gCRegVhlTyp=gCRegVhlTyp,
                           gNTonage=gNTonage,
                           gNDisplacement=gNDisplacement,
                           gCCarAge=gCCarAge,
                           JQ_fTInsrncBgnTm=JQ_fTInsrncBgnTm,
                           hCAppNme=hCAppNme,
                           gCFrmNo=gCFrmNo,
                           gCEngNo=gCEngNo,
                           gCFstRegYm=gCFstRegYm,
                           gCModelCde=gCModelCde,
                           gCSearchCode=gCSearchCode,
                           lNVhlActVal_036005=lNVhlActVal_036005,
                           gNNewPurchaseValue=gNNewPurchaseValue,
                           jCOwnerAge=jCOwnerAge,
                           JQgCVhlTyp=JQgCVhlTyp,
                           SY_JQ_fCProdNo=SY_JQ_fCProdNo)

    body = body.__str__().replace("\n", "")
    return urllib.quote(urllib.quote(body))
