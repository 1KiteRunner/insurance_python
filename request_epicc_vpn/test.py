# -*- coding:utf-8 -*-
import time
from driverLogin import Singleton

name = 'nanj-617'
pwd = '201701'

name2 = 'A320100906'
pwd2 = 'c464465851'

driver = Singleton().driver
driver.implicitly_wait(15)
url = "https://vpn.piccjs.com/remote-sale"
login_url = 'https://vpn.piccjs.com/prx/000/http/10.134.136.112/portal'
driver.get(url)
driver.get("javascript:document.getElementById('overridelink').click();")
try:
    driver.switch_to_alert().accept()
except Exception, e:
    print e
time.sleep(2)
driver.execute_script('document.getElementById("uname").value = "%s";' % name)
driver.execute_script('document.getElementById("pwd").value = "%s";' % pwd)
driver.find_element_by_xpath('//*[@id="loginbtn"]').click()
time.sleep(15)
try:
    driver.switch_to_alert().accept()
except Exception, e:
    print e
driver.get(login_url)
driver.get("javascript:document.getElementById('overridelink').click();")
driver.execute_script('document.getElementById("username1").value = "%s";' % name2)
driver.execute_script('document.getElementById("password1").value = "%s";' % pwd2)
driver.find_element_by_xpath('//*[@id="button"]').click()
driver.get("http://10.134.136.112:8000/prpall/index.jsp?calogin")
driver.switch_to.frame('main')
driver.switch_to.frame('page')

# driver2 = Singleton()
# url = "https://vpn.piccjs.com/remote-sale"
# driver2.driver.get(url)
# driver2.driver.quit()
# driver2.instance=None
# print driver2.driver
