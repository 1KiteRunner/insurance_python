# coding:utf8
import urllib

import time

import settings as se
from urllib import quote


# 获取CPlyNo, 判断有没有续保信息
def get_xubao_1(session, plateNumber):
    url_xubao_1 = "http://ply.e-acic.com/pcis/policyAppBizAction_getLastPolicyForUnion/actionservice.ai"

    CUST_DATA = "COrigPlyNo=###CPlateNo={CPlateNo}###CFrmNo=###CEngNo=###CProdNo=0336###CUnionMrk=1".format(
        CPlateNo=plateNumber)

    CUST_DATA = urllib.quote(urllib.quote(CUST_DATA))

    data = "SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=getLastPolicyForUnion&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA={CUST_DATA}".format(
        DW_DATA=se.DW_DATA_RENEWAL, CUST_DATA=CUST_DATA)

    ret = session.post(url_xubao_1, data=data)

    return ret


# 获取续保信息
def get_xubao_2(session, syPlyNo, jqPlyNo):
    url_xubao_2 = "http://ply.e-acic.com/pcis/policy/universal/quickapp/actionservice.ai"

    CUST_DATA = "scene=PLY_APP_STRICT_RENEW_SCENE###prodNo=0336_0330###dptCde=32011001###syAppNo=null###jqAppNo=null###syPlyNo={syPlyNo}###jqPlyNo={jqPlyNo}###taskId=null###updTm=null###appFromTmpl=null###appNo=null###relAppNo=null###edrType=null###edrRsnOrBundle=null###syEdrNo=###jqEdrNo=###applicant=sy###insured=sy###vhlowner=sy###isGroupPolicy=null###seqNo=null###groupNo=null".format(
        syPlyNo=syPlyNo, jqPlyNo=jqPlyNo)

    CUST_DATA = urllib.quote(urllib.quote(CUST_DATA))

    data = "ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=quickAppDataLoadBizAction&SERVICE_MOTHOD=initQuick&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA={CUST_DATA}".format(
        DW_DATA=se.DW_DATA, CUST_DATA=CUST_DATA)

    ret = session.post(url_xubao_2, data=data)

    return ret


# 车辆查询
def query_car(session, plat, frame):
    url_query_car = "http://ply.e-acic.com/pcis/policyAppBizAction_getVinVhlInfo/actionservice.ai"

    CUST_DATA = "{0}###{1}".format(plat, frame)
    CUST_DATA = urllib.quote(urllib.quote(CUST_DATA))

    data = "SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=getVinVhlInfo&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA={CUST_DATA}".format(
        DW_DATA=se.DW_DATA_CAR, CUST_DATA=CUST_DATA)

    ret = session.post(url_query_car, data=data, headers=se.HEADERS)

    return ret


