# -*- coding: utf8 -*-
from img.damatuWeb import DamatuApi
from common.log import Logger
log = Logger()


def pic2Str(filename):
    try:
        log.info(u"开始调用打码兔")
        dmt = DamatuApi()
        str = dmt.decode(filename, 200)
        log.info(u"调用打码兔结束 验证码为 %s " % str)
        return str
    except Exception as e:
        log.error(u"打码兔异常--------------------------------")
        return 'ssss'
