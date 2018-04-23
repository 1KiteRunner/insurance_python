# -*- coding:utf-8 -*-
__author__ = 'weikai'
import urllib
import re
import traceback

import request_cic.cic_settings as se
from request_cic.parse import parsedataObjs
from common.dama.damaUtil import dama
from common.log import Logger

log = Logger()
headers = se.headers


# headers['Content-Type']='application/x-www-form-urlencoded'
def getCode(requesteicc, searchVin):
    try:
        dt = {}
        #####################请求车管所信息#############################################
        # plateNo='苏AB1S17'
        plateNo = ''
        CUST_DATA = 'plateNo=' + plateNo + '&frmNo=' + searchVin
        CUST_DATA = urllib.quote(urllib.quote(CUST_DATA))
        getcodeinfo_url = 'http://carply.cic.cn/pcis/policy/universal/quickapp/actionservice.ai'
        getcodeinfo_data = 'ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=vhlPlatformCommonAction&SERVICE_MOTHOD=getJsCheckInfo&DW_DATA=%255B%255D&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=' + CUST_DATA
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        getcodeinforesp = requesteicc.post(url=getcodeinfo_url, data=getcodeinfo_data, headers=headers)
        getcodeinforesp = getcodeinforesp.json()

        if getcodeinforesp['RESULT_TYPE'] == 'SUCCESS':
            checkNo = getcodeinforesp['JSON_OBJ']['checkNo']
            checkCode = getcodeinforesp['JSON_OBJ']['checkCode']
            dt['checkNo'] = checkNo
            dt['checkCode'] = checkCode
            # 打码
            gCValidateCode = dama("3", checkCode)
            dt['gCValidateCode'] = gCValidateCode
            return dt
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())


def getCarInof(requesteicc, searchVin):
    try:
        dt = getCode(requesteicc, searchVin)
        checkNo = dt['checkNo']
        codestr = dt['gCValidateCode']
        # http://carply.cic.cn/pcis/policy/universal/pop/vhl/vhl_info_confirm.jsp?all=【0332|32010101】,72CICP320017001483515917692846|GXZV|苏BG027F|LHGCM567852063612
        ###############################校验验证码############################################
        log.info(u"------------------getCarInof.start--------------------------------")
        # plateNo='苏AB1S17'
        plateNo = ''
        # print(checkCode)
        # print(plateNo.decode('utf-8'))
        confirm_url = 'http://carply.cic.cn/pcis/actionservice.ai'

        alldata = checkNo + '|' + codestr + '|' + plateNo.decode('utf-8') + '|' + searchVin

        alldata = urllib.quote(urllib.quote(alldata.encode('utf-8')))
        confirm_data = 'SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=getVhlConfirmInfo&DW_DATA=%253Cdata%253E%253CdataObjs%2520type%253D%2522ONE_SELECT%2522%2520%2520dwName%253D%2522policy.pub.vhl_inf_confirm_DW%2522%2520dwid%253D%2522dwid0.3056373666299691%2522%2520pageCount%253D%25221%2522%2520pageNo%253D%25221%2522%2520pageSize%253D%252215%2522%2520rsCount%253D%25220%2522%252F%253E%253Cfilters%2520colsInOneRow%253D%25222%2522%2520dwName%253D%2522policy.pub.vhl_inf_confirm_DW%2522%252F%253E%253C%252Fdata%253E&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA=all%253d%25e3%2580%25900332%257c32010101%25e3%2580%2591%252c' + alldata

        confirmresp = requesteicc.post(url=confirm_url, data=confirm_data, headers=headers)
        confirmresp = confirmresp.text
        sucess = re.findall(r"RESULT_MSG:\'(.+?)\',", confirmresp, re.S)[0]
        count = 1
        while u'校验码有误' in sucess and count < 4:
            log.error(u"验证码有误重发")
            dama("99", dt['checkCode'])
            dt = getCode(requesteicc, searchVin)
            checkNo = dt['checkNo']
            codestr = dt['gCValidateCode']
            alldata = checkNo + '|' + codestr + '|' + plateNo.decode('utf-8') + '|' + searchVin
            alldata = urllib.quote(urllib.quote(alldata.encode('utf-8')))
            confirm_data = 'SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=getVhlConfirmInfo&DW_DATA=%253Cdata%253E%253CdataObjs%2520type%253D%2522ONE_SELECT%2522%2520%2520dwName%253D%2522policy.pub.vhl_inf_confirm_DW%2522%2520dwid%253D%2522dwid0.3056373666299691%2522%2520pageCount%253D%25221%2522%2520pageNo%253D%25221%2522%2520pageSize%253D%252215%2522%2520rsCount%253D%25220%2522%252F%253E%253Cfilters%2520colsInOneRow%253D%25222%2522%2520dwName%253D%2522policy.pub.vhl_inf_confirm_DW%2522%252F%253E%253C%252Fdata%253E&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA=all%253d%25e3%2580%25900332%257c32010101%25e3%2580%2591%252c' + alldata
            confirmresp = requesteicc.post(url=confirm_url, data=confirm_data, headers=headers)
            confirmresp = confirmresp.text
            sucess = re.findall(r"RESULT_MSG:\'(.+?)\',", confirmresp, re.S)[0]
            log.info('cic RESULT_MSG %s ', sucess)
            count += 1

        if "未匹配到交管车辆信息" in re.findall(r"RESULT_MSG:\'(.+?)\',", confirmresp, re.S)[0]:
            return "车险平台返回信息 未匹配到交管车辆信息，可提交电子联系单至平台进行核实！"

        cardict = parsedataObjs(confirmresp)
        cardict['checkNo'] = checkNo
        cardict['gCValidateCode'] = codestr
        # log.info('cardict%s'% json.dumps(cardict,ensure_ascii=False))
        log.info(u"------------------getCarInof.end--------------------------------")
        return cardict
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
        return "未知问题"