def query_car_model(session, VEHICLE_MODEL):
    url_query_car_model = 'http://ply.e-acic.com/pcis/vehicleAction_queryVhl/actionservice.ai'

    DW_DATA = "%253Cdata%253E%253CdataObjs%2520type%253D%2522ONE_SELECT%2522%2520%2520dwName%253D%2522sys.common.new_vehicle_DW%2522%2520dwid%253D%2522dwid0.03169838701826044%2522%2520pageCount%253D%25221%2522%2520pageNo%253D%25221%2522%2520pageSize%253D%252214%2522%2520rsCount%253D%25220%2522%252F%253E%253Cfilters%2520colsInOneRow%253D%25222%2522%2520dwName%253D%2522sys.common.new_vehicle_DW%2522%253E%253Cfilter%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowBegin%253D%2522true%2522%2520name%253D%2522null%2522%2520width%253D%2522150%2522%252F%253E%253Cfilter%2520checkType%253D%2522Text%2522%2520cols%253D%25221%2522%2520dataType%253D%2522STRING%2522%2520dateFormat%253D%2522yyyy-MM-dd%2520HH%253Amm%2522%2520defaultValue%253D%2522{VEHICLE_MODEL}%2522%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isNullable%253D%2522true%2522%2520isRowBegin%253D%2522false%2522%2520isRowEnd%253D%2522false%2522%2520name%253D%2522VehicleName%2522%2520onblur%253D%2522UpperCase%28%29%2522%2520operator%253D%2522*%2522%2520rows%253D%25221%2522%2520tableName%253D%2522%2522%2520title%253D%2522%25E8%25BD%25A6%25E5%259E%258B%25E5%2590%258D%25E7%25A7%25B0%2522%2520type%253D%2522input%2522%2520width%253D%2522190%2522%2520issExtValue%253D%2522{VEHICLE_MODEL}%2522%252F%253E%253Cfilter%2520checkType%253D%2522Text%2522%2520cols%253D%25221%2522%2520dataType%253D%2522STRING%2522%2520dateFormat%253D%2522yyyy-MM-dd%2520HH%253Amm%2522%2520defaultValue%253D%2522%2522%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowEnd%253D%2522true%2522%2520name%253D%2522VehicleType%2522%2520operator%253D%2522%2522%2520optioncontent%253D%2522A%2524%7E%2524%25E8%25BF%259B%25E5%258F%25A3%2524%7E%2524B%2524%7E%2524%25E5%259B%25BD%25E4%25BA%25A7%2522%2520rows%253D%25221%2522%2520tableName%253D%2522%2522%2520title%253D%2522%25E8%25BD%25A6%25E8%25BE%2586%25E7%25A7%258D%25E7%25B1%25BB%2522%2520type%253D%2522issSelect%2522%2520width%253D%2522190%2522%2520issExtValue%253D%2522%25E8%25AF%25B7%25E9%2580%2589%25E6%258B%25A9%2522%253E%253Coption%2520value%253D%2522A%2522%253E%25E8%25BF%259B%25E5%258F%25A3%253C%252Foption%253E%253Coption%2520value%253D%2522B%2522%253E%25E5%259B%25BD%25E4%25BA%25A7%253C%252Foption%253E%253C%252Ffilter%253E%253Cfilter%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowBegin%253D%2522true%2522%2520name%253D%2522null%2522%2520width%253D%2522150%2522%252F%253E%253Cfilter%2520checkType%253D%2522Text%2522%2520cols%253D%25221%2522%2520dataType%253D%2522STRING%2522%2520dateFormat%253D%2522yyyy-MM-dd%2520HH%253Amm%2522%2520defaultValue%253D%2522%2522%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowBegin%253D%2522false%2522%2520isRowEnd%253D%2522false%2522%2520name%253D%2522BrandName%2522%2520operator%253D%2522*%2522%2520rows%253D%25221%2522%2520tableName%253D%2522%2522%2520title%253D%2522%25E5%2593%2581%25E7%2589%258C%2522%2520type%253D%2522input%2522%2520width%253D%2522190%2522%2520issExtValue%253D%2522%2522%252F%253E%253Cfilter%2520checkType%253D%2522Text%2522%2520cols%253D%25221%2522%2520dataType%253D%2522STRING%2522%2520dateFormat%253D%2522yyyy-MM-dd%2520HH%253Amm%2522%2520defaultValue%253D%2522%2522%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowEnd%253D%2522true%2522%2520name%253D%2522FamilyName%2522%2520operator%253D%2522*%2522%2520rows%253D%25221%2522%2520tableName%253D%2522%2522%2520title%253D%2522%25E8%25BD%25A6%25E7%25B3%25BB%2522%2520type%253D%2522input%2522%2520width%253D%2522190%2522%2520issExtValue%253D%2522%2522%252F%253E%253Cfilter%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowBegin%253D%2522true%2522%2520name%253D%2522null%2522%2520width%253D%2522150%2522%252F%253E%253Cfilter%2520checkType%253D%2522Text%2522%2520cols%253D%25221%2522%2520dataType%253D%2522STRING%2522%2520dateFormat%253D%2522yyyy-MM-dd%2520HH%253Amm%2522%2520defaultValue%253D%2522%2522%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowBegin%253D%2522false%2522%2520isRowEnd%253D%2522false%2522%2520name%253D%2522SearchCode%2522%2520onchange%253D%2522UpperCase%28%29%2522%2520operator%253D%2522*%2522%2520rows%253D%25221%2522%2520tableName%253D%2522%2522%2520title%253D%2522%25E8%25BD%25A6%25E5%259E%258B%25E6%2590%259C%25E7%25B4%25A2%25E7%25A0%2581%2522%2520type%253D%2522input%2522%2520width%253D%2522190%2522%2520issExtValue%253D%2522%2522%252F%253E%253Cfilter%2520checkType%253D%2522Text%2522%2520cols%253D%25221%2522%2520dataType%253D%2522STRING%2522%2520dateFormat%253D%2522yyyy-MM-dd%2520HH%253Amm%2522%2520defaultValue%253D%2522%2522%2520isGroupBegin%253D%2522true%2522%2520isGroupEnd%253D%2522true%2522%2520isHidden%253D%2522false%2522%2520isRowEnd%253D%2522true%2522%2520name%253D%2522VehicleSeat%2522%2520operator%253D%2522*%2522%2520rows%253D%25221%2522%2520tableName%253D%2522%2522%2520title%253D%2522%25E5%25BA%25A7%25E4%25BD%258D%25E6%2595%25B0%2522%2520type%253D%2522input%2522%2520width%253D%2522190%2522%2520issExtValue%253D%2522%2522%252F%253E%253C%252Ffilters%253E%253C%252Fdata%253E".format(
        VEHICLE_MODEL=VEHICLE_MODEL)

    data = "SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=vehicleAction&SERVICE_MOTHOD=queryVhl&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA=0330".format(
        DW_DATA=DW_DATA)

    ret = session.post(url_query_car_model, data=data, headers=se.HEADERS)

    return ret


