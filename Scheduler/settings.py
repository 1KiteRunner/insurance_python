# -*- coding:utf-8 -*-
import os
import traceback

from common.log import Logger

log = Logger()

__author__ = 'weikai'
PICC_QUEUE='/queue/PICC_QUEUE'
CHINA_CONTINENT_QUEUE='/queue/CHINA_CONTINENT_QUEUE'
CHINA_JOINT_QUEUE='/queue/CHINA_JOINT_QUEUE'
QUEUE = '/queue/FILL_UP_QUEUE'
BATCH_PROCESS_QUEUE='BATCH_PROCESS_QUEUE'
REAL_TIME_QUEUE="REAL_TIME_QUEUE"
COMPLETE_FLAG = "/queue/COMPLETE_FLAG"
COMPLETE_PLATE_NUMBER="/queue/COMPLETE_PLATE_NUMBER"
EPICC_PLATE_NUMBER="EPICC_PLATE_NUMBER"
CJBX_PLATE_NUMBER="/queue/CJBX_PLATE_NUMBER"
ANCHENG_PLATE_NUMBER="/queue/ANCHENG_PLATE_NUMBER"

#批量队列
BATCH_COMPLETE_FLAG="BATCH_COMPLETE_FLAG"#是否能补全信息队列
BATCH_CIC_QUEUE="/queue/BATCH_CIC_QUEUE"
BATCH_CICC_QUEUE="/queue/BATCH_CICC_QUEUE"
BATCH_PINGAN_QUEUE="/queue/BATCH_PINGAN_QUEUE"
BATCH_EPICC_QUEUE="BATCH_EPICC_QUEUE"
EPICC_BATCH_REPAIR_QUEUE="EPICC_BATCH_REPAIR_QUEUE"
BATCH_ANCHENG_QUEUE="/queue/BATCH_ANCHENG_QUEUE"
'''
MQIP='127.0.0.1'
MQPORT=61613
MQHOST='tcp://127.0.0.1:61613'
'''
'''
MQIP='118.178.232.65'
MQPORT=61613
MQHOST='tcp://118.178.232.65:61613'




MQIP='99.48.70.162'
MQPORT=61613
MQHOST='tcp://99.48.70.162:61613'
'''
#65内网IP
'''
MQIP='10.27.229.102'
MQPORT=61613
MQHOST='tcp://10.27.229.102:61613'
'''
MQIP='10.0.1.233'
MQPORT=61613
MQHOST='tcp://10.0.1.233:61613'


# 开发环境
class Production:
    MQIP = '10.0.1.233'
    MQPORT = 61613
    MQHOST = 'tcp://10.0.1.233:61613'


# 本地测试
class Local:
    MQIP = '127.0.0.1'
    MQPORT = 61613
    MQHOST = 'tcp://127.0.0.1:61613'


def import_string(import_name):
    try:
        module_name, obj_name = import_name.rsplit('.', 1)
        module = __import__(module_name, None, None, [obj_name])
        return getattr(module, obj_name)
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


# 通过环境变量来进行配置切换

try:
    env = os.environ.get('NAN_MI', None)
except Exception as e:
    env = None

if not env:
    env = 'Local'


if env not in ['Local', 'Production']:
    raise EnvironmentError('The environment variable (NANMI) is invalid ')

i_config = import_string('Scheduler.settings.{0}'.format(env))

if __name__ == '__main__':
    print i_config.MQIP
