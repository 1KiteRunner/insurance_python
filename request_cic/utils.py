# -*- coding:utf-8 -*-
__author__ = 'weikai'
import collections
import time
import datetime


def getCuttime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def readCookies():
    file_object = open('cookies.pkl')
    try:
        all_the_text = file_object.read()
        all_the_text.split(":", )
        print(all_the_text)

    finally:
        file_object.close()


def minTime(date1, date2):
    # date1小于date2 返回相差秒数
    # date1大于date2返回86399-seconds
    date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
    return (date2 - date1).seconds


# 86399 86398
# print(minTime('2017-01-03 15:09:33','2017-01-03 15:09:35'))


def getlatedate(i, str_date=''):
    if str_date == '':
        nowdate = datetime.date.today()  #
        tomorrow = nowdate + datetime.timedelta(days=i)
        return str(tomorrow)
    else:
        str_date = datetime.datetime.strptime(str_date, "%Y-%m-%d").date()
        tomorrow = str_date + datetime.timedelta(days=i)
        return str(tomorrow)


# 字典混合编码 utf-8 与  unicode 同意转为str
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


if __name__ == "__main__":
    print getlatedate(0)
