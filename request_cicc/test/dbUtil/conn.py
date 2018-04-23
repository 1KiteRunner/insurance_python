# -*- coding:utf-8 -*-
from my_dbUtil.DB_connetion_pool import getPTConnection;

def TestMySQL():
    #申请资源
    with getPTConnection() as db:
        # SQL 查询语句;
        # sql = "SELECT * FROM spard_session WHERE COMPANY_ID IN (4,5) AND CREATE_DATE >=(SELECT NOW()- INTERVAL 60*20 SECOND)ORDER BY CREATE_DATE DESC LIMIT 0,2";
        # sql = "SELECT * FROM car_premium WHERE PREMIUM_ID='15209'"
        sql = "UPDATE car_premium11 SET BAO_E='12312323' WHERE PREMIUM_ID='15209'"
        connection = db.conn
        try:
            # 获取所有记录列表
            connection.cursor.execute(sql)
            # connection.commit()
            # print 1/0
            # results = db.cursor.fetchall();
            # sess = {}

            # for spard_session in results:
            #     print spard_session
            # print sess
        except:
            print 111
            connection.rollback()

TestMySQL()