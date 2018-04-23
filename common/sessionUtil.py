# -*- coding:utf-8 -*-
__author__ = 'weikai'
from common.Serialization import instance2base64, base642instance
from common.redisUtil import CRedis

r = CRedis()

# 获取session对象 返回request对象


def get_session(compayid):
    base64str = r.get_session_redis(compayid)
    if isinstance(base64str,list):
        oplist=[]
        for str in base64str:
            if str!=None:
                oplist.append(base642instance(str))
            else:
                oplist.append(None)
        return oplist

    elif base64str!=None:
        return base642instance(base64str)
    else:
        return None

# 设置session


def set_session(session,compayid):
    base64str=instance2base64(session)
    r.set_session_redis(base64str,compayid)

if __name__=="__main__":
    s=get_session(["1","4","5"])
    print(s)