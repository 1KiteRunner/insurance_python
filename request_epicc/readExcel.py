# -*- coding:utf-8 -*-
import xlrd
__author__ = 'weikai'
import copy
import json
import os
import time
from request_thread import threadpool
import datetime
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            if ".del" in s:
                continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

def redExcel(list):
    #fname = e
    try:

        list_1 = []
        for fname in list:
            bk = xlrd.open_workbook(fname)
            shxrange = range(bk.nsheets)
            try:
                sh = bk.sheet_by_index(0)
                newWb = copy(bk)
                newWs = newWb.get_sheet(0);
            except:
                print "no sheet in %s named Sheet1" % fname
            nrows = sh.nrows
            ncols = sh.ncols
            # 获取第一行第一列数据

            # 获取各行数据
            for i in range(1, nrows):
                row_list = sh.row_values(i)
                list_1.append({'insuredName':row_list[0],
                               'insuredIDNumber':row_list[1],
                               'insuredPhNo':row_list[2],
                               #'address':row_list[3],
                               'LicenseNo':row_list[4],
                               #'VEHICLE_MODELSH':row_list[5],
                               #'carddate':row_list[6],
                               #'regisdate':row_list[7],
                               'EngineNo':str(row_list[8]).split('.')[0],#发动机号纯数字可能会带点
                               'FrameNo':row_list[9],
                               'cityCode':str(int(row_list[10]))
                               })
        for e in list:
            os.rename(e, e + ".del")
            #jsonstr = json.dumps(dict_list,ensure_ascii=False)
        threadpool(list_1)
            #return jsonstr
    except Exception,e:
        print e
if __name__ == '__main__':
    while True:
        try:
            # list = GetFileList('C:\Users\memedai\Downloads\excel', [])
            list = GetFileList('C:\usr\local\src\insurance', [])
            if len(list)==0:
                print "==========：" + str(datetime.datetime.now())
                time.sleep(60*30)
                print "==============："+ str(datetime.datetime.now())
            else:
                print "=================：" + str(datetime.datetime.now())
                redExcel(list)
        except Exception,e:
            print "-=========:" + str(datetime.datetime.now())
#redExcel("C:\\Users\\weikai\\PycharmProjects\\robotframwork-lib\\webdr\\file\\D_20161223134648_843a28e6-c254-4820-b740-ddf626e5b7bc.xlsx")

