# -*- coding:utf-8 -*-
import datetime
discount_month = {
    '00':'0.0090',
    '01': '0.0110',
    '02': '0.0060',
    '03': '0.0060',
    '10': '0.0090',
    '11': '0.0110',
    '13': '0.0090',
    '20': '0.0090',
    '21': '0.0110',
    '23': '0.0090',
    '30': '0.0090',
    '31': '0.0110',
    '32': '0.0060',
    '33': '0.0090',
    '40': '0.0140',
    '41': '0.0140',
    '43': '0.0110',
    '50': '0.0090',
    '51': '0.0110',
    '53': '0.0090',
    '60': '0.0110',
    '61': '0.0110',
    '63': '0.0090',
    '70': '0.0110',
    '71': '0.0110',
    '73': '0.0090',
    '80': '0.0090',
    '81': '0.0110',
    '82': '0.0060',
    '83': '0.0090',
    '90': '0.0090',
    '91': '0.0110'
}
def getDisCountRatebyMonth(code):
    fee = 0;
    try:
        fee = discount_month[code]
        return fee
    except:
        return fee
def calculateActualValue(cost,useNatureCode,seatCount,vehicleKind,lvCarkindcode1,enrollDate,today=""):
    if vehicleKind=='A0':
        if int(seatCount) > 9:
            lvCarkindcode1  = "1"; # 这里可能有问题 应为第一个符赋值
        else:
            lvCarkindcode1 = "0";
    if useNatureCode=="82":#出租租赁
        lvCarkindcode1 = lvCarkindcode1 + "1"
    elif useNatureCode=="85":#家庭自用
        lvCarkindcode1 = lvCarkindcode1 + "2"
    elif useNatureCode=="84":#非营业用
        lvCarkindcode1 = lvCarkindcode1 + "3"
    else:#其他
        lvCarkindcode1 = lvCarkindcode1 + "0"
    fee = getDisCountRatebyMonth(lvCarkindcode1)
    enrollDate = datetime.datetime.strptime(enrollDate, "%Y-%m-%d").date()
    if today=="":
        today = datetime.date.today()
    endD = today.day+1
    endM = today.month
    endY = today.year
    startD = enrollDate.day
    startM = enrollDate.month
    startY = enrollDate.year
    if endD >= startD:
        month = (endY - startY) * 12 + (endM - startM)
    else:
        month = (endY - startY) * 12 + (endM - startM) - 1;
    allDiscount = float(fee) * int(month)
    if allDiscount > 0.8:
        allDiscount = 0.8
    realPrice = int(float(cost) - float(cost) * allDiscount)
    return realPrice

if __name__ =='__main__':
    print calculateActualValue("160000",'85',5,'A0','',"2007-06-06",today=datetime.datetime.strptime("2017-05-11", "%Y-%m-%d"))