# 获取vehcle_code
def get_vehcle_code(session, cmodel_code):
    url_vehcle_code = "http://ply.e-acic.com/pcis/policyAppBizAction_getVehcleCarCde/actionservice.ai"
    CUST_DATA = cmodel_code

    data = "SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=getVehcleCarCde&DW_DATA=%253Cdata%253E%253C%252Fdata%253E&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA={CUST_DATA}".format(
        CUST_DATA=CUST_DATA)

    ret = session.post(url_vehcle_code, data=data, headers=se.HEADERS)

    return ret


# 获取车型ID
def get_car_id(session, plat, frame):
    url_car_id = "http://ply.e-acic.com/pcis/policy/universal/quickapp/actionservice.ai"

    CUST_DATA = "{0}###{1}".format(frame, plat)
    CUST_DATA = urllib.quote(urllib.quote(CUST_DATA))
    data = "ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=quickBizAction&SERVICE_MOTHOD=vhlPlatQuery72_2&DW_DATA=%255B%255D&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA={CUST_DATA}".format(
        CUST_DATA=CUST_DATA)

    ret = session.post(url_car_id, data=data)

    return ret


# 通过id和验证码请求车辆信息
def get_car_info(session, PLAT_ID, YZM_CODE):
    url_plat = "http://ply.e-acic.com/pcis/quickBizAction_vhlPlatQuery73/actionservice.ai"

    CUST_DATA = "{PLAT_ID}###{YZM_CODE}".format(PLAT_ID=PLAT_ID, YZM_CODE=YZM_CODE)
    CUST_DATA = urllib.quote(urllib.quote(CUST_DATA))

    data = "SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=quickBizAction&SERVICE_MOTHOD=vhlPlatQuery73&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA={CUST_DATA}".format(
        DW_DATA=se.DW_DATA_PLAT, CUST_DATA=CUST_DATA)

    ret = session.post(url_plat, data=data)
    return ret


