# -*- coding:utf-8 -*-
__author__ = 'weikai'
import urllib
import  json
from request_cic import utils

def getFeebody(fee):
  fee={"TLastSaliEndDate":"","SY_fTInsrncBgnTm":"","SY_fTInsrncEndTm":""
       }

  fee['TLastSaliEndDate']=TLastSaliEndDate=fTOprTm=fTAppTm=utils.getlatedate(0) ##当前日期
  fee['SY_fTInsrncBgnTm']=SY_fTInsrncBgnTm=utils.getlatedate(1)+' 00:00:00'#保险起止期(商)
  fee['SY_fTInsrncEndTm']=SY_fTInsrncEndTm=utils.getlatedate(365)+" 23:59:59"#保险起止期(商)
  fee['SY__fCTmSysCde']=SY__fCTmSysCde="365"  #默认间隔
  fee['JQ_fTInsrncBgnTm']=JQ_fTInsrncBgnTm=utils.getlatedate(1)+" 00:00:00" #保险起止期(交)
  fee['JQ_fTInsrncEndTm']=JQ_fTInsrncEndTm=utils.getlatedate(365)+" 23:59:59" #保险起止期(交)
  fee['JQ__fCTmSysCde']=JQ__fCTmSysCde="365"  #默认间隔
  #fTOprTm='2017-01-05'#投保时间
  fCOprCde="ex_xishijuan001" #用户名
  fee['gNNewPurchaseTaxValue']=gNNewPurchaseTaxValue="96766" #新车购置价(含税)
  fee['gNKindredPrice']=gNKindredPrice="0"#类比价格
  fee['gNKindredPriceTax']=gNKindredPriceTax="0"#类比价(含税)
  fee['gNNewPurchaseValue']=gNNewPurchaseValue="92800.0" #>新车购置价
  fee['gNDiscussActualValue']=gNDiscussActualValue="79993.60" #协商实际价值
  fee['gCFrmNo']=gCFrmNo=gCVin="LMVHEKFD6EA029484" #车架号
  fee['gCMonDespRate']=gCMonDespRate="307007001" #月折旧率
  fee['gNActualValue']=gNActualValue="79993.60" #<!-- 车辆实际价值 -->
  fee['gNOfferPurChasePriceMax']=gNOfferPurChasePriceMax="92800.0" #新车购置价浮动上限
  fee['gNOfferPurChasePriceMin']=gNOfferPurChasePriceMin="83520.0" #新车购置价浮动下
  fee['gCIndustryModelCode']=gCIndustryModelCode="BHMESXUB0001" #行业车型编码
  fee['gCIndustryModelName']=gCIndustryModelName="海马HMA7161GA4W 智乐型" #行业车型名称
  fee['gCNoticeType']=gCNoticeType="HMA7161GA4W" #行业公告车型
  fee['gCProdPlace']=gCProdPlace="0" #系别名称"0";//国产 "1";//进口 "2";//合资
  fee['gCFamilyCode']=gCFamilyCode="HMB0AL"#车系编码
  fee['gCFamilyName']=gCFamilyName="海马S5" #车系名称
  fee['gCFstRegYm']=gCFstRegYm="2015-01-27" #初登日期
  fee['gCModelNme']=gCModelNme="海马HMA7161GA4W轿车" #车型名称
  fee['gCBrandId']=gCBrandId="海马牌"
  fee['gCModelCde']=gCModelCde="HMD1061YQH" #精友车型代码
  fee['gCSearchCode']=gCSearchCode="72CICP320017001483843985550846" #code查询码
  fee['gCValidateCode']=gCValidateCode="6FWJ" #验证码
  fee['gCPlateNo']=gCPlateNo="苏AB1S17" #车牌
  fee['gCEngNo']=gCEngNo= "4B029952" #发动机
  fee['gNDisplacement']=gNDisplacement=NExhaustCapacity="1.591"  #排气量
  fee['gCPlateTyp']=gCPlateTyp="02" #号牌种类
  fee['gCCarAge']=gCCarAge="306002" #车龄等级???????????????????????????
  fee['gNSeatNum']=gNSeatNum="5"#座位数
  fee['gNPoWeight']=gNPoWeight="1.35" #整备质量
  #机动车损失保险（主险）#保额-----------------------------------------
  fee['lNVhlActVal']=lNVhlActVal=lNAmt_036001="79993.60" #机动车损失保险（主险）#保额
  fee['lNDeductible_036001']=lNDeductible_036001="2000" #免赔额
  fee['lNDductRate_036001']=lNDductRate_036001="0.15" #http://carply.cic.cn/pcis/policy/universal/quickapp/vhl_quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0&id=479A78C22656FB9CAFE2C29B6280C930
  #玻璃单独破碎险##################################################
  fee['lNAmt_036002']=lNAmt_036002="036002" #玻璃单独破碎险
  fee['lNAmt_036002']=lNAmt_036002=lNIndemLmt_036002="500000"
  fee['lCIndemLmtLvl_036002']=lCIndemLmtLvl_036002="306006009" #50万
  fee['lNDductRate__036002']=lNDductRate__036002="0.15"
  ####################机动车车上人员责任保险（司机）###############
  fee['lNDductRate_036003']=lNDductRate_036003="0.15"
  ####################机动车车上人员责任保险（乘客）###############
  fee['lNLiabDaysLmt_036004']=lNLiabDaysLmt_036004='4' #座位数-1
  ######################机动车全车盗窃保险（主险）</################
  fee['lNVhlActVal_036005']=lNVhlActVal_036005=lNAmt_036005="79993.60"
  fee['lNDductRate_036005']=lNDductRate_036005="0.2"
  ########################机动车交通事故强制责任险@#####################
  fee['lNAmt_033201']=lNAmt_033201='122000'
  ########玻璃单独破碎险
  fee['_l_s30']=_l_s30= "303011001"#国产
  #自燃损失险
  fee['lNVhlActVal_036007']=lNVhlActVal_036007=NAmt_036007="79993.60" #自燃损失险
  fee['lNDductRate_036007']=lNDductRate_036007="0.2"
  ##########发动机涉水损失险#############
  ###############车身划痕损失险##############
  fee['lNAmt_036013']=lNAmt_036013="2000"
  fee['lCIndemLmtLvl_306013']=lCIndemLmtLvl_306013="N03001001" #// 2000元
  lNDductRate_306013="0.15"
  ###交通违法次数
  fee['hCAppNme']=hCAppNme=iCInsuredNme=jCOwnerNme="陆军"
  fee['jCGender']=jCGender="1061"#男
  fee['jCOwnerAge']=jCOwnerAge="341060"#年龄阶段
  #fee['NExhaustCapacity']=NExhaustCapacity="2.354" #排气量

  fee['NCurbWt']=NCurbWt="1.35"#整备质量(吨)
  CTaxItemCde='398014'
  fee['gCRegVhlTyp']=gCRegVhlTyp=gCCardDetail='K33'
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
  #http://carply.cic.cn/pcis/core/js/compress/vhl_offer_app.js?version=704557
  #9900行 判断税目
  if int(gNSeatNum)<=9 and int(float(gNDisplacement)*1000)<= 1000:
      CTaxItemCde="398013" #["398013", "乘用车9人（含）以下排量1.0升（含）以下的"]
  elif int(gNSeatNum)<=9 and int(float(gNDisplacement)*1000)>1000 and int(float(gNDisplacement)*1000)<= 1600:
      CTaxItemCde="398014" #["398014", "乘用车9人（含）以下排量1.0升以上至1.6升（含）的"]);
  elif int(gNSeatNum)<=9 and int(float(gNDisplacement)*1000)>1600 and int(float(gNDisplacement)*1000)<= 2000:
      CTaxItemCde="398015"                   #["398015", "乘用车9人（含）以下排量1.6升以上至2.0升（含）的"]);
  elif int(gNSeatNum)<=9 and int(float(gNDisplacement)*1000)>2000 and int(float(gNDisplacement)*1000)<= 2500:
      CTaxItemCde="398016"         #["398016", "乘用车9人（含）以下排量2.0升以上至2.5升（含）的"]);
  elif int(gNSeatNum)<=9 and int(float(gNDisplacement)*1000)>2500 and int(float(gNDisplacement)*1000)<= 3000:
      CTaxItemCde="398017"         #["398017", "乘用车9人（含）以下排量2.5升以上至3.0升（含）的"]);
  elif int(gNSeatNum)<=9 and int(float(gNDisplacement)*1000)>3000 and int(float(gNDisplacement)*1000)<= 4000:
      CTaxItemCde="398018"         #["398017", "乘用车9人（含）以下排量2.5升以上至3.0升（含）的"]);
  elif int(gNSeatNum)<=9 and int(float(gNDisplacement)*1000)>4000:
      CTaxItemCde="398019"         #["398017", "乘用车9人（含）以下排量2.5升以上至3.0升（含）的"]);
  elif int(gNSeatNum)> 9 and int(gNSeatNum)<20:
      CTaxItemCde="398020"         #["398020", "商用车9人以上20人以下的中型客车及电车"]);
  elif int(gNSeatNum)>=20:
      CTaxItemCde="398021"         #["398021", "商用车20人以上(含)的大型客车及电车"]);

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
              "_-gCNoticeType": gCNoticeType
            },
            {
              "_-gCProdPlace": gCProdPlace
            },
            {
              "_-gCHfcode": "0"
            },
            {
              "_-gCDragWeight": ""
            },
            {
              "_-gCFamilyCode": gCFamilyCode
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
              "_-gCFstRegYm": gCFstRegYm
            },
            {
              "_-gCFrmNo": gCFrmNo
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
              "_-gCModelCde": gCModelCde
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
              "_-gCSearchCode": gCSearchCode
            },
            {
              "_-gCValidateCode": gCValidateCode
            },
            {
              "_-gCPlateNo": gCPlateNo
            },
            {
              "_-gCEngNo": gCEngNo
            },
            {
              "_-gNDisplacement": gNDisplacement
            },
            {
              "_-gCPlateTyp": gCPlateTyp
            },
            {
              "_-gNNewPurchaseValue": gNNewPurchaseValue
            },
            {
              "_-gNDiscussActualValue": gNDiscussActualValue
            },
            {
              "JQ__-gCUsageCde": "309001"
            },
            {
              "JQ__-gCVhlTyp": "302001001"
            },
            {
              "_-gCCarAge": gCCarAge
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
              "_-gCRegVhlTyp": gCRegVhlTyp
            },
            {
              "_-gCCardDetail": gCRegVhlTyp
            },
            {
              "_-gCNatOfBusines": "359002"
            },
            {
              "_-gNTonage": "0"
            },
            {
              "_-gNSeatNum": gNSeatNum
            },
            {
              "_-gTTransferDate": ""
            },
            {
              "_-gCBillDate": ""
            },
            {
              "_-gNPoWeight": gNPoWeight
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
              "_-lNAmt": lNVhlActVal
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
              "_-lNVhlActVal": lNVhlActVal
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
              "_-lNAmt": "10000"
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
              "_-lNAmt": str(int(lNLiabDaysLmt_036004)*10000)
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
              "_-lNAmt": lNVhlActVal_036005
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
              "_-lNVhlActVal": lNVhlActVal_036005
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
              "VsTax.CTaxItemCde": CTaxItemCde #根据排量计算
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

  body=json.dumps(body,ensure_ascii=False,separators=(',',':'))
  #from collections import OrderedDict
  #body=json.dumps(body, ensure_ascii=False,object_pairs_hook=OrderedDict)
  #json.loads()
  #print(body)
  return urllib.quote(urllib.quote(body))

#getFeebody()