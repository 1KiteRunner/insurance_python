# -*- coding:utf-8 -*-
__author__ = 'weikai'
from common.OCR.ocr import ocr_code, change_pic
import base64
from common.log import Logger
from io import BytesIO

log = Logger()


def dama_huanong(base64str):
    try:
        code = ocr_code(change_pic(BytesIO(base64.b64decode(base64str)))).replace("7:", "?=").replace("O", "0").replace(
            "o", "0").replace("l", "1").replace("A", "8").replace("72", "?=").replace("Z", "2").replace("z",
                                                                                                        "2").replace(
            "s", "8").replace("S", "8")
        log.info("code %s " % code)
        if "+" in code:
            code = code.replace("+", "").replace("?", "")
            ls = code.split("=")
            a = int(ls[0])
            b = int(ls[1])
            return b - a
        else:
            log.error(base64str)
            return 0
    except Exception as e:
        import traceback
        log.error(traceback.format_exc())
        log.error(e)
        log.error(base64str)
        return 0
