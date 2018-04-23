# -*- coding:utf-8 -*-
__author__ = 'weikai'
from bs4 import BeautifulSoup
import re
#html.parser
#lxml
#soup.html
#soup = BeautifulSoup(open("C:\\Users\\weikai\\Desktop\\5.html"),"lxml")
soup=BeautifulSoup(open("C:\\Users\\weikai\\Desktop\\5.html"),"xml")
#text=soup.html

#soup.findAll('dataObj')[0].findChildren('attribute')[0].getText()

#soup.findAll('dataObj')[0].findAll(attrs={"name":"CPlateNo"})[0].getText()
dataObj=soup.findAll('dataObj')


for i in dataObj:
    CPlateNo=i.findAll(attrs={"name":"CPlateNo"})[0].getText()
    CPlateTyp=i.findAll(attrs={"name":"CPlateTyp"})[0].getText()
    pmUseType=i.findAll(attrs={"name":"pmUseType"})[0].getText()
    CFrmNo=i.findAll(attrs={"name":"CFrmNo"})[0].getText()
    CEngNo=i.findAll(attrs={"name":"CEngNo"})[0].getText()
    color=i.findAll(attrs={"name":"color"})[0].getText()
    COwnerNme=i.findAll(attrs={"name":"COwnerNme"})[0].getText()
    CFstRegYm=i.findAll(attrs={"name":"CFstRegYm"})[0].getText()
    RLimitLoadPerson=i.findAll(attrs={"name":"RLimitLoadPerson"})[0].getText()
    RVehlcleTonnage=i.findAll(attrs={"name":"RVehlcleTonnage"})[0].getText()
    IneffectualDate=i.findAll(attrs={"name":"IneffectualDate"})[0].getText()
    MadeFactory=i.findAll(attrs={"name":"MadeFactory"})[0].getText()
    Model=i.findAll(attrs={"name":"Model"})[0].getText()
    BrandCN=i.findAll(attrs={"name":"BrandCN"})[0].getText()
    BrandEN=i.findAll(attrs={"name":"BrandEN"})[0].getText()
    CVhlTyp=i.findAll(attrs={"name":"CVhlTyp"})[0].getText()
    LastCheckDate=i.findAll(attrs={"name":"LastCheckDate"})[0].getText()
    RejectDate=i.findAll(attrs={"name":"RejectDate"})[0].getText()
    status=i.findAll(attrs={"name":"status"})[0].getText()
    Haulage=i.findAll(attrs={"name":"Haulage"})[0].getText()
    TransferDate=i.findAll(attrs={"name":"TransferDate"})[0].getText()
    NCurbWt=i.findAll(attrs={"name":"NCurbWt"})[0].getText()
    NDisplacement=i.findAll(attrs={"name":"NDisplacement"})[0].getText()
    SalesChannl=i.findAll(attrs={"name":"SalesChannl"})[0].getText()
    VehlclePrice=i.findAll(attrs={"name":"VehlclePrice"})[0].getText()
    EngineType=i.findAll(attrs={"name":"EngineType"})[0].getText()
    RImportFlag=i.findAll(attrs={"name":"RImportFlag"})[0].getText()
    useType=i.findAll(attrs={"name":"useType"})[0].getText()



    print CPlateNo,CPlateTyp















