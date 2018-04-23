# -*- coding:utf-8 -*-
__author__ = 'weikai'
from request_cic.request_getdata import renewal_data
from request_cic.CicRenewalBody import getLastPlyByVhl, get_insurance_info
from request_cic.utils import getlatedate


# 车牌号获取续保用户信息入口
def cic_entrance_renwal(requestcic, CPlateNo):
    try:
        dts = renewal_data(requestcic, CPlateNo=CPlateNo)
        if dts != 0:
            jq_plyNo = getLastPlyByVhl(requestcic, CPlyNo=dts['CPlyNo'])
            dts['jq_plyNo'] = jq_plyNo
            dts['sy_plyNo'] = CPlyNo = dts['CPlyNo']
            user = get_insurance_info(requestcic, dts)
            # user['endDate']=dts['TInsrncEndTm'].split(" ")[0] #保险结束时间
            # 修改问题  2017-03-09 ：中华联合返回的数据为 日期 23:59:59  加一天为启保时间
            user['endDate'] = getlatedate(1, str_date=dts['TInsrncEndTm'].split(" ")[0])
            user["COMPANY_ID"] = "4"
            return user
        return 0
    except Exception as e:
        print(e)
        return 0
