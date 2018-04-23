# -*- coding:utf-8 -*-
import datetime

CMonDespRate = {
    '302001001': '0.0060',
    '302001008': '0.0060',
    '302001003': '0.0090',
    '302001011': '0.0090',
    '302001016': '0.0090'
}


# 第一个参数注册时间
# 第二个参数新车购置价格
# 第三个参数车辆类型(商)
def calcNActualValue(CFstRegYm, NNewPurchaseValue, CVhlTyp):
    lvCarkindcode1 = CMonDespRate[CVhlTyp]
    enrollDate = datetime.datetime.strptime(CFstRegYm, "%Y-%m-%d").date()
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    endD = tomorrow.day
    endM = tomorrow.month
    endY = tomorrow.year
    startD = enrollDate.day
    startM = enrollDate.month
    startY = enrollDate.year
    if endD >= startD:
        month = (endY - startY) * 12 + (endM - startM)
    else:
        month = (endY - startY) * 12 + (endM - startM) - 1;
    allDiscount = float(lvCarkindcode1) * int(month)
    #print(allDiscount)
    if allDiscount > 0.8:
        allDiscount = 0.8
    realPrice = round(float(float(NNewPurchaseValue) - float(NNewPurchaseValue) * allDiscount), 2)
    return '%.2f' % realPrice


if __name__ == "__main__":
    print type(calcNActualValue('2011-01-11', 268000, '302001001'))
