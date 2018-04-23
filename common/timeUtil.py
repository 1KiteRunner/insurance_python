# -*- coding:utf-8 -*-
import datetime
import time


# 获取当前时间距离当天的24时还有多少秒，返回的数据类型为整形
def get_seconds():
    now = datetime.datetime.now()
    return int((datetime.datetime(now.year, now.month, now.day, 23, 59, 59) - now).total_seconds())


# 获取当前时间戳
def get_timestamp():
    return int(time.time())


# 时间戳转为标准格式
def conver_time(timestamp=1462451334):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def getlatedate(i, str_date=''):
    if str_date == '':
        nowdate = datetime.date.today()  #
        tomorrow = nowdate + datetime.timedelta(days=i)
        return str(tomorrow)
    str_date = datetime.datetime.strptime(str_date, "%Y-%m-%d").date()
    tomorrow = str_date + datetime.timedelta(days=i)
    return str(tomorrow)


# 日期比较 返回值 为大的日期
def compare_date(str_date1, str_date2):
    str_date1 = str_date1.split(" ")[0]
    str_date2 = str_date2.split(" ")[0]
    str_date1 = datetime.datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2 = datetime.datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date() >= str_date2.date():
        return str(str_date1.date())

    return str(str_date2.date())


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


def conver_timestamp(dt="2016-05-05 20:28:54"):
    # 转换成时间数组
    timearray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timearray)
    return int(timestamp)


def jq_sy_time(carIfon):
    jqflag = syflag = 0
    insuranceType = carIfon.get("insuranceType", {})
    if isinstance(insuranceType, list):
        insuranceType = insuranceType[0]
    if insuranceType.get("compulsoryInsurance", "1") == "1":
        jqflag = 1
    if insuranceType.get("otherHurtPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("carNickPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("driverDutyPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("passengerDutyPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("carTheftPremium", "1") == "1" or \
                    insuranceType.get("engineWadingPremium", "1") == "1" or \
                    insuranceType.get("carTheftPremium", "1") == "1" or \
                    insuranceType.get("carDamagePremium", "1") == "1":
        syflag = 1

    insuranceTime = carIfon.get("insuranceTime", {})
    syStart = ""
    jqStart = ""
    syEnd = insuranceTime.get("syEnd", "")
    jqEnd = insuranceTime.get("jqEnd", "")

    endDate = carIfon.get("endDate", "")
    if jqEnd != "":
        jqStart = compare_date(jqEnd, getlatedate(1))

    if jqEnd == "" and endDate != "":
        jqStart = compare_date(endDate, getlatedate(1))
    if syEnd != "":
        syStart = compare_date(syEnd, getlatedate(1))
    if syEnd == "" and endDate != "":
        syStart = compare_date(endDate, getlatedate(1))
    if syStart == "":
        syStart = getlatedate(1)
    if jqEnd == "":
        jqStart = getlatedate(1)

    # 交强险大于40天的
    if jqflag == 1 and compare_time40(jqStart) > 41:
        return {"code": "1001", "msg": "交强险重复投保 结束日期为 %s" % jqStart, "syStart": syStart, "jqStart": jqStart}
    # 商业险大于40天的
    if syflag == 1 and compare_time40(syStart) > 41:
        return {"code": "1002", "msg": "商业险重复投保 结束日期为 %s" % syStart, "syStart": syStart, "jqStart": jqStart}

    return {"code": "1000", "msg": "成功", "syStart": syStart, "jqStart": jqStart}


if __name__ == "__main__":
    boy = {
        "licenseNo": "苏MG3950",
        "vinNo": "LZWACAGA3B4195097",
        "endDate": "",
        "CCardDetail": "小型面包车",
        "CUsageCde": "",
        "insuredName": "靖江丽人妇产医院有限公司",
        "identifyNumber": "",
        "NNewPurchaseValue": "",
        "COMPANY_ID": "中国大地财产保险股份有限公司",
        "insuredAddress": "",
        "mobile": "",
        "enrollDate": "2011-10-17",
        "brandName": "五菱牌 LZW6376NF",
        "CModelCde": "",
        "insuranceType": {
            "otherHurtPremium": {
                "Amount": "500000.00",
                "isCheck": "1"
            },
            "driverDutyPremium": {
                "Amount": "10000.00",
                "isCheck": "1"
            },
            "passengerDutyPremium": {
                "Amount": "60000.00",
                "isCheck": "1"
            },
            "carDamagePremium": "1",
            "carFireBrokenBenchMarkPremium": "0",
            "carTheftPremium": "0",
            "otherHurtBenchMarkPremium": "0",
            "carTheftBenchMarkPremium": "0",
            "engineWadingBenchMarkPremium": "0",
            "JqSumPremium": "0",
            "carNickPremium": {
                "Amount": "0",
                "isCheck": "0"
            },
            "carDamageBenchMarkPremium": "0",
            "carNickBenchMarkPremium": "0",
            "engineWadingPremium": "0",
            "passengerBenchMarkPremium": "0",
            "SySumPremium": "1669.46",
            "driverDutyBenchMarkPremium": "0",
            "carFirePremium": "0",
            "glassBrokenPremium": "0",
            "compulsoryInsurance": "0",
            "nAggTax": "0"
        },
        "NSeatNum": "7",
        "engineNo": "B04135555",
        "insuranceTime": {
            "syEnd": "2017-11-12",
            "syStart": "",
            "jqStart": "",
            "jqEnd": ""
        }
    }
    import json

    print json.dumps(jq_sy_time(boy), ensure_ascii=False)
    print compare_time40()
    print(getlatedate(-40, "2017-06-01"))
