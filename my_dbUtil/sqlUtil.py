# -*- coding:utf-8 -*-
import traceback

from DB_connetion_pool import getPTConnection
from common.log import Logger

log = Logger()


def query(sql):
    results = {}
    with getPTConnection() as db:
        try:
            log.info(sql)
            db.cursor.execute(sql)
            results = db.cursor.fetchall()
            return results
            # for spard_session in results:
            #     print spard_session
            # print sess
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
            return 0


def update(sql):
    with getPTConnection() as db:
        try:
            log.info(sql)
            db.cursor.execute(sql)
            db.conn.commit()
            return 1  # 更新成功
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
            return 0  # 更新失败


def insert(sql):
    with getPTConnection() as db:
        try:
            log.info(sql)
            db.cursor.execute(sql)
            db.conn.commit()
            return 1  # 插入成功
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
            return 0  # 插入失败
