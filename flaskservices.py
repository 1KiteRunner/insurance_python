# -*- coding:utf-8 -*-
__author__ = 'weikai'
import  json
import traceback

from flask import Flask, request, jsonify

from common.log import Logger
from request_epicc.interface.isRenewal import isRenewal2
from  request_epicc import settings as SE

log = Logger(SE.logpath +'Flask.log')
app = Flask(__name__)



@app.route('/flask/epicc',methods=['POST'])
def getepicc():
    try:
        data = json.loads(request.data)
        if data!=None:
            cityCode=data['cityCode']
            insuredIDNumber=data['insuredIDNumber']
            insuredName=data['insuredName']
            LicenseNo=data['LicenseNo']
            FrameNo=data['FrameNo']
            EngineNo=['EngineNo']
            log.info(data)
            if cityCode=="" or insuredIDNumber=="" or insuredName=="" or LicenseNo=="" or FrameNo=="" or EngineNo=="":
                return jsonify({'result':'error','content':{},'code':'1001','message':u'参数不能为空'})
            else:
                isRenewal2(data)
                return jsonify({'result':'success','content':{},'code':'1000','message':''})
    except Exception,e:
        log.error(traceback.format_exc())
        return jsonify({'result':'error','content':{},'code':'1001','message':u'未知异常'})


if __name__ == "__main__":
    app.run(host="99.48.58.5",port=5000,debug=True,threaded=True)
