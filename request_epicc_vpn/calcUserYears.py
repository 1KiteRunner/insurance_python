# -*- coding:utf-8 -*-
import datetime
def calc_user_years(startDate,enrollDate):
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
        if monthGap<11:
           return '0'
        elif dayGap>=0:
            return '1'
        else:
            return '0'
    elif yearGap == 1:
        if monthGap + 12 < 11:
            return '0'
        elif monthGap + 12 == 11:
            if dayGap>=0:
                return '1'
            else:
                return '0'
        else:
            return '1'
    elif yearGap >= 2:
        if monthGap < 0:
            return str(yearGap-1)
        elif monthGap == 0:
            if dayGap >= 0:
                return str(yearGap)
            else:
                return str(yearGap-1)
        else:
            return str(yearGap)

if __name__=="__main__":
    print calc_user_years('2017-05-09','2013-05-13')