# 获取保费
def get_premium_data(session, DW_DATA):
    url_premium = "http://ply.e-acic.com/pcis/policy/universal/quickapp/actionservice.ai"

    data = "ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=quickAppBaseBizAction&SERVICE_MOTHOD=calcPremium&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=%3A0336%3APLY_APP_NEW_SCENE".format(
        DW_DATA=DW_DATA)

    ret = session.post(url_premium, data=data)

    return ret


# 保存
def save_premium(session, DW_DATA):
    url_save_premium = "http://ply.e-acic.com/pcis/policy/universal/quickapp/actionservice.ai"

    data = "ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=quickAppBaseBizAction&SERVICE_MOTHOD=savePlyApp&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=".format(
        DW_DATA=DW_DATA)

    ret = session.post(url_save_premium, data)

    return ret


# 核保
def he_bao(session, DW_DATA):
    url_hebao = "http://ply.e-acic.com/pcis/policy/universal/quickapp/actionservice.ai"

    data = "ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBaseBizAction&SERVICE_MOTHOD=validatePlyAppIsNotEqualQuick&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=%257B%2522CUST_DATA%2522%3A%2522%2522%257D".format(
        DW_DATA=DW_DATA)

    ret = session.post(url_hebao, data)

    return ret


def he_bao2(session, appno):
    url_hebao2 = "http://ply.e-acic.com/pcis/policy/universal/quickapp/actionservice.ai"
    updTm = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

    CUST_DATA = "appNo={appno}###updTm={updTm}###taskId=###content= ###emergency=001".format(appno=appno, updTm=updTm)
    CUST_DATA = quote(quote(CUST_DATA))
    data = "ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBaseBizAction&SERVICE_MOTHOD=submitToUnderwriting&DW_DATA=[]&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA={CUST_DATA}".format(
        CUST_DATA=CUST_DATA)

    ret = session.post(url_hebao2, data)

    return ret


