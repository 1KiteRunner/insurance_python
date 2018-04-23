# -*- coding:utf-8 -*-
__author__ = 'weikai'
import sys, traceback
from common.mongodb.mongoUtils import mg_find, mg_update_insert
from my_dbUtil.sql.optionslist import car_type
from common.log import Logger
from request_cjbx.start import parse_body
from common.timeUtil import get_timestamp
reload(sys)
sys.setdefaultencoding('utf8')
log = Logger()


# ,"BODY.UPDATE_TIME":{'$let':1492481155}
def query_user_renewal(PLATE_NUMBER):
    try:
        # 查询一周内可用的数据用户数据
        mydate = mg_find("renrwalInfo", {"BODY.licenseNo": PLATE_NUMBER})
        if mydate != None and len(mydate) > 0:
            # 查询7天内存在的数据
            if mydate.get("UPDATE_TIME", 0) > (get_timestamp() - 604800):
                return mydate
            else:
                return 0
        else:
            return 0
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0


def inser_user_renewal(dt):
    '''
    :param dt:{"licenseNo": "苏AN0Q83", "vinNo": "LVTDB14B7FC003044", "endDate": "2017-01-27", "CCardDetail": "K33", "brandName": "奇瑞SQR6451T217", "insuredName": "熊飞", "identifyNumber": "321183198903103659", "CUsageCde": "309001", "NNewPurchaseValue": "80910.00", "COMPANY_ID": "4", "insuredAddress": "句容市", "mobile": "13921551352", "enrollDate": "2015-01-29", "engineNo": "TAEM02094", "CModelCde": "QRAAFD0105", "NSeatNum": "5"}
    :return:
    '''
    try:
        # dt['licenseNo']=dt['plateNumber']
        licenseNo = dt.get('licenseNo', '')
        plateNumber = dt.get('plateNumber', '')
        No = ''
        if licenseNo != '':
            No = licenseNo
        else:
            No = plateNumber

        dt['UPDATE_TIME'] = get_timestamp()
        mg_update_insert('renrwalInfo', {"BODY.licenseNo": No}, dt)
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


def query_user_permium_time(PLATE_NUMBER):
    try:
        mydata = mg_find("InsuranceInfo", {'BODY.PALTE_NO': PLATE_NUMBER})
        if mydata != None and len(mydata) > 0:
            out = parse_body(mydata)
            out['CCardDetail'] = car_type[out['CCardDetail'].encode()]
            return out
        else:
            return 0
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0


if __name__ == "__main__":
    dt = {
        "licenseNo": "苏AN0Q84",
        "vinNo": "LVTDB14B7FC003044",
        "endDate": "2017-01-27",
        "CCardDetail": "K33",
        "brandName": "奇瑞SQR6451T217",
        "insuredName": "熊飞",
        "identifyNumber": "321183198903103659",
        "CUsageCde": "309001",
        "NNewPurchaseValue": "80910.00",
        "COMPANY_ID": "4",
        "insuredAddress": "句容市",
        "mobile": "13921551352",
        "enrollDate": "2015-01-29",
        "engineNo": "TAEM02094",
        "CModelCde": "",
        "NSeatNum": "5"}
    # inser_user_renewal(dt)
    # a=query_user_renewal("苏AB1P05")
    # b = {field: a.get(field, '').decode() for field in a if isinstance(a.get(field, ''), str)}
    # del_user_renewal("苏AN0Q83")
    # print json.dumps(query_user_permium_time('苏A5112D'), ensure_ascii=False)
    query_user_renewal('苏A5112D')
