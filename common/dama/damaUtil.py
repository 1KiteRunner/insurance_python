# -*- coding:utf-8 -*-
__author__ = 'weikai'
import re
import base64
import traceback

from yunsu import APIClient
from common.dama.damatuWeb import DamatuApi
from common.log import Logger
from common.dama.mydam import query_Code,report_verificationCode

log = Logger()

#打码工具
'''
1 打码兔
2 云打码 云打码只能打4位字母数字 http://www.ysdm.net
3 自己的打码
'''
def dama(type, base64str, flag=0):
    try:
        if type == "2":
            client = APIClient()
            paramKeys = ['username',
                         'password',
                         'typeid',
                         'timeout',
                         'softid',
                         'softkey'
                         ]
            paramDict = {'username': 'nanmi2016',
                         'password': 'qwer1234',
                         'typeid': '3040',
                         'timeout': '10',
                         'softid': '1',
                         'softkey': 'b40ffbee5c1cf4e38028c197eb2fc751'
                         }
            log.info(u'调用云打码打码开始')
            result = client.http_upload_image(
                "http://121.43.68.66/create.xml",
                paramKeys,
                paramDict,
                base64.b64decode(base64str))
            code = re.findall(r"<Result>(.+?)</Result>", result, re.S)[0]
            log.info(u'调用云打码打码结束 验证码:%s:' % (code))
            return code

        if type == "1":
            dmt = DamatuApi()
            log.info(u'调用打码兔打码开始')
            code = dmt.decode(base64.b64decode(base64str), 200)
            log.info(u'调用打码兔打码结束 验证码:%s:' % (code))
            return code

        if type=="3":
            log.info(u'调用老王打码开始')
            code=query_Code(base64str)
            log.info(u'调用老王打码结束 验证码:%s:' % (code))
            return code

        if type=="99":
            log.info(u'上报错误验证码')
            report_verificationCode(base64str)

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        if flag == 0:
            code=dama(type, base64str, 1)
            return code
if __name__ == "__main__":
    bas = "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"
    print dama("3", bas)
    #print dama("1", bas)

    #data="file=%s"% urllib.quote(bas)
    data={"file":bas}
    import requests

    ip="http://52.80.31.10:8088/"
    url1="verificationCode/verificationCode/queryCode"
    url2="verificationCode/verificationCode/reportverificationCode"
    hdr={"Content-Type":"application/x-www-form-urlencoded"}
    #ss= requests.post(url=ip+url1,data=data,headers=hdr)
    ss= requests.post(url=ip+url2,data=data,headers=hdr)
    print(ss.text)
    print(ss.status_code)
