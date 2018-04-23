# -*- coding: utf8 -*-
__author__ = 'wk'
from apscheduler.schedulers.blocking import BlockingScheduler
import traceback
import os
from Scheduler.SessionKeep.keepSession import keep_alive_session


# 任务调度模块
# 参考http://debugo.com/apscheduler/

if __name__ == '__main__':

    scheduler = BlockingScheduler()
    # scheduler.add_job(tick,'cron', second='*/30', hour='*')
    scheduler.add_job(keep_alive_session, 'interval', minutes=2)
    # scheduler.add_job(keep_flow, 'interval', minutes=1)
    # scheduler.add_job(check_relogin, 'interval', minutes=5)
    # 删除session
    # scheduler.add_job(del_session, 'interval', hours=10)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except Exception as e:
        print(traceback.format_exc())
        # scheduler.shutdown()
