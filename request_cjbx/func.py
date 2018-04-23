# coding:utf8
import base64

import requests
import time

#from request_cjbx.db import MysqlModel
from request_epicc.utils import pic2Str


def post_request(url, data, req_session=None, headers=None, timeout=20, verify=False):
    session = req_session if req_session else requests.Session()
    try:
        resp = session.post(url, data=data, headers=headers, timeout=timeout, verify=verify)
    except requests.exceptions.Timeout:
        print('网络连接超时')
        return
    except Exception as e:
        print('网络连接失败 - {0}'.format(e))
        return

    if resp.status_code != requests.codes.ok:
        print('网络请求错误 - {0}'.format(resp.status_code))
        return resp

    return resp


def get_request(url, req_session=None, headers=None, timeout=20, verify=False):
    session = req_session if req_session else requests.Session()
    try:
        resp = session.get(url, headers=headers, timeout=timeout, verify=verify)
    except requests.exceptions.Timeout:
        print('网络连接超时')
        return
    except Exception as e:
        print('网络连接失败 - {0}'.format(e))
        return

    if resp.status_code != requests.codes.ok:
        print('网络请求错误 - {0}'.format(resp.status_code))
        return resp

    return resp


# 获取最新的session
def get_new_session(id):
    mysql = MysqlModel()

    sql = "SELECT * FROM spard_session WHERE COMPANY_ID={0} ORDER BY CREATE_DATE DESC LIMIT 0,1".format(id)

    # mysql.execute(sql)

    session = {}
    for spard_session in mysql.fetch(sql):
        session[spard_session['COMPANY_ID']] = spard_session['SESSION']
    return session


# 根据公司id与id、序列化的session对数据库进行先删后增的操作
def update_new_session(companyId, sessionsDic):
    mysql = MysqlModel()

    sql1 = "DELETE FROM spard_session WHERE COMPANY_ID=%s"
    sql2 = "INSERT INTO `spard_session` (`COMPANY_ID`, `SESSION`) VALUES (%s, %s)"

    try:
        with mysql as db:
            db.cursor.execute(sql1, (companyId))
            for key, value in sessionsDic.items():
                db.cursor.execute(sql2, (key, value))

            db.conn.commit()
    except:
        mysql.conn.rollback()

    return


# 获取验证码
def get_yzm(TWFID):
    millis = int(round(time.time() * 1000))

    headers_3 = {
        'Accept': 'image/png, image/svg+xml, image/jxr, image/*;q=0.8, */*;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN',
        'Referer': 'https://vpn.cjbx.com.cn/web/1/http/0/88.32.0.232:88/sinoiais/',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'collection=%7Bauto_login_count%3A0%2Cpage_state%3A%27started%27%2Cneed_ist_cscm%3A%27-1%27%2CscacheUseable%3A0%2CAppCount%3A0%7D; g_LoginPage=login_psw; VisitTimes=0; haveLogin=1; ENABLE_RANDCODE=0; LoginMode=2; websvr_cookie={0}; TWFID={1}; webonly=1; allowlogin=1'.format(
            millis * 1000, TWFID),
        'Host': 'vpn.cjbx.com.cn',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
    }

    url3 = "https://vpn.cjbx.com.cn/web/0/http/1/88.32.0.232:88/sinoiais/pages/login/RandomNumUtil.jsp?d={0}".format(
        str(millis))
    print url3

    # 验证码
    r = requests.get(url3, headers=headers_3, verify=False)

    with open('3.png', 'wb') as output:
        output.write(r.content)

    code_base64 = base64.b64encode(r.content)
    codestr = pic2Str(base64.b64decode(code_base64))

    print codestr
    return codestr
