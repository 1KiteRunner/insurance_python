# -*- coding:utf-8 -*-
__author__ = 'weikai'
import settings as se
import json

#实时发送是否可以续保
def send_complete_flag(
        client,
        plateNumber, #车牌号
        completeFlag,#1 是 ，0 否
        isPhone,
        sessionId,
        carInfo=""):#车辆信息
    complete2 = {
        "plateNumber": plateNumber,
        "completeFlag": completeFlag,
        "isPhone": isPhone,
        "sessionId": sessionId,
        "carInfo": carInfo}
    client.send(
        body=json.dumps(
            complete2,
            ensure_ascii=False).encode(),
        destination=se.COMPLETE_FLAG)
#批量时候推送后台是否存在用户信息
def send_batch_complete_flag(
        client,
        plateNumber, #车牌号
        completeFlag,#1 是 ，0 否
        carInfo=""):#车辆信息
    complete2 = {
        "plateNumber": plateNumber,
        "completeFlag": completeFlag,
        "carInfo": carInfo}
    client.send(
        body=json.dumps(
            complete2,
            ensure_ascii=False).encode(),
        destination=se.BATCH_COMPLETE_FLAG)