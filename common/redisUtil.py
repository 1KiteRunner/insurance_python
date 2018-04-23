# -*- coding:utf-8 -*-
__author__ = 'weikai'
import redis
from common.config import REDIS_HOST
from common.timeUtil import get_seconds
from common.config import SESSIONTIME
from common.config import REDIS_PASSWORD


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CRedis:
    #单例模式
    __metaclass__ = Singleton

    def __init__(self):
        self.host = REDIS_HOST
        # self.host = '127.0.0.1'
        self.port = 6379
        self.db = 0
        self.password = REDIS_PASSWORD
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password,
                                         max_connections=50)
        # self.r = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)
        self.r = redis.Redis(connection_pool=self.pool)

    # 1. strings 类型及操作
    # 设置 key 对应的值为 string 类型的 value
    def set(self, key, value):
        return self.r.set(key, value)

    # 设置 key 对应的值为 string 类型的 value。如果 key 已经存在,返回 0,nx 是 not exist 的意思
    def setnx(self, key, value):
        return self.r.setnx(key, value)

    # 设置 key 对应的值为 string 类型的 value,并指定此键值对应的有效期
    def setex(self, key, time, value):
        return self.r.setex(key, time, value)

    # 设置指定 key 的 value 值的子字符串
    # setrange name 8 gmail.com
    # 其中的 8 是指从下标为 8(包含 8)的字符开始替换
    def setrange(self, key, num, value):
        return self.r.setrange(key, num, value)

    # 获取指定 key 的 value 值的子字符串
    def getrange(self, key, start, end):
        return self.r.getrange(key, start, end)

    # mget(list)
    def get(self, key):
        if isinstance(key, list):
            return self.r.mget(key)
        else:
            return self.r.get(key)

    # 删除
    def remove(self, key):
        return self.r.delete(key)

    # 自增
    def incr(self, key, default=1):
        if (1 == default):
            return self.r.incr(key)
        else:
            return self.r.incr(key, default)

    # 自减
    def decr(self, key, default=1):
        if (1 == default):
            return self.r.decr(key)
        else:
            return self.r.decr(key, default)

    # 2. hashes 类型及操作
    # 根据email获取session信息
    def hget(self, email):
        return self.r.hget('session', email)

    # 以email作为唯一标识，增加用户session
    def hset(self, email, content):
        return self.r.hset('session', email, content)

    # 获取session哈希表中的所有数据
    def hgetall(self):
        return self.r.hgetall('session')

    # 删除hashes
    def hdel(self, name, key=None):
        if (key):
            return self.r.hdel(name, key)
        return self.r.hdel(name)

    # 清空当前db
    def clear(self):
        return self.r.flushdb()

    # 3、lists 类型及操作
    # 适合做邮件队列
    # 在 key 对应 list 的头部添加字符串元素
    def lpush(self, key, value):
        return self.r.lpush(key, value)

    # 从 list 的尾部删除元素,并返回删除元素
    def lpop(self, key):
        return self.r.plush(key)

    # 输入车架号，公司id
    def get_vin(self, vin, compayid):
        try:
            key = vin + "_" + compayid
            return self.r.get(key)
        except Exception as e:
            print(e)

    # 输入车架号公司id 消息体 存储

    def set_vin(self, vin, compayid, body):
        try:
            key = vin + "_" + compayid
            return self.r.setex(key, body, get_seconds())
        except Exception as e:
            print(e)

    # 获取session
    def get_session_redis(self, compayid):
        try:
            if isinstance(compayid, list):
                keylist = []
                for i in compayid:
                    key = i + "_COMPANY"
                    keylist.append(key)
                return self.r.mget(keylist)
            else:
                return self.r.get(compayid + "_COMPANY")
        except Exception as e:
            print(e)
            return None

    # 设置session

    def set_session_redis(self, session, compayid):
        try:
            key = compayid + "_COMPANY"
            if compayid == '2':
                return self.r.set(key, session)
            return self.r.setex(key, session, SESSIONTIME)
        except Exception as e:
            print(e)

    def set_appno(self, appno, compayid):
        try:
            key = compayid + "_APPNO"
            return self.r.sadd(key, appno)
        except Exception as e:
            print e

    def sadd(self, key, value):
        return self.r.sadd(key, value)

    def srem(self,key, member):
        return self.r.srem(key, member)

    def smembers(self, key):
        return self.r.smembers(key)


if __name__ == '__main__':

    import datetime

    r = CRedis()
    print id(r)

    r2 = CRedis()
    print id(r2)

    try:
        r.set_vin("aaa", "3", "0000000000000")
        # r.remove("aaa")
    except Exception as e:
        print(e)
