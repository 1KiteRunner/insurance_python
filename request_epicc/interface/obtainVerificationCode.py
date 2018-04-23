# -*- coding:utf-8 -*-
__author__ = 'weikai'
from common.log import Logger
from request_epicc import settings as se
headers = se.headers
import requests
import urllib
import jsonpath
from request_epicc import  utils
import base64
import traceback
log = Logger()
def getobtainVerificationCode(licenseno,sessionid,frameNo):
    try:
        #请求车管所验证码并且打码
        #######################################
        log.info(u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================开始")
        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput2'
        #obtainVerificationCodebody='licenseNo=%E8%http://www.epicc.com.cn8B%8FA44444&frameNo=LVZA43F93EC554224&channelNo=2&sessionId='+sessionid
        obtainVerificationCodebody={
                                "licenseNo": licenseno,
                                "sessionId": sessionid,
                                "frameNo": frameNo,
                                "channelNo": "2"
                                 }
        obtainVerificationCodebody=urllib.urlencode(obtainVerificationCodebody)
        obtainVerificationCode_response=requests.post(url='http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode',headers=headers,data=obtainVerificationCodebody)
        obtainVerificationCode_body = obtainVerificationCode_response.json()
        code_msg=obtainVerificationCode_body['message']
        code_msg=eval(code_msg)
        check_code = jsonpath.jsonpath(code_msg,'$.check_code')[0]
        #log.info("check_code=%s" % check_code)
        #fname=se.imagePath+utils.getTimstamp()+'.jpg'
        #log.info('code =%s'% check_code)
        #log.info('picnam =%s'% fname)
        #imagebse64.base642img(check_code,fname)
        codestr=utils.pic2Str(base64.b64decode(check_code))
        log.info(u"验证码为=%s"% (codestr))
        log.info(u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================结束")
        return codestr
    except Exception,e:
        log.error(e)
        log.error(traceback.format_exc())
        log.error(u"验证码流程异常")

#getobtainVerificationCode('苏A44444','4a9491a5-0460-459d-9d6b-e3c79634ee3a','LVZA43F93EC554224')