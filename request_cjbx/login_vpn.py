# coding:utf8
import os
import time

import requests
from selenium import webdriver

import settings as se
from request_cjbx.func import get_request
from common.log import Logger
from request_cjbx.login_ssl import login_ssl


# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

IEdriver = "C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe"

svpn_name = "yanglei"
svpn_password = "yanglei5512115"

url = "https://vpn.cjbx.com.cn/por/login_psw.csp"

log = Logger()


def check_VPN():
    with open('cookie.txt') as f:
        TWFID = f.readline()

    print '!!!!!!', TWFID

    url = "https://vpn.cjbx.com.cn/web/1/http/0/88.32.0.232:88/sinoiais"

    headers = se.headers
    req_session = requests.session()
    req_session.headers.update(headers)

    cookie_dict = {
        "TWFID": TWFID
    }
    cookies = requests.utils.cookiejar_from_dict(cookie_dict)
    req_session.cookies = cookies

    resp = get_request(url=url, headers=headers, req_session=req_session)

    if resp and resp.status_code == '200' or resp.status_code == '502':
        return True

    else:
        return False


def killTask(name):
    for i in name:
        log.error("关闭进程")
        cmd = "taskkill /f /im %s" % i
        os.popen(cmd)
    return


def login_vpn():
    try:
        os.environ["webdriver.ie.driver"] = IEdriver
        driver = webdriver.Ie()
        driver.implicitly_wait(15)
        driver.get(url)

        # print dir(driver)
        driver.get("javascript:document.getElementById('overridelink').click();")

        try:
            al = driver.switch_to_alert()
            al.dismiss()

        except Exception, e:
            print e
        time.sleep(2)

        # print dir(driver)
        driver.execute_script('document.getElementById("svpn_name").value = "%s";' % svpn_name)
        driver.execute_script('document.getElementById("svpn_password").value = "%s";' % svpn_password)
        driver.find_element_by_xpath('//*[@id="logButton"]').click()

        cookie = driver.get_cookies()
        # print cookie
        time.sleep(20)

        for i in cookie:
            if i.get('name', '') == 'TWFID':
                global TWFID
                TWFID = i.get('value', '')
                print TWFID
                break

        with open('cookie.txt', 'w') as f:
            f.write(TWFID)
        while True:
            driver.refresh()
            time.sleep(50)

    except Exception, e:
        print e
        log.error("VPN登录异常，正在重新登录")
        return False


def check_session():
    #第二次登陆之后请求修改密码页面保持内部
    from request_cjbx.login import get_cjbx_session,login_cjbx
    headers = se.headers
    session=get_cjbx_session()
    url ="http://32.0.192.232:88/sinoiais/modifyPuTongPassword.do"
    rsp=session.get(url=url,headers=headers)
    if rsp.url==u'http://32.0.192.232:88/sinoiais/modifyPuTongPassword.do' and u"Session超时" not in  rsp.text:
        print(rsp.status_code)
        print("session is alive")

    else:
        login_cjbx()






def check_relogin():
    result = check_VPN()
    if not result:
        log.error("vpn连接异常，正在重新连接")
        killTask(["IEDriverServer.exe", "iexplore.exe", "SangforCSClient.exe"])
        result = login_vpn()
        if result:
            login_ssl()
    else:
        login_ssl()

        # else:
        #     result = check_session()
        #     if result:
        #         log.info("检测到session正常")
        #     else:
        #         log.error("session失效，正在重新登录")
        #         login()


if __name__ == "__main__":
    check_session()

