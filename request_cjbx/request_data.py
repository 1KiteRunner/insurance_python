# coding:utf8
from urllib import quote
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from parse import parse_car_detail
from common.log import Logger
import settings as se
import sys
from parse2 import parse_insuranceType

reload(sys)
log = Logger()
sys.setdefaultencoding('utf-8')
from request_cjbx.login import get_cjbx_session

headers = se.headers


# 查询车牌号
def query_car(car_num, session=None, licensetype="02"):
    url = "http://32.0.192.232:88/sinoiais/showall/query.do?dimensionSelect=03"
    if session == None:
        session = get_cjbx_session()
    car_num = quote(car_num.encode("GB2312"))
    # print car_num

    data = "queryLicensetype=&queryCredentialcode=&queryChecked=&policyNo=&vin=&licensetype={1}&carmark={0}&credentialcode=01&credentialno=&cacciid=&taccidt=&dname=&lastNo=&CheckboxGroup1=02&CheckboxGroup1=03&CheckboxGroup1=04&CheckboxGroup1=08&CheckboxGroup1=05&CheckboxGroup1=07&CheckboxGroup1=09".format(
        car_num, licensetype)
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    r = session.post(url=url, data=data, headers=headers)

    return r.text


# 查看详情
def query_detail(PLATE_NUMBER, session=None, licensetype="02"):
    if session is None:
        session = get_cjbx_session()
    if "挂" in PLATE_NUMBER:
        type = "%B9%D2%B3%B5%BA%C5%C5%C6"  # 挂车号牌
    elif licensetype == "01":
        type = "%B4%F3%D0%CD%C6%FB%B3%B5%BA%C5%C5%C6"  # 大型汽车
    else:
        type = "%D0%A1%D0%CD%C6%FB%B3%B5%BA%C5%C5%C6"  # 小型汽车
    url = "http://32.0.192.232:88/sinoiais/carowner/viewJGCarOwner.do?carmark=" + quote(
        PLATE_NUMBER.encode("gb2312")) + "&vehicletype=" + type
    r = session.get(url, headers=headers)
    html = r.text
    data = parse_car_detail(html)
    if data != 0:
        # del_car(PLATE_NUMBER)
        # sql_add_car2(data)
        return data
    else:
        return 0


# 保单号 查询保险组合
def policy_info(policyno, session=None):
    try:
        if session is None:
            session = get_cjbx_session()
        url = "http://32.0.192.232:88/sinoiais/insurance/viewIAPMMain.do?riskType=2&confirmSequenceNo=" + policyno
        r = session.get(url, headers=headers)
        return parse_insuranceType(r.text)
    except Exception as e:
        log.error(e)
        import traceback
        log.error(traceback.format_exc())
        return {}


if __name__ == "__main__":
    import re
    import json

    session = get_cjbx_session()
    ss = policy_info('V0201PAIC320017001489495565156', session)

    print json.dumps(ss, ensure_ascii=False)
