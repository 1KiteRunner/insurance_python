# -*- coding:utf-8 -*-
__author__ = 'weikai'
from common.mongodb.mongo_model import MongoModel
from common.log import Logger
import traceback
from gevent import monkey, sleep
monkey.patch_all()

log = Logger()


# InsuranceInfo  车管所查询信息 、renrwalInfo 续保查询的信息
def mg_insert(collection, data):
    try:
        client = MongoModel()
        client.insert(collection, {"BODY": data})
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


# 查询#{'BODY.FRAME_NO': FRAME_NO}
def mg_update_insert(collection, query, data):
    try:
        client = MongoModel()
        # client.update_insert(collection, query, {"$set": {"BODY": data}})
        client.update_insert(collection, query, {"BODY": data})
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


## 查询{'BODY.PALTE_NO': '苏A92Q62'}
def mg_find(collection, query):
    try:
        client = MongoModel()
        data = client.find(collection, query)
        if data != None:
            if data.has_key('_id'):
                data.pop('_id')
                return data['BODY']
            else:
                return data['BODY']
        else:
            return None
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return None


def mg_find_all(collection, query):
    try:
        client = MongoModel()
        datas = client.find_data(collection, query)

        return [data['BODY'] for data in datas if data.has_key('BODY')]
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return None