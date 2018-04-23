# -*- coding: utf8 -*-
__author__ = 'wk'
from apscheduler.schedulers.blocking import BlockingScheduler
import traceback
import time
import os
from  login_vpn import check_session
import logging
logging.basicConfig()

# 任务调度模块
#参考http://debugo.com/apscheduler/

if __name__ == '__main__':

    scheduler = BlockingScheduler()
    scheduler.add_job(check_session, 'interval', minutes=1)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except Exception as e:
        print(traceback.format_exc())
        # scheduler.shutdown()
