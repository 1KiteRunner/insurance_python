# coding:utf8
from sqlalchemy import Column, String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 车主用户信息
class VehicleInfo(Base):
    __tablename__ = 'vehicle_info'

    FRAME_NUMBER = Column(String, primary_key=True)  # 车架号
    CUST_NAME = Column(String)  # 车主名称
    PLATE_NUMBER = Column(String)  # 车牌号码
    VEHICLE_TYPE = Column(String)  # 车辆类型代码
    VEHICLE_MODEL = Column(String)  # 车辆型号
    ENGLISH_BRAND = Column(String)  # 英文品牌
    VEHICLE_USE = Column(String)  # 车辆使用性质代码
    VEHICLE_STATE = Column(String)  # 机动车状态代码
    SEATING_CAPACITY = Column(String)  # 核定载客人数
    LATEST_INSPECTION_DATE = Column(String)  # 最近定检日期
    INSPECTION_VALID_DATE = Column(String)  # 检验有效日期止
    ENERGY_TYPES = Column(String)  # 能源种类
    PLATE_TYPE = Column(String)  # 号牌种类代码
    ENGINE_NUMBER = Column(String)  # 发动机号
    INITIAL_REGISTRATION_DATE = Column(String)  # 车辆初始登记日期
    BODY_COLOR = Column(String)  # 车身颜色代码
    CHINESE_BRAND = Column(String)  # 中文品牌
    TRANSFER_DATE = Column(String)  # 转移登记日期
    MANUFACTURER = Column(String)  # 制造厂名称
    APPROVED_LOAD = Column(String)  # 核定载质量
    DISPLACEMENT = Column(String)  # 排量
    TRACTION_MASS = Column(String)  # 准牵引总质量
    CURB_WEIGHT = Column(String)  # 整备质量



class UserCompany(Base):
    __tablename__='user_permium_time'
    palte_number=Column(String, primary_key=True)
    company_id=Column(String)
    toubao_time=Column(String)
    start_time=Column(String)
    end_time=Column(String)
    permium_id=Column(String)

