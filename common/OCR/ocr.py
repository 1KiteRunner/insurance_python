# -*- coding:utf-8 -*-
__author__ = 'weikai'
import os, sys
from pyocr import libtesseract
from pyocr.builders import TextBuilder
from PIL import Image
from PIL import Image, ImageEnhance, ImageFilter

'''
当前目录必须有tessdata ,libtesseract304.dll ,liblept172.dll
修改C:\Python27\Lib\site-packages\pyocr\libtesseract文件中的dll
安装vc_redist.x64.exe
'''


def ocr_code(filename, lang='eng'):
    tessdir = os.getenv('TESSDATA_PREFIX', None)
    if tessdir is None:
        tessdir = os.path.split(os.path.realpath(__file__))[0]
        os.environ['TESSDATA_PREFIX'] = tessdir
    if tessdir not in os.environ['PATH']:
        os.environ['PATH'] = tessdir + ';' + os.environ['PATH']

    if isinstance(filename, Image.Image):
        img = filename
    else:
        img = Image.open(filename)
    # 不设置成单行模式,没有输出
    bu = TextBuilder(tesseract_layout=7)
    # lang为语言,默认使用eng fontyp

    code = libtesseract.image_to_string(img, lang=lang, builder=bu)
    return code.replace(" ", "").upper()


def change_pic(filename):
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    if isinstance(filename, Image.Image):
        im = filename
    else:
        im = Image.open(filename)

    enhancer = ImageEnhance.Contrast(im)
    enhancer = enhancer.enhance(4)
    imgry = im.convert('L')
    # 保存图像
    # imgry.save('g' + name)
    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')
    return out


if __name__ == "__main__":
    print libtesseract.__all__
    print ocr_code("1.tif",lang="fontyp")
    print ocr_code("2.tif",lang="fontyp")
