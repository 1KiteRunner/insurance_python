# -*- coding:utf-8 -*-
__author__ = 'weikai'
#通过车架号获取车辆型号信息
import  re
import sys
from request_cic import cic_settings as SE
import requests
from parse import parseCarInfo
from Scheduler.session import getSession

reload(sys)
sys.setdefaultencoding('utf8')
from common.log import *
log=Logger()
def get_car_model(searchVin,requesteicc=None):
    try:
        if requesteicc is None:
            requesteicc=getSession()['4']
        headers = SE.headers
        #获取查询车辆精确信息的MD5
        res3=requesteicc.get(url='http://carply.cic.cn/pcis/policy/universal/quickapp/quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0')
        res_body=res3.text
        if res3.status_code==200:
            md5byJy=re.findall(r"md5byJy = \"(.+?)\";",res_body,re.S)[0]
        else:
            res_body=requesteicc.get(url='http://carply.cic.cn/pcis/policy/universal/quickapp/quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0')
            res_body=res3.text
            md5byJy=re.findall(r"md5byJy = \"(.+?)\";",res_body,re.S)[0]
        request114=requests.session();
        headers114=SE.headers
        request114.headers.update(headers114)
        #车架号
        #searchVin='LMVHEKFD6EA029484'
        #searchVin='LFV2A11K8F4192886'
        validNo=md5byJy
        #vehicleId='I0000000000000000230000000000033'
        search_url='http://114.251.1.161/zccx/search?regionCode=00000000&jyFlag=0&businessNature=A&operatorCode=0000000000&returnUrl=http://carply.cic.cn/pcis/offerAcceptResult&vname=&searchVin='+searchVin+'&vinflag=1&validNo='+validNo
        repon114=request114.get(url=search_url)
        if "没有找到符合条件的数据" in repon114.text:
            log.error(u"没有找到符合条件的数据")
            return None
        else:
            carlist = parseCarInfo(repon114.text)
            return carlist[0]
    except Exception as e:
        log.error(e)
        import traceback
        log.error(traceback.format_exc())

if __name__=="__main__":
    import json

    car=get_car_model('LFV2B25G0E5140444')
    print(json.dumps(car,ensure_ascii=False))