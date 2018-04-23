# -*- coding:utf-8 -*-
__author__ = 'weikai'
import urllib
TLastSaliEndDate=fTOprTm=fTAppTm='2017-01-05' ##当前日期
SY_fTInsrncBgnTm='2017-01-06 00:00:00'#保险起止期(商)
SY_fTInsrncEndTm="2018-01-05 23:59:59"#保险起止期(商)
SY__fCTmSysCde="365"  #默认间隔
JQ_fTInsrncBgnTm="2017-01-06 00:00:00" #保险起止期(交)
JQ_fTInsrncEndTm="2018-01-05 23:59:59" #保险起止期(交)
JQ__fCTmSysCde="365"  #默认间隔
#fTOprTm='2017-01-05'#投保时间
fCOprCde="ex_xishijuan001" #用户名
gNNewPurchaseTaxValue="278700" #新车购置价(含税)
gNKindredPrice="198800"#类比价格
gNKindredPriceTax="215800"#类比价(含税)
gNNewPurchaseValue="256800.0" #>新车购置价
gNDiscussActualValue="51873.60" #协商实际价值
gCFrmNo=gCVin="LHGCM567852063612" #车架号
gCMonDespRate="307007001" #月折旧率
gNActualValue="51873.60" #<!-- 车辆实际价值 -->
gNOfferPurChasePriceMax="256800.0" #新车购置价浮动上限
gNOfferPurChasePriceMin=''"231120.0" #新车购置价浮动下
gCIndustryModelCode="BGQEYHUB0015" #行业车型编码
gCIndustryModelName="雅阁HG7240 标准版" #行业车型名称
gCNoticeType="HG7240" #行业公告车型
gCProdPlace="2" #系别名称"0";//国产 "1";//进口 "2";//合资
gCFamilyCode="BTA1AL"#车系编码
gCFamilyName="雅阁" #车系名称
gCFstRegYm="2005-11-11" #初登日期
gCModelNme="雅阁HG7240轿车" #车型名称
gCBrandId="广州雅阁"
gCModelCde="YGD1006GZB" #精友车型代码
gCSearchCode="72CICP320017001483579654826160" #code查询码
gCValidateCode="YUJN" #验证码
gCPlateNo="苏BG027F" #车牌
gCEngNo= "K24A4 2563601" #发动机
gNDisplacement="2.354"  #排气量
gCPlateTyp="02" #号牌种类
gCCarAge="306007" #车龄等级???????????????????????????
gNSeatNum="5"#座位数
gNPoWeight="1.465" #整备质量
#机动车损失保险（主险）#保额-----------------------------------------
lNVhlActVal=lNAmt_036001="51873.60" #机动车损失保险（主险）#保额
lNDeductible_036001="2000" #免赔额
lNDductRate_036001="0.15" #http://carply.cic.cn/pcis/policy/universal/quickapp/vhl_quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0&id=479A78C22656FB9CAFE2C29B6280C930
#玻璃单独破碎险##################################################
lNAmt_036002="036002" #玻璃单独破碎险
lNAmt_036002=lNIndemLmt_036002="500000"
lCIndemLmtLvl_036002="306006009" #50万
lNDductRate__036002="0.15"
####################机动车车上人员责任保险（司机）###############
lNDductRate_036003="0.15"
####################机动车车上人员责任保险（乘客）###############
lNLiabDaysLmt_036004='4' #座位数-1
######################机动车全车盗窃保险（主险）</################
lNVhlActVal_036005=lNAmt_036005="51873.60"
lNDductRate_036005="0.2"
########################机动车交通事故强制责任险@#####################
lNAmt_033201='122000'
########玻璃单独破碎险
_l_s30= "303011001"#国产
#自燃损失险
lNVhlActVal_036007=NAmt_036007="51873.60" #自燃损失险
lNDductRate_036007="0.2"
##########发动机涉水损失险#############
###############车身划痕损失险##############
lNAmt_036013="2000"
lCIndemLmtLvl_306013="N03001001" #// 2000元
lNDductRate_306013="0.15"
###交通违法次数
hCAppNme=iCInsuredNme=jCOwnerNme="潘汀"
jCGender="1061"#男
jCOwnerAge="341060"#年龄阶段
NExhaustCapacity="2.354" #排气量
NCurbWt="1.465"#整备质量(吨)

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

