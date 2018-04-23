# -*- coding:utf-8 -*-
__author__ = 'weikai'

import requests
from common.config import DAMA_IP,queryCode,reportverificationCode

def _dama_requests(url,base64):
    data={"file":base64}
    hdr={"Content-Type":"application/x-www-form-urlencoded"}
    damarsp = requests.post(url=url,data=data,headers=hdr)
    if damarsp.status_code==200 and damarsp.text!="":
        damajson=damarsp.json()
        text=damajson['text']
        code=damajson['code']
        if code=="1":
            return text
        else:
            return "ERROR"
    else:
        return "ERROR"

def query_Code(base64):
    out =_dama_requests(DAMA_IP+queryCode,base64)
    return  out

def report_verificationCode(base64):
    _dama_requests(DAMA_IP+reportverificationCode,base64)

import os
import base64
lista=[]
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        #print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题

        lista.append(child.decode('gbk'))
    return lista

if __name__=="__main__":
    bas="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"
    #print  query_Code(bas).upper()
    requests.post("http://www.baidu.com/%s"%("中文"),data="123")
    '''
    filelist=eachFile("C:\Users\weikai\Desktop\img\\")

    print("asd23".upper())
    for i in filelist:
        try:
            f=open(i,"rb")
            bastr=base64.b64encode(f.read())
            mycode=i[-8:-4]
            codestr=query_Code(bastr).upper()

            if len(codestr)==3:
                report_verificationCode(bastr)
            if mycode!=codestr:
                print("mycode %s codestr %s" %(mycode ,codestr))
        except Exception as e:
            print(e)
    '''