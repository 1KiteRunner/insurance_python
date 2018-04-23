# -*- coding:utf-8 -*-
#根据进程名杀死进程
import sys,os
def kill_process_by_name(name):
    cmd = "taskkill /f /im %s" % name
    f = os.popen(cmd)
    return
if __name__ == "__main__":
    if len(sys.argv) == 1:
        name=raw_input("plz input the process name which you want to kill :")
    else:
        name=sys.argv[1]
    kill_process_by_name(name)