body = [{
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
            "_-fCRenewMrk": ""
          },
          {
            "SY__-fCAppNo": ""
          },
          {
            "JQ__-fCAppNo": ""
          },
          {
            "JQ__-fCOfferNo": ""
          },
          {
            "SY__-fCOfferNo": ""
          },
          {
            "JQ__-fNRiskCost": ""
          },
          {
            "SY__-fNRiskCost": ""
          },
          {
            "JQ__-fNTargetPrm": ""
          },
          {
            "SY__-fNTargetPrm": ""
          },
          {
            "JQ__-fNProfitRatio": ""
          },
          {
            "SY__-fNProfitRatio": ""
          },
          {
            "JQ__-fNPayRatio": ""
          },
          {
            "_-fCPayRatioLevel": ""
          },
          {
            "SY__-fNPayRatio": ""
          },
          {
            "_-fNDoubleRiskCost": ""
          },
          {
            "_-fNDoublePrm": ""
          },
          {
            "_-fNDoublePayRatio": ""
          },
          {
            "_-fCDoublePayRatioLevel": ""
          },
          {
            "JQ__-fNCostRatio": ""
          },
          {
            "SY__-fNCostRatio": ""
          },
          {
            "JQ__-fNCostRate": ""
          },
          {
            "SY__-fNCostRate": ""
          },
          {
            "JQ__-fCCostRatioLevel": ""
          },
          {
            "SY__-fCCostRatioLevel": ""
          },
          {
            "_-fNDoubleCostRate": ""
          },
          {
            "_-fNDoubleCostRatio": ""
          },
          {
            "_-fCDoubleCostRatioLevel": ""
          },
          {
            "_-fCCommonFlag": "0"
          },
          {
            "_-fCAppTyp": "A"
          },
          {
            "SY__-fCPlyNo": ""
          },
          {
            "JQ__-fCPlyNo": ""
          },
          {
            "_-fNEdrPrjNo": ""
          },
          {
            "_-fCRelPlyNo": ""
          },
          {
            "_-fCProdNo": "0360_0332"
          },
          {
            "_-fCDptCde": "32010101"
          },
          {
            "_-fCSlsCde": ""
          },
          {
            "_-fCHandLe": ""
          },
          {
            "_-fCBsnsTyp": "1900101" #直销业务
          },
          {
            "_-fCChaType": ""
          },
          {
            "_-fCBsnsSubtyp": ""
          },
          {
            "_-fCBrkrCde": ""
          },
          {
            "_-fCBrkrName": ""
          },
          {
            "_-fCSaleNme": ""
          },
          {
            "_-fCAgtAgrNo": ""
          },
          {
            "_-fNSubCoNo": ""
          },
          {
            "_-fNCommRate": ""
          },
          {
            "_-fNCommissionRateUpper": ""
          },
          {
            "SY__-fCRenewMrk": ""
          },
          {
            "JQ__-fCRenewMrk": ""
          },
          {
            "JQ__-fCTrunMrk": "0"
          },
          {
            "SY__-fCTrunMrk": "0"
          },
          {
            "_-fCPlyTyp": ""
          },
          {
            "JQ__-fCOrigPlyNo": ""
          },
          {
            "SY__-fCOrigPlyNo": ""
          },
          {
            "_-fCOrigInsurer": ""
          },
          {
            "_-fCAmtCur": ""
          },
          {
            "SY__-fNAmt": "0.00"
          },
          {
            "JQ__-fNAmt": "122000.00" #交强险保额 122000.00
          },
          {
            "_-fNAmtRmbExch": ""
          },
          {
            "_-fCPrmCur": ""
          },
          {
            "SY__-fNCalcPrm": ""
          },
          {
            "JQ__-fNCalcPrm": ""
          },
          {
            "SY__-fNPrm": "0.00"
          },
          {
            "JQ__-fNPrm": "0.00"
          },
          {
            "_-fNPrmRmbExch": "1"
          },
          {
            "_-fNIndemLmt": ""
          },
          {
            "_-fCRatioTyp": "D"
          },
          {
            "SY__-fNRatioCoef": "1"
          },
          {
            "JQ__-fNRatioCoef": "1"
          },
          {
            "_-fNSavingAmt": ""
          },
          {
            "_-fCPlySts": ""
          },
          {
            "_-fTTermnTm": ""
          },
          {
            "_-fCInwdMrk": ""
          },
          {
            "_-fCCiMrk": ""
          },
          {
            "_-fCCiTyp": ""
          },
          {
            "_-fNCiJntAmt": ""
          },
          {
            "_-fNCiJntPrm": ""
          },
          {
            "_-fCLongTermMrk": ""
          },
          {
            "_-fTAppTm": fTAppTm
          },
          {
            "_-fCOprTyp": ""
          },
          {
            "_-fCPrnNo": ""
          },
          {
            "_-fCIcCardId": ""
          },
          {
            "SY__-fTInsrncBgnTm": SY_fTInsrncBgnTm
          },
          {
            "SY__-fTInsrncEndTm": SY_fTInsrncEndTm
          },
          {
            "SY__-fCTmSysCde": SY__fCTmSysCde
          },
          {
            "JQ__-fTInsrncBgnTm": JQ_fTInsrncBgnTm
          },
          {
            "JQ__-fTInsrncEndTm": JQ_fTInsrncEndTm
          },
          {
            "JQ__-fCTmSysCde": JQ__fCTmSysCde
          },
          {
            "SY__-fCUnfixSpc": ""
          },
          {
            "JQ__-fCUnfixSpc": ""
          },
          {
            "_-fCGrpMrk": ""
          },
          {
            "_-fCListorcolMrk": ""
          },
          {
            "_-fCMasterMrk": ""
          },
          {
            "_-fCPkgNo": ""
          },
          {
            "_-fCRegMrk": ""
          },
          {
            "_-fCDecMrk": ""
          },
          {
            "_-fCJuriCde": ""
          },
          {
            "_-fCAgriMrk": "0"
          },
          {
            "_-fCForeignMrk": ""
          },
          {
            "_-fCImporexpMrk": ""
          },
          {
            "JQ__-fCManualMrk": ""
          },
          {
            "SY__-fCManualMrk": ""
          },
          {
            "_-fCManualMrk": ""
          },
          {
            "_-fCInstMrk": ""
          },
          {
            "_-fCVipMrk": ""
          },
          {
            "_-fCOpenCoverNo": ""
          },
          {
            "_-fCDisptSttlCde": "007001"#诉讼
          },
          {
            "_-fCDisptSttlOrg": ""
          },
          {
            "_-fCOprCde": "ex_xishijuan001"
          },
          {
            "_-fTOprTm": fTOprTm
          },
          {
            "_-fCChkCde": ""
          },
          {
            "_-fTIssueTm": ""
          },
          {
            "_-fTUdrTm": ""
          },
          {
            "_-fCUdrDptCde": ""
          },
          {
            "_-fCUdrCde": ""
          },
          {
            "_-fCUdrMrk": ""
          },
          {
            "_-fCRiFacMrk": ""
          },
          {
            "_-fCRiChkCde": ""
          },
          {
            "_-fCRiMrk": ""
          },
          {
            "_-fTNextEdrBgnTm": ""
          },
          {
            "_-fTNextEdrEndTm": ""
          },
          {
            "_-fTNextEdrUdrTm": ""
          },
          {
            "_-fCRemark": ""
          },
          {
            "_-fTEdrAppTm": ""
          },
          {
            "_-fTEdrBgnTm": ""
          },
          {
            "_-fTEdrEndTm": ""
          },
          {
            "_-fCEdrMrk": ""
          },
          {
            "_-fCEdrType": ""
          },
          {
            "_-fCCrtCde": ""
          },
          {
            "_-fTCrtTm": ""
          },
          {
            "_-fCUpdCde": ""
          },
          {
            "SY__-fTUpdTm": ""
          },
          {
            "JQ__-fTUpdTm": ""
          },
          {
            "_-fNRate": ""
          },
          {
            "_-f_-s1": ""
          },
          {
            "_-f_-s2": ""
          },
          {
            "_-f_-s3": ""
          },
          {
            "_-f_-s4": ""
          },
          {
            "_-fCLatestMrk": ""
          },
          {
            "_-fCBidMrk": ""
          },
          {
            "_-fCPrmSts": ""
          },
          {
            "_-fNAmtVar": ""
          },
          {
            "_-fNCalcPrmVar": ""
          },
          {
            "_-fNPrmVar": ""
          },
          {
            "_-fNIndemLmtVar": ""
          },
          {
            "_-fCAppPrsnCde": ""
          },
          {
            "_-fCAppPrsnNme": ""
          },
          {
            "_-fCEdrCtnt": ""
          },
          {
            "_-fCOcPlyNo": ""
          },
          {
            "_-fCRevertMrk": ""
          },
          {
            "_-fCEdrRsnBundleCde": ""
          },
          {
            "_-fNBefEdrPrjNo": ""
          },
          {
            "_-fNBefEdrAmt": ""
          },
          {
            "_-fNBefEdrPrm": ""
          },
          {
            "_-fCEdrNo": ""
          },
          {
            "JQ__-fCEdrNo": ""
          },
          {
            "SY__-fCEdrNo": ""
          },
          {
            "_-fNPrmDisc": ""
          },
          {
            "_-fNDiscRate": ""
          },
          {
            "_-fNMaxFeeProp": ""
          },
          {
            "_-fCFinTyp": "001"#缴费方式
          },
          {
            "_-fCGrantDptCde": ""
          },
          {
            "_-fCVipCus": ""
          },
          {
            "_-fNOrigTimes": ""
          },
          {
            "_-fCDptAttr": ""
          },
          {
            "_-fCSalegrpCde": ""
          },
          {
            "_-fCSlsId": ""
          },
          {
            "_-fCSlsTel": ""
          },
          {
            "_-fCSlsNme": ""
          },
          {
            "_-fCMinUndrDpt": ""
          },
          {
            "_-fCMinUndrCls": ""
          },
          {
            "_-fCPkgMrk": ""
          },
          {
            "_-fCAppStatus": ""
          },
          {
            "JQ__-fCImmeffMrk": ""
          },
          {
            "SY__-fCImmeffMrk": ""
          },
          {
            "_-fCInsrncTm": ""
          },
          {
            "_-fNBasePrm": ""
          },
          {
            "_-fNAllPrm": ""
          },
          {
            "_-fCSusBusiness": ""
          },
          {
            "JQ__-fCNewFlg": "1"
          },
          {
            "SY__-fCNewFlg": "1"
          },
          {
            "_-fTInsrncTm": ""
          },
          {
            "_-fCOprNm": ""
          },
          {
            "_-fCSaleTeam": ""
          },
          {
            "_-fCAgantPer": ""
          },
          {
            "_-fCVisInsure": ""
          },
          {
            "_-fCIsTender": ""
          },
          {
            "_-fCTenderNo": ""
          },
          {
            "_-fTRepstopExtLastEndTm": ""
          },
          {
            "_-fCRepstopextStatus": ""
          },
          {
            "_-fTRepStopExtBgnTm": ""
          },
          {
            "_-fTRepStopExtEndTm": ""
          },
          {
            "_-fCRepStopExtRleAppNo": ""
          },
          {
            "_-fTUntilDate": ""
          },
          {
            "_-fCMkupFlag": ""
          },
          {
            "_-fCGrpBaseMrk": ""
          },
          {
            "_-fCComputerIp": ""
          },
          {
            "_-fCUsbKey": ""
          },
          {
            "_-fCPosNo": ""
          },
          {
            "_-fCChaNmeCode": "B"#渠道
          },
          {
            "_-fCNewChaType": "B01"#渠道
          },
          {
            "_-fCNewBsnsTyp": "B0105"#渠道
          },
          {
            "_-fCServiceCode": ""
          },
          {
            "_-fCTeamCode": ""
          },
          {
            "_-fCTeamName": ""
          },
          {
            "_-fCServiceId": ""
          },
          {
            "_-fCPubNetFlag": ""
          },
          {
            "_-fCDeptName": ""
          },
          {
            "_-fCAppointAreaCode": ""
          },
          {
            "_-fCIsFullEndor": ""
          },
          {
            "_-fNAdditionalCostRate": ""
          },
          {
            "_-fCOfferPlan": "A"#价格方案
          },
          {
            "_-fCClauseType": "01"#条款体系
          },
          {
            "_-fCPrmCalcProTyp": ""
          },
          {
            "_-fCPriskPremFlag": ""
          },
          {
            "_-fNCarLossPrm": ""
          },
          {
            "JQ__-fCOfferUseSpc": ""
          },
          {
            "SY__-fCOfferUseSpc": ""
          },
          {
            "_-fCOperDpt": ""
          },
          {
            "_-fCPayAgreement": ""
          },
          {
            "_-fNIncrementRate": ""
          },
          {
            "JQ__-fNNoTaxPrm": ""
          },
          {
            "SY__-fNNoTaxPrm": ""
          },
          {
            "JQ__-fNAddedTax": ""
          },
          {
            "SY__-fNAddedTax": ""
          },
          {
            "_-fCDataSrc": ""
          },
          {
            "_-fCFiMrk": ""
          },
          {
            "_-fNJsPrm": ""
          },
          {
            "_-fNJsAmt": ""
          },
          {
            "_-fNJcPrm": ""
          },
          {
            "_-fNJcAmt": ""
          },
          {
            "_-fCPropertyMrk": ""
          },
          {
            "_-fNPropertyPrm": ""
          },
          {
            "_-fNPropertyAmt": ""
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
            "_-gNNewPurchaseTaxValue": gNNewPurchaseTaxValue
          },
          {
            "_-gNKindredPrice": gNKindredPrice
          },
          {
            "_-gNKindredPriceTax": gNKindredPriceTax
          },
          {
            "_-gCVin": gCVin
          },
          {
            "_-gCMonDespRate": gCMonDespRate
          },
          {
            "_-gNActualValue": gNActualValue
          },
          {
            "_-gCLoanVehicleFlag": "0"#车贷投保多年
          },
          {
            "JQ__-gCQryCde": ""
          },
          {
            "SY__-gCQryCde": ""
          },
          {
            "_-gCVehlcleFamily": ""
          },
          {
            "_-gCModelDesc": ""
          },
          {
            "_-gRMarketDate": ""
          },
          {
            "_-gNAssignPrice": ""
          },
          {
            "_-gNOfferPurChasePrice": ""
          },
          {
            "_-gNOfferPurChasePriceMax": gNOfferPurChasePriceMax
          },
          {
            "_-gNOfferPurChasePriceMin": gNOfferPurChasePriceMin
          },
          {
            "_-gCSnModifyPrices": "0"
          },
          {
            "_-gCXnModifyPrices": "0"
          },
          {
            "_-gCFleetMrk": "0"
          },
          {
            "_-gCVhlPkgNO": ""
          },
          {
            "_-gCIndustryModelCode": gCIndustryModelCode
          },
          {
            "_-gCIndustryModelName":gCIndustryModelName
          },
          {
            "_-gCNoticeType": "HG7240"
          },
          {
            "_-gCProdPlace": "2"
          },
          {
            "_-gCHfcode": "0"
          },
          {
            "_-gCDragWeight": ""
          },
          {
            "_-gCFamilyCode": "BTA1AL"
          },
          {
            "_-gCFamilyName": gCFamilyName
          },
          {
            "_-gCEcdemicMrk": "0"
          },
          {
            "_-gCDevice1Mrk": "0"
          },
          {
            "_-gCNewVhlFlag": "1"
          },
          {
            "_-gCNewMrk": "0"
          },
          {
            "_-gCFstRegYm": "2005-11-11"
          },
          {
            "_-gCFrmNo": "LHGCM567852063612"
          },
          {
            "_-gCModelNme": gCModelNme
          },
          {
            "CarModel": ""
          },
          {
            "searcheVehicleModel": ""
          },
          {
            "queryPlateCarInfo": ""
          },
          {
            "_-gCBrandId": gCBrandId
          },
          {
            "_-gCModelCde": "YGD1006GZB"
          },
          {
            "_-gCModelCde2": ""
          },
          {
            "CarSerachValidate": ""
          },
          {
            "CarSerachConfirm": ""
          },
          {
            "_-gCSearchCode": "72CICP320017001483579654826160"
          },
          {
            "_-gCValidateCode": "YUJN"
          },
          {
            "_-gCPlateNo": gCPlateNo
          },
          {
            "_-gCEngNo": "K24A4 2563601"
          },
          {
            "_-gNDisplacement": "2.354"
          },
          {
            "_-gCPlateTyp": "02"
          },
          {
            "_-gNNewPurchaseValue": "256800.0"
          },
          {
            "_-gNDiscussActualValue": "51873.60"
          },
          {
            "JQ__-gCUsageCde": "309001"
          },
          {
            "JQ__-gCVhlTyp": "302001001"
          },
          {
            "_-gCCarAge": "306007"
          },
          {
            "SY__-gCUsageCde": "309001"
          },
          {
            "SY__-gCVhlTyp": "302001001"
          },
          {
            "SY__-g_-s6": "11"
          },
          {
            "_-gCRegVhlTyp": "K33"
          },
          {
            "_-gCCardDetail": "K33"
          },
          {
            "_-gCNatOfBusines": "359002"
          },
          {
            "_-gNTonage": "0"
          },
          {
            "_-gNSeatNum": "5"
          },
          {
            "_-gTTransferDate": ""
          },
          {
            "_-gCBillDate": ""
          },
          {
            "_-gNPoWeight": "1.465"
          },
          {
            "_-gCDisplacementLvl": ""
          },
          {
            "_-gCTaxItemCde": ""
          },
          {
            "_-gCFuelType": "0"
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
    "dataObjVoList": [
      {
        "index": "1",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "1"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036001"
          },
          {
            "_-lNAmt": "51873.60"
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "0"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": "2000"
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": "0.15"
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": "51873.60"
          }
        ]
      },
      {
        "index": "2",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "2"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036002"
          },
          {
            "_-lNAmt": "500000"
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": "500000"
          },
          {
            "_-lNRate": ""
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": "306006009"
          },
          {
            "_-lNDductRate": "0.15"
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": ""
          }
        ]
      },
      {
        "index": "3",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "3"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036003"
          },
          {
            "_-lNAmt": "0"
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": "10000"
          },
          {
            "_-lNLiabDaysLmt": "1"
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "0"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": "0.15"
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": ""
          }
        ]
      },
      {
        "index": "4",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "4"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036004"
          },
          {
            "_-lNAmt": "0"
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": "10000"
          },
          {
            "_-lNLiabDaysLmt": "4"
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "0"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": "0.15"
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": ""
          }
        ]
      },
      {
        "index": "5",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "5"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036005"
          },
          {
            "_-lNAmt": "51873.60"
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "0"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": "0.2"
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": "51873.60"
          }
        ]
      },
      {
        "index": "21",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "21"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "033201"
          },
          {
            "_-lNAmt": "122000"
          },
          {
            "_-lCDductMrk": ""
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "0"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": ""
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": ""
          }
        ]
      },
      {
        "index": "6",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "6"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036006"
          },
          {
            "_-lNAmt": ""
          },
          {
            "_-lCDductMrk": ""
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "0"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": "303011001" ##国产
          },
          {
            "_-l_-s29": "0"
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": ""
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": ""
          }
        ]
      },
      {
        "index": "7",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "7"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036007"
          },
          {
            "_-lNAmt": NAmt_036007
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "2"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": lNDductRate_036007
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": lNVhlActVal_036007
          }
        ]
      },
      {
        "index": "12",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "12"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036012"
          },
          {
            "_-lNAmt": ""
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": ""
          },
          {
            "_-lNRate": "2"
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": ""
          },
          {
            "_-lNDductRate": lNDductRate_036007
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": ""
          }
        ]
      },
      {
        "index": "13",
        "selected": "true",
        "status": "INSERTED",
        "attributeVoList": [
          {
            "_-lCCancelMrk": "0"
          },
          {
            "_-lNSeqNo": "13"
          },
          {
            "_-lCPkId": ""
          },
          {
            "_-lCCvrgNo": "036013"
          },
          {
            "_-lNAmt": "2000"
          },
          {
            "_-lCDductMrk": "369003"
          },
          {
            "_-lNBasePrm": ""
          },
          {
            "_-lNPrm": ""
          },
          {
            "_-lNPerAmt": ""
          },
          {
            "_-lNLiabDaysLmt": ""
          },
          {
            "_-lNIndemLmt": "2000"
          },
          {
            "_-lNRate": ""
          },
          {
            "_-lCRowId": ""
          },
          {
            "_-lCCrtCde": ""
          },
          {
            "_-lTCrtTm": ""
          },
          {
            "_-lNDeductible": ""
          },
          {
            "_-lCUpdCde": ""
          },
          {
            "_-lTUpdTm": ""
          },
          {
            "_-lTBgnTm": ""
          },
          {
            "_-lTEndTm": ""
          },
          {
            "_-lNDisCoef": ""
          },
          {
            "_-l_-s30": ""
          },
          {
            "_-l_-s29": ""
          },
          {
            "_-l_-s12": ""
          },
          {
            "_-l_-s1": ""
          },
          {
            "_-lCIndemLmtLvl": "N03001001"
          },
          {
            "_-lNDductRate":lNDductRate_306013
          },
          {
            "_-l_-u1": ""
          },
          {
            "_-lNPerPrm": ""
          },
          {
            "_-lNDductPrm": ""
          },
          {
            "_-lNBefPrm": ""
          },
          {
            "_-lNVhlActVal": ""
          }
        ]
      }
    ]
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
            "JQ__-mNDiscountAmount": ""
          },
          {
            "JQ__-mNCoef": ""
          },
          {
            "JQ__-mNPriPre": ""
          },
          {
            "SY__-mCAppNo": ""
          },
          {
            "SY__-mCPlyNo": ""
          },
          {
            "JQ__-mCAppNo": ""
          },
          {
            "JQ__-mCPlyNo": ""
          },
          {
            "_-mCCrtCde": ""
          },
          {
            "_-mTCrtTm": ""
          },
          {
            "_-mCUpdCde": ""
          },
          {
            "_-mTUpdTm": ""
          },
          {
            "JQ__-mNClaimTime": ""
          },
          {
            "SY__-mNClaimTime": ""
          },
          {
            "JQ__-mNTotalClaimAmount": ""
          },
          {
            "SY__-mNTotalClaimAmount": ""
          },
          {
            "_-mNManualProduct": ""
          },
          {
            "_-mNPreChannelFactor": ""
          },
          {
            "_-mNPreUnderFactor": ""
          },
          {
            "_-mNDrinkDriRiseRat": "0"
          },
          {
            "_-mNProcesseNum": "0"
          },
          {
            "_-mNProcesseNumB": "0"
          },
          {
            "_-mNAllDrinkRiseRat": "0"
          },
          {
            "_-mNLllegalNum": "0"
          },
          {
            "_-mNDrinkDriRiseRatB": "0.15"
          },
          {
            "_-mNLllegalNumB": "0"
          },
          {
            "_-mNUnProcesseNum": ""
          },
          {
            "_-mNDrunkDri": "0"
          },
          {
            "_-mNUnProcesseNumB": ""
          },
          {
            "_-mNSpeedNum": "0"
          },
          {
            "_-mNBreakRul": "0"
          },
          {
            "_-mNOverloadNum": "0"
          },
          {
            "_-mNNoGood": "0"
          },
          {
            "_-mNOtherNum": "0"
          },
          {
            "JQ__-mCNdiscRsn": "0"
          },
          {
            "_-mNDeathToll": "0"
          },
          {
            "_-mNLyRepRiseRat": "1"
          },
          {
            "_-mNOneYearNoDanger": ""
          },
          {
            "_-mNRecordRiseRat": "1"
          },
          {
            "_-mCSafetyViola": "00"
          },
          {
            "_-mCAccidentInfo": "00"
          },
          {
            "_-mCDangerInfo": "00"
          },
          {
            "SY__-mNDiscountAmount": ""
          },
          {
            "SY__-mNCoef": ""
          },
          {
            "SY__-mNPriPre": ""
          },
          {
            "_-mCOfferPlan": "A"
          },
          {
            "_-mNNoLossRat": ""
          },
          {
            "SY__-mNTrafficViolateRat": ""
          },
          {
            "SY__-mNCarTypeRat": ""
          },
          {
            "SY__-mNChannelFactor": ""
          },
          {
            "SY__-mNIndeptUnderRat": ""
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
            "_-jCOwnerCde": ""
          },
          {
            "_-jCCrtCde": ""
          },
          {
            "_-jTCrtTm": ""
          },
          {
            "_-jCUpdCde": ""
          },
          {
            "_-jTUpdTm": ""
          },
          {
            "_-j_-s1": "1"
          },
          {
            "_-jCOwnerNme": jCOwnerNme
          },
          {
            "_-jCOwnerAge": jCOwnerAge
          },
          {
            "_-jCGender": jCGender
          },
          {
            "_-jCCertfCls": ""
          },
          {
            "_-jCCertfCde": ""
          },
          {
            "_-jCCOwnerTyp": ""
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
            "_-hCAppNme": hCAppNme
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
            "_-iCInsuredNme": iCInsuredNme
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
            "VsTax.NAggTaxVar": "0.00"
          },
          {
            "VsTax.NBefEdrTax": "0.00"
          },
          {
            "VsTax.NBalanceTax": "0.00"
          },
          {
            "VsTax.CTaxUnit": "0.00"
          },
          {
            "VsTax.CVehicleNumber": ""
          },
          {
            "VsTax.CVsTaxMrk": "N"
          },
          {
            "VsTax.CPaytaxTyp": "T"
          },
          {
            "VsTax.CAbateMrk": "002"
          },
          {
            "VsTax.CAbateRsn": ""
          },
          {
            "VsTax.CFreeType": ""
          },
          {
            "VsTax.CAbateProp": ""
          },
          {
            "VsTax.CAbateAmt": ""
          },
          {
            "VsTax.CTaxReliefCertNo": ""
          },
          {
            "VsTax.NBeforTax": ""
          },
          {
            "VsTax.CTaxItemCde": "398016"
          },
          {
            "VsTax.NAnnUnitTaxAmt": "0"
          },
          {
            "VsTax.CTaxYear": "2017"
          },
          {
            "VsTax.CLastTaxYear": "2016"
          },
          {
            "VsTax.TBillDate": ""
          },
          {
            "VsTax.CTaxpayerId": ""
          },
          {
            "VsTax.CTaxpayerCertTyp": "01"
          },
          {
            "VsTax.CTaxpayerCertNo": ""
          },
          {
            "VsTax.CTaxpayerNme": ""
          },
          {
            "VsTax.TLastSaliEndDate": TLastSaliEndDate
          },
          {
            "VsTax.CDrawbackOpr": ""
          },
          {
            "VsTax.NOverdueDays": ""
          },
          {
            "VsTax.NOverdueFineProp": "0.0005"
          },
          {
            "VsTax.NOverdueAmt": ""
          },
          {
            "VsTax.NChargeProp": "0.05"
          },
          {
            "VsTax.NChargeAmt": ""
          },
          {
            "VsTax.NLastYearTaxableMonths": ""
          },
          {
            "VsTax.NLastYear": ""
          },
          {
            "VsTax.NTaxableMonths": ""
          },
          {
            "VsTax.NTaxableAmt": "0.00"
          },
          {
            "VsTax.TTaxEffBgnTm": ""
          },
          {
            "VsTax.TTaxEffEndTm": ""
          },
          {
            "VsTax.NExhaustCapacity": NExhaustCapacity
          },
          {
            "VsTax.NCurbWt": NCurbWt
          },
          {
            "VsTax.CTaxPaymentRecptNo": ""
          },
          {
            "VsTax.CDepartmentNonLocal": ""
          },
          {
            "VsTax.CTaxAuthorities": ""
          },
          {
            "VsTax.CDrawbackOprMonth": ""
          },
          {
            "VsTax.NAggTax": "0"
          },
          {
            "VsTax.TSaliAppDate": ""
          },
          {
            "VsTax.CDeclareStatusIA": ""
          },
          {
            "VsTax.TDeclareDate": ""
          },
          {
            "VsTax.CCalcTaxFlag": ""
          }
        ]
      }
    ]
  }]
#import  json

#print  json.dumps(body,ensure_ascii=False,indent=4)
# print(body[1]['dataObjVoList'][0]['attributeVoList'])
#print urllib.quote(str(body).decode('gbk').encode('utf-8'))


