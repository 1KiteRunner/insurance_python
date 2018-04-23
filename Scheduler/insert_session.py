# -*- coding:utf-8 -*-
import pymysql
"""
插入序列化session方法，需要的参数是由保险公司ID作为key，session值作为value的一个字典
"""
def insert_srssion(sessionsDic):
    connection = pymysql.connect(host='120.55.189.14',
                                 user='insurance',
                                 # password='123456',
                                 password='insurance',
                                 db='insurance',
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

"""
获取最新session方法，需要保险公司id组成的数组作为参数
"""
def get_session(companyids):
    connection = pymysql.connect(host='120.55.189.14',
                                 user='insurance',
                                 # password='123456',
                                 password='insurance',
                                 db='insurance',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM spard_session WHERE COMPANY_ID IN %s AND CREATE_DATE >=(SELECT NOW()- INTERVAL 60*20 SECOND) ORDER BY CREATE_DATE DESC LIMIT 0,%d"
    sql_condition = "("
    for i in companyids:
        sql_condition = sql_condition + "'"+i +"'"+ ","
    sql_condition = sql_condition[0:-1] + ")"
    sql = sql % (sql_condition, len(companyids))
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    except:
        connection.close()
    finally:
        connection.close()
    sess={}
    for spard_session in cursor.fetchall():
        sess[spard_session['COMPANY_ID']]=spard_session['SESSION']
    #print sess
    return sess

def del_session():
    connection = pymysql.connect(host='120.55.189.14',
                                 user='insurance',
                                 # password='123456',
                                 password='insurance',
                                 db='insurance',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = " DELETE FROM spard_session WHERE	 CREATE_DATE < DATE_SUB(NOW(), INTERVAL 1 HOUR) AND COMPANY_ID =4 OR COMPANY_ID =5 OR COMPANY_ID=1 "

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        return 1
    except:
        return 0
        connection.close()
    finally:
        connection.close()



if __name__=="__main__":
#     session={
#         "cic":"11111111",
#         "cicc":"1222222222"
#     }
    companyids = ["4","5"]
    print del_session()
    # insert_srssion(session)
