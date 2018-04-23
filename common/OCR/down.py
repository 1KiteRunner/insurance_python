# -*- coding:utf-8 -*-
__author__ = 'weikai'
from io import BytesIO
import time

import requests
from PIL import Image, ImageEnhance

from common.OCR.ocr import ocr_code

threshold = 140

table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
# name = "1.tif"
for i in xrange(200):
    rsp = requests.get("https://icore-pts.pingan.com.cn/ebusiness/auto/rand-code-imgage.do")
    im = Image.open(BytesIO(rsp.content))
    enhancer = ImageEnhance.Contrast(im)
    enhancer = enhancer.enhance(4)
    imgry = im.convert('L')
    # 保存图像
    # imgry.save('g' + name)
    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')

    name = ocr_code(out,lang="fontyp")
    name = name.replace(" ", "")
    if name == "":
        name = str(i)
    print(name + "----")
    out.save("C:\Users\weikai\Desktop\ocr\\tran\\" + name + ".tif")
    time.sleep(0.5)
