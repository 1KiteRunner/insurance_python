# -*- coding:utf-8 -*-
import datetime


# 需要两个参数  第一个是商业险的开始时间  第二个是车辆的注册时间
def get_user_years(startDate, enrollDate):
    userYear = '0'
    enrollDate = datetime.datetime.strptime(enrollDate, "%Y-%m-%d").date()
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    startD = startDate.day
    startM = startDate.month
    startY = startDate.year
    endD = enrollDate.day
    endM = enrollDate.month
    endY = enrollDate.year
    yearGap = startY - endY
    monthGap = startM - endM
    dayGap = startD - endD
    if yearGap == 0:
        if monthGap < 11:
            userYear = '0'
        elif dayGap >= 0:
            userYear = '1'
        else:
            userYear = '0'
    elif yearGap == 1:
        if monthGap + 12 < 11:
            userYear = '0'
        elif monthGap + 12 == 11:
            if dayGap >= 0:
                userYear = '1'
            else:
                userYear = '0'
        else:
            userYear = '1'
    elif yearGap >= 2:
        if monthGap < 0:
            userYear = str(yearGap - 1)
        elif monthGap == 0:
            if dayGap >= 0:
                userYear = str(yearGap)
            else:
                userYear = str(yearGap - 1)
        else:
            userYear = str(yearGap)

    return userYear

codeMap = {
    '0': '345020001',
    '1': '345020002',
    '2': '345020003',
    '3': '345020004',
}

PHCC_VHL_USEYEAR_MAP = {
    '0': '345003007',
    '1': '345003007',
    '2': '345003008',
    '3': '345003008',
    '4': '345003009',
    '5': '345003009',
    '6': '345003010',
}

JQ_PHCC_VHL_USEYEAR_MAP = {
    '0': '345011001',
    '1': '345011002',
    '2': '345011002',
    '3': '345011003',
    '4': '345011003',
    '5': '345011004',
    '6': '345011004',
    '7': '345011004',
    '8': '345011005',
}


if __name__ == "__main__":
    #print calc_user_years("2017-03-27", "2016-04-01")
    pass
