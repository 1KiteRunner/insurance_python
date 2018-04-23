# -*- coding:utf-8 -*-
import pymysql
from common import config as SE
#根据保险公司ID和序列化的session对象入库
def insert_srssion(sessionsDic):
    connection = pymysql.connect(host=SE.MYSQLHOST,
                                 user=SE.MYSQLUSER,
                                 # password='123456',
                                 password=SE.MYSQLPASSWORD,
                                 db=SE.MYSQLDB,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = "INSERT INTO `spard_session` (`COMPANY_ID`, `SESSION`) VALUES (%s, %s)"
    for key,value in sessionsDic.items():
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (key, value))
            connection.commit()
        except:
            connection.close()
    connection.close()

#根据公司id与id、序列化的session对数据库进行先删后增的操作
def updata_session(companyId,sessionsDic):
    connection = pymysql.connect(host=SE.MYSQLHOST,
                                 user=SE.MYSQLUSER,
                                 # password='123456',
                                 password=SE.MYSQLPASSWORD,
                                 db=SE.MYSQLDB,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    sql1 = "DELETE FROM spard_session WHERE COMPANY_ID=%s"
    sql2 = "INSERT INTO `spard_session` (`COMPANY_ID`, `SESSION`) VALUES (%s, %s)"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql1, (companyId))
            for key, value in sessionsDic.items():
                cursor.execute(sql2, (key, value))
        connection.commit()
    except:
        connection.rollback()
        connection.close()

#获取最新的一条session insurance/insurance
def get_session():
    connection = pymysql.connect(host=SE.MYSQLHOST,
                                 user=SE.MYSQLUSER,
                                 # password='123456',
                                 password=SE.MYSQLPASSWORD,
                                 db=SE.MYSQLDB,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM spard_session WHERE COMPANY_ID='2' ORDER BY CREATE_DATE DESC LIMIT 0,1"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    except:
        connection.close()
    sess = {}
    for spard_session in cursor.fetchall():
        sess[spard_session['COMPANY_ID']] = spard_session['SESSION']
    return sess