data4='''
{RESULT_TYPE:'SUCESS',CODE_TYPE:'UTF-8',RESULT_MSG:'交管车辆信息查询成功！',JSON_OBJ:null,DATA:['<dataObjs dwid="dwid0.3056373666299691" rsCount="5" pageSize="8" pageNo="1" pageCount="1" dwName="policy.pub.vhl_inf_confirm_DW" difFlag="false"><dataObj index="1" status="UNCHANGED" selected="false"><attribute name="CPlateNo" value="苏BG027F" newValue="苏BG027F" modified="false" type="">苏BG027F</attribute><attribute name="CPlateTyp" value="02" newValue="02" modified="false" type="">小型汽车号牌</attribute><attribute name="pmUseType" value="A" newValue="A" modified="false" type="">非营运</attribute><attribute name="CFrmNo" value="LHGCM567852063612" newValue="LHGCM567852063612" modified="false" type="">LHGCM567852063612</attribute><attribute name="CEngNo" value="K24A4 2563601" newValue="K24A4 2563601" modified="false" type="">K24A4 2563601</attribute><attribute name="color" value="J" newValue="J" modified="false" type="">黑</attribute><attribute name="COwnerNme" value="潘汀" newValue="潘汀" modified="false" type="">潘汀</attribute><attribute name="CFstRegYm" value="2005-11-11" newValue="2005-11-11" modified="false" type="">2005-11-11</attribute><attribute name="RLimitLoadPerson" value="5" newValue="5" modified="false" type="">5</attribute><attribute name="RVehlcleTonnage" value="0.0" newValue="0.0" modified="false" type="">0.0</attribute><attribute name="IneffectualDate" value="20161130" newValue="20161130" modified="false" type="">20161130</attribute><attribute name="MadeFactory" value="广州本田汽车公司" newValue="广州本田汽车公司" modified="false" type="">广州本田汽车公司</attribute><attribute name="Model" value="HG7240" newValue="HG7240" modified="false" type="">HG7240</attribute><attribute name="BrandCN" value="广州雅阁" newValue="广州雅阁" modified="false" type="">广州雅阁</attribute><attribute name="BrandEN" value="" newValue="" modified="false" type=""></attribute><attribute name="CVhlTyp" value="K33" newValue="K33" modified="false" type="">轿车</attribute><attribute name="LastCheckDate" value="20151202" newValue="20151202" modified="false" type="">20151202</attribute><attribute name="RejectDate" value="20991231" newValue="20991231" modified="false" type="">20991231</attribute><attribute name="status" value="Q" newValue="Q" modified="false" type="">逾期未检验</attribute><attribute name="Haulage" value="0" newValue="0" modified="false" type="">0</attribute><attribute name="TransferDate" value="2012-08-22" newValue="2012-08-22" modified="false" type="">2012-08-22</attribute><attribute name="NCurbWt" value="0.0" newValue="0.0" modified="false" type="">0.0</attribute><attribute name="NDisplacement" value="2.354" newValue="2.354" modified="false" type="">2.354</attribute><attribute name="SalesChannl" value="A" newValue="A" modified="false" type="">国产</attribute><attribute name="VehlclePrice" value="0" newValue="0" modified="false" type="">0</attribute><attribute name="EngineType" value="A" newValue="A" modified="false" type="">汽油</attribute><attribute name="RImportFlag" value="11" newValue="11" modified="false" type="">六座以下客车</attribute><attribute name="useType" value="" newValue="" modified="false" type=""></attribute></dataObj><dataObj index="2" status="UNCHANGED" selected="false"><attribute name="CPlateNo" value="苏B6LE80" newValue="苏B6LE80" modified="false" type="">苏B6LE80</attribute><attribute name="CPlateTyp" value="02" newValue="02" modified="false" type="">小型汽车号牌</attribute><attribute name="pmUseType" value="A" newValue="A" modified="false" type="">非营运</attribute><attribute name="CFrmNo" value="LHGCM567852063612" newValue="LHGCM567852063612" modified="false" type="">LHGCM567852063612</attribute><attribute name="CEngNo" value="K24A4 2563601" newValue="K24A4 2563601" modified="false" type="">K24A4 2563601</attribute><attribute name="color" value="J" newValue="J" modified="false" type="">黑</attribute><attribute name="COwnerNme" value="无锡大方寅和工程有限公司" newValue="无锡大方寅和工程有限公司" modified="false" type="">无锡大方寅和工程有限公司</attribute><attribute name="CFstRegYm" value="2005-11-11" newValue="2005-11-11" modified="false" type="">2005-11-11</attribute><attribute name="RLimitLoadPerson" value="5" newValue="5" modified="false" type="">5</attribute><attribute name="RVehlcleTonnage" value="0.0" newValue="0.0" modified="false" type="">0.0</attribute><attribute name="IneffectualDate" value="20171130" newValue="20171130" modified="false" type="">20171130</attribute><attribute name="MadeFactory" value="广州本田汽车公司" newValue="广州本田汽车公司" modified="false" type="">广州本田汽车公司</attribute><attribute name="Model" value="HG7240" newValue="HG7240" modified="false" type="">HG7240</attribute><attribute name="BrandCN" value="广州雅阁" newValue="广州雅阁" modified="false" type="">广州雅阁</attribute><attribute name="BrandEN" value="" newValue="" modified="false" type=""></attribute><attribute name="CVhlTyp" value="K33" newValue="K33" modified="false" type="">轿车</attribute><attribute name="LastCheckDate" value="20161213" newValue="20161213" modified="false" type="">20161213</attribute><attribute name="RejectDate" value="20991231" newValue="20991231" modified="false" type="">20991231</attribute><attribute name="status" value="A" newValue="A" modified="false" type="">正常</attribute><attribute name="Haulage" value="0" newValue="0" modified="false" type="">0</attribute><attribute name="TransferDate" value="2016-12-13" newValue="2016-12-13" modified="false" type="">2016-12-13</attribute><attribute name="NCurbWt" value="0.0" newValue="0.0" modified="false" type="">0.0</attribute><attribute name="NDisplacement" value="2.354" newValue="2.354" modified="false" type="">2.354</attribute><attribute name="SalesChannl" value="A" newValue="A" modified="false" type="">国产</attribute><attribute name="VehlclePrice" value="0" newValue="0" modified="false" type="">0</attribute><attribute name="EngineType" value="A" newValue="A" modified="false" type="">汽油</attribute><attribute name="RImportFlag" value="11" newValue="11" modified="false" type="">六座以下客车</attribute><attribute name="useType" value="" newValue="" modified="false" type=""></attribute></dataObj></dataObjs>'],CUST_DATA:{"ACTION_TIME":"142","REQUEST_TIME":"146"}}
'''
import re


LT=re.findall(r"DATA:\[(.+?)\],",data4,re.S)[0]
LT=LT.strip().lstrip().rstrip("'").strip("'")

print(LT)