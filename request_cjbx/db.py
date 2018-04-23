# coding:utf8
import traceback

import pymysql
from sqlalchemy import create_engine
from DBUtils.PooledDB import PooledDB
# sqlalchemy连接池
#from request_cjbx.settings import config

ENGINE = create_engine('mysql+mysqlconnector://insurance:insurance@120.55.189.14:3306/insurance', pool_size=10, echo=True, echo_pool=True,
                       pool_recycle=3600)