# 查询核保信息
def query_hebao_data(session, appNo):
    url_query_hebao = "http://ply.e-acic.com/pcis/policyQueryBizAction_qryUnderwirttenStateList/actionservice.ai"

    date_begin = time.strftime("%Y-%m-%d", time.localtime(time.time()))  # 投保单开始时间
    date_end = time.strftime("%Y-%m-%d", time.localtime(time.time()))  # 投保单结束时间

    DW_DATA = """<data><dataObjs type="MULTI_SELECT"  dwName="policy.app_auditing_state_DW" dwid="dwid0.17062983604958437" pageCount="1" pageNo="1" pageSize="10" rsCount="0"/><filters colsInOneRow="2" dwName="policy.app_auditing_state_DW"><filter isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="true" name="null" width="150"/><filter checkType="Text" class="input400 mustinput read" codeKind="codeKind" codelistname="dataDptSet" cols="2" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="32011001" isGroupBegin="true" isGroupEnd="false" isHidden="false" isNullable="false" isReadOnly="false" isRowBegin="false" name="CDptCde" operator="2" rows="1" tableName="" title="机构部门" type="issSelect" width="430" issExtValue="32011001 安诚财产保险股份有限公司江苏分公司公司业务一部"/><filter checkType="Text" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="1" isGroupBegin="false" isGroupEnd="true" isHidden="false" isRowEnd="true" name="LoadSub" operator="2" rows="1" tableName="" title="包含下级" type="checkbox" width="70" issExtValue="1"/><filter isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="true" name="null" width="150"/><filter checkType="Select" codeKind="codeKind" codelistname="NewDataPermKind_List" cols="2" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="03" isGroupBegin="true" isGroupEnd="false" isHidden="false" isRowBegin="false" name="CKindNo" operator="*" relate="CProdNo" rows="1" title="产品" type="issSelect" width="160" issExtValue="03 机动车辆保险"/><filter checkType="Text" codeKind="codeKind" codelistname="NewDataPermProd_List" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="" isGroupBegin="false" isGroupEnd="true" isHidden="false" isRowEnd="true" name="CProdNo" operator="*" rows="1" title="" type="issSelect" width="268" issExtValue="请选择"/><filter isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="true" name="null" width="150"/><filter checkType="Text" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="{appNo}" isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="false" isRowEnd="false" maxLength="100" name="CAppNo" operator="2" rows="1" tableName="" title="投保单号" type="input" width="250" issExtValue="{appNo}"/><filter checkType="Text" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="" isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowEnd="true" maxLength="100" name="CAppNme" operator="8" rows="1" tableName="" title="投保人名称" type="input" width="250" issExtValue=""/><filter isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="true" name="null" width="150"/><filter checkType="Text" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="" isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="false" isRowEnd="false" maxLength="100" name="CInsuredNme" operator="8" rows="1" tableName="" title="被保人名称" type="input" width="250" issExtValue=""/><filter checkType="Date" cols="1" dataType="DATE" dateFormat="yyyy-MM-dd" defaultValue="{date_begin}" isGroupBegin="true" isGroupEnd="false" isHidden="false" isNullable="false" label="投保申请日期" name="TAppTmStart" onchange="compareFilterDate(this, getFilterByObj(this, 'TAppTmEnd'), this)" operator="3" rows="1" tableName="" title="投保申请日期" type="input" width="115" issExtValue="{date_begin}"/><filter checkType="Date" cols="1" dataType="DATE" dateFormat="yyyy-MM-dd" defaultValue="{date_end}" isGroupBegin="false" isGroupEnd="true" isHidden="false" isNullable="false" isRowEnd="true" name="TAppTmEnd" onchange="compareFilterDate(getFilterByObj(this, 'TAppTmStart'), this, this)" operator="1" rows="1" tableName="" title="-" type="input" width="115" issExtValue="{date_end}"/><filter isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="true" name="null" width="150"/><filter checkType="Text" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="" isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="false" isRowEnd="false" maxLength="100" name="CPlateNo" operator="2" rows="1" tableName="" title="车牌号码" type="input" width="250" issExtValue=""/><filter checkType="Text" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="" isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowEnd="true" maxLength="100" name="CEngNo" operator="2" rows="1" tableName="" title="发动机号" type="input" width="250" issExtValue=""/><filter isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="true" name="null" width="150"/><filter checkType="Text" cols="1" dataType="STRING" dateFormat="yyyy-MM-dd HH:mm" defaultValue="" isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowBegin="false" isRowEnd="false" maxLength="100" name="CFrmNo" operator="2" rows="1" tableName="" title="车架号" type="input" width="250" issExtValue=""/><filter isGroupBegin="true" isGroupEnd="true" isHidden="false" isRowEnd="true" name="" width="150"/></filters></data>""".format(
        appNo=appNo, date_begin=date_begin, date_end=date_end)

    DW_DATA = quote(quote(DW_DATA))
    data = "SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyQueryBizAction&SERVICE_MOTHOD=qryUnderwirttenStateList&DW_DATA={DW_DATA}&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA=sysCde%253DPOLY_AUTO%2523%2523%2523scene%253DA".format(
        DW_DATA=DW_DATA)

    ret = session.post(url_query_hebao, data, headers=se.HEADERS)

    return ret


# 查询核保失败原因
def query_hebao_reason(session, appNo):
    url_query_reason = "http://ply.e-acic.com/pcis/policyTraceQueryAction_queryPolicyTraceByAppNo/actionservice.ai"

    data = "SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyTraceQueryAction&SERVICE_MOTHOD=queryPolicyTraceByAppNo&DW_DATA=%253Cdata%253E%253C%252Fdata%253E&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA={appNo}".format(
        appNo=appNo)

    ret = session.post(url_query_reason, data, headers=se.HEADERS)

    return ret
