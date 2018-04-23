# -*- coding:utf-8 -*-
__author__ = 'weikai'
import time
import datetime


# 格式化日期换算成时间戳


def conver_timestamp(dt="2016-05-05 20:28:54"):
    # 转换成时间数组
    timearray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timearray)
    return int(timestamp)


def getlatedate(i, str_date=''):
    if str_date == '':
        nowdate = datetime.date.today()  #
        tomorrow = nowdate + datetime.timedelta(days=i)
        return str(tomorrow)
    str_date = datetime.datetime.strptime(str_date, "%Y-%m-%d").date()
    tomorrow = str_date + datetime.timedelta(days=i)
    return str(tomorrow)


# 时间戳格式化


def conver_time(timestamp=1462451334):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def getgender(beforeProposalNo):
    if int(beforeProposalNo[16:17]) % 2 == 0:
        return 'F'
        # 女

    return 'M'
    # 男


def getbirthday(beforeProposalNo):
    # 返回出生日期
    return beforeProposalNo[6:10] + '-' + \
           beforeProposalNo[10:12] + '-' + beforeProposalNo[12:14]


# 判断时间是否超过40天
def compare_time40(endtime="2017-04-03 23:59:59"):
    try:
        if " " not in endtime:
            endtime = endtime + " 23:59:59"

        currnt_time = int(time.time())
        endtime = conver_timestamp(endtime)
        out = (endtime - currnt_time) / 86400
        return out
    except Exception as e:
        return 10  # 如果有异常随便给个小于40的
