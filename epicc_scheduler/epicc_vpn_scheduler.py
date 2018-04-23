# -*- coding: utf8 -*-
__author__ = 'wk'
from apscheduler.schedulers.blocking import BlockingScheduler
import traceback
import time
import os
from request_epicc_vpn.login import check_relogin
import logging
logging.basicConfig()

# 任务调度模块
#参考http://debugo.com/apscheduler/

if __name__ == '__main__':

    scheduler = BlockingScheduler()
    scheduler.add_job(check_relogin, 'interval', minutes=5)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except Exception as e:
        print(traceback.format_exc())
        # scheduler.shutdown()
