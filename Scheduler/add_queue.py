# -*- coding:utf-8 -*-
__author__ = 'weikai'

'''
        BATCH_PROCESS_QUEUE,  -- 批量队列
        FILL_UP_QUEUE, -- 补全 队列
        PICC_QUEUE, -- 中国人保队列
        CHINA_CONTINENT_QUEUE, -- 中国大地队列
        CHINA_JOINT_QUEUE; -- 中华联合队列
'''
import stomp
import json
import traceback
import settings as se


def add(data):
    try:
        picc_queue = se.PICC_QUEUE
        CHINA_CONTINENT_QUEUE = se.CHINA_CONTINENT_QUEUE
        CHINA_JOINT_QUEUE = se.CHINA_JOINT_QUEUE
        conn = stomp.Connection10([(se.i_config.MQIP, se.i_config.MQPORT)])
        # data=t=[{'VIN_NO':'LHGCM567852063612','INSURE_CAR_ID':75},{'VIN_NO':'UU6MF48411D017474','INSURE_CAR_ID':76},{'VIN_NO':'LVSFDFAB6AN188127','INSURE_CAR_ID':77},{'VIN_NO':'LDNH4LGE970154536','INSURE_CAR_ID':78}]
        conn.start()
        conn.connect()
        conn.send(body=json.dumps(data).encode(), destination=picc_queue)
        conn.send(
            body=json.dumps(data).encode(),
            destination=CHINA_CONTINENT_QUEUE)
        conn.send(
            body=json.dumps(data).encode(),
            destination=CHINA_JOINT_QUEUE)
        conn.disconnect()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
