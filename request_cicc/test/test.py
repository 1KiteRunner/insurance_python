#-*-encoding=utf-8-*-
# multiprocessing.py
from multiprocessing import Process
import os
import time
import datetime
from multiprocessing import Pool
import os, time, random
# 子进程要执行的代码
def run_proc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())
    time.sleep(1)

def testProess():
    time = datetime.datetime.now()
    print 'Parent process %s.' % os.getpid()
    p4 = Process(target=run_proc, args=('test',))
    p3 = Process(target=run_proc, args=('test',))
    p2 = Process(target=run_proc, args=('test',))
    p1 = Process(target=run_proc, args=('test',))
    p = Process(target=run_proc, args=('test',))
    print 'Process will start.'
    p.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    print 'Process end.'+str(datetime.datetime.now()-time)

def long_time_task(name):
    print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print 'Task %s runs %0.2f seconds.' % (name, (end - start))

def testProssPoll():
    print 'Parent process %s.' % os.getpid()
    p = Pool(5)
    for i in range(9):
        p.apply_async(long_time_task, args=(i,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
if __name__=="__main__":
    testProssPoll()