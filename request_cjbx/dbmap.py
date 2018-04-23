# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import sys

from common.log import Logger

reload(sys)
sys.setdefaultencoding('utf8')
from my_dbUtil.sqlUtil import insert,update
reload(sys)
log=Logger()
sys.setdefaultencoding('utf-8')

'''
def sql_add_car(cardata):
    session = None
    try:
        session = sessionmaker(bind=ENGINE)()
        new_data = VehicleInfo(**cardata)
        session.merge(new_data)
        session.commit()
        return 1
    except Exception as e:
        log.error(traceback.format_exc())
        log.error(e)
        return 0
    #finally:
     #   if session:
      #      session.close()

def sql_add_usercompay(userdata):
    session = None
    try:
        session = sessionmaker(bind=ENGINE)()
        new_data = UserCompany(**userdata)
        session.merge(new_data)
        session.commit()
        return 1
    except Exception as e:
        log.error(traceback.format_exc())
        log.error(e)
        return 0
    #finally:
     #   if session:
      #      session.close()
'''
def sql_add_car2(dt):
    SQL="INSERT INTO vehicle_info(CUST_NAME,PLATE_NUMBER,FRAME_NUMBER,VEHICLE_TYPE,VEHICLE_MODEL,ENGLISH_BRAND,VEHICLE_USE,VEHICLE_STATE,SEATING_CAPACITY,LATEST_INSPECTION_DATE,INSPECTION_VALID_DATE,ENERGY_TYPES,PLATE_TYPE,ENGINE_NUMBER,INITIAL_REGISTRATION_DATE,BODY_COLOR,CHINESE_BRAND,TRANSFER_DATE,MANUFACTURER,APPROVED_LOAD,DISPLACEMENT,TRACTION_MASS,CURB_WEIGHT)VALUES" \
        "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (dt.get('CUST_NAME',''),
dt.get('PLATE_NUMBER',''),
dt.get('FRAME_NUMBER',''),
dt.get('VEHICLE_TYPE',''),
dt.get('VEHICLE_MODEL',''),
dt.get('ENGLISH_BRAND',''),
dt.get('VEHICLE_USE',''),
dt.get('VEHICLE_STATE',''),
dt.get('SEATING_CAPACITY',''),
dt.get('LATEST_INSPECTION_DATE',''),
dt.get('INSPECTION_VALID_DATE',''),
dt.get('ENERGY_TYPES',''),
dt.get('PLATE_TYPE',''),
dt.get('ENGINE_NUMBER',''),
dt.get('INITIAL_REGISTRATION_DATE',''),
dt.get('BODY_COLOR',''),
dt.get('CHINESE_BRAND',''),
dt.get('TRANSFER_DATE',''),
dt.get('MANUFACTURER',''),
dt.get('APPROVED_LOAD',''),
dt.get('DISPLACEMENT',''),
dt.get('TRACTION_MASS',''),
dt.get('CURB_WEIGHT',''))
    out = insert(SQL)
    return out

def del_car(PLATE_NUMBER):
    sql="DELETE FROM vehicle_info WHERE PLATE_NUMBER ='%s'" % PLATE_NUMBER
    sql2="DELETE FROM user_permium_time WHERE palte_number = '%s'"% PLATE_NUMBER
    out=update(sql)
    out=update(sql2)
    return out

def sql_add_usercompay2(dt):
    SQL="INSERT INTO user_permium_time (palte_number, company_id, toubao_time, start_time, end_time, permium_id) VALUES('%s','%s','%s','%s','%s','%s')" %(
        dt.get('palte_number',''),
dt.get('company_id',''),
dt.get('toubao_time',''),
dt.get('start_time',''),
dt.get('end_time',''),
dt.get('permium_id','')
    )
    out = insert(SQL)
    return out