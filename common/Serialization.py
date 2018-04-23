# -*- coding:utf-8 -*-
__author__ = 'weikai'
import codecs
import cPickle as pickle

# 对象转为base64


def instance2base64(instance):
    return codecs.encode(pickle.dumps(instance), "base64").decode()

# base64转为对象


def base642instance(base64str):
    return pickle.loads(codecs.decode(base64str.encode(), "base64"))
