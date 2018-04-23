# -*- coding:utf-8 -*-
__author__ = 'weikai'
from io import BytesIO
import  time
import urlparse
import datetime
import traceback

from PIL import Image

from img.damatuWeb import DamatuApi
from common.log import Logger
from img import imagebse64

log=Logger()

def pic2Str(filename):
    log.info(u'调用打码开始')
    try:
        dmt = DamatuApi()
        str=dmt.decode(filename,200)
        log.info(u'调用打码结束 验证码:%s:'% (str))
        return str
    except Exception,e:
        log.error(traceback.format_exc())
        log.error('打码兔返回错误')

        return 'ssss'

def readImage(response,name):
    i = Image.open(BytesIO(response.content))
    i.save(name)
    basestr = imagebse64.img2base64(name)
    return basestr


def getTimstamp():
    return "%d" % (time.time() * 1000)

def url2dict(url):
    query=urlparse.urlparse(url).query
    return dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])

def getgender(beforeProposalNo):
        if int(beforeProposalNo[16:17])%2==0:
         return  '2'
         #女
        else:
         return  '1'
         #男
def getbirthday(beforeProposalNo):
    #返回出生日期
     return  beforeProposalNo[6:10]+'/'+beforeProposalNo[10:12]+'/'+beforeProposalNo[12:14]

#返回当前日期
def getnowdate():
    nowdate = str(datetime.date.today()).replace('-','/')
    return nowdate
#返回当前日期
def getlatedate(i):
    nowdate = datetime.date.today()#
    tomorrow = nowdate + datetime.timedelta(days=i)
    return str(tomorrow)

def readImage(response,name):
    i = Image.open(BytesIO(response.content))
    i.save(name)
    basestr = imagebse64.img2base64(name)
    return basestr