# -*- coding:utf-8 -*-
__author__ = 'weikai'
from Tkinter import *
import tkMessageBox
import os
PATH = 'C:\Python27\\'


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        # self.nameInput.pack()
        self.alertButton = Button(self, text='scheduler', command=self.scheduler)
        self.alertButton.pack()
        self.alertButton = Button(self, text='plateNoQueue', command=self.plateNoQueue)
        self.alertButton.pack()
        self.alertButton = Button(self, text='realtimeQueue', command=self.realtimeQueue)
        self.alertButton.pack()
        #self.alertButton = Button(self, text='stomp_cicc_client', command=self.stomp_cicc_client)
        #self.alertButton.pack()
        #self.alertButton = Button(self, text='stomp_client', command=self.stomp_client)
        #self.alertButton.pack()
        #self.alertButton = Button(self, text='stomp_epicc_client', command=self.stomp_epicc_client)
        #self.alertButton.pack()
        #self.alertButton = Button(self, text='stomp_cic_client', command=self.stomp_cic_client)
        #self.alertButton.pack()
        self.alertButton = Button(self, text='CjbxNoQueue', command=self.CjbxNoQueue)
        self.alertButton.pack()
        self.alertButton = Button(self, text='CjbxKeepSession', command=self.CjbxKeepSession)
        self.alertButton.pack()
        self.alertButton = Button(self, text='startall', command=self.start_all)
        self.alertButton.pack()
        self.alertButton = Button(self, text='stopall', command=self.stop_all)
        self.alertButton.pack()
    def start_all(self):
        #os.system("start  python Scheduler/scheduler.py")
        os.system("start  python %sScheduler\scheduler.py" % PATH)
        os.system("start  python %sScheduler\plateNoQueue.py" % PATH)
        os.system("start  python %sScheduler\\realtimeQueue.py" % PATH)
        os.system("start  python %sScheduler\stomp_cic_client.py" % PATH)
        os.system("start  python %sScheduler\stomp_cicc_client.py" % PATH)
        os.system("start  python %sScheduler\stomp_client.py" % PATH)
        os.system("start  python %sScheduler\stomp_epicc_client.py" % PATH)
    def scheduler(self):
        os.system("start  python %sScheduler\scheduler.py" % PATH)
    def plateNoQueue(self):
        os.system("start  python %sScheduler\plateNoQueue.py" % PATH)
    def realtimeQueue(self):
        os.system("start  python %sScheduler\\realtimeQueue.py" % PATH)
    def stomp_cic_client(self):
        os.system("start  python %sScheduler\stomp_cic_client.py" % PATH)
    def stomp_cicc_client(self):
        os.system("start  python %sScheduler\stomp_cicc_client.py" % PATH)
    def stomp_client(self):
        os.system("start  python %sScheduler\stomp_client.py" % PATH)
    def CjbxNoQueue(self):
        os.system("start  python %srequest_cjbx\CjbxNoQueue.py" % PATH)
    def CjbxKeepSession(self):
        os.system("start  python %srequest_cjbx\scheduler.py" % PATH)
    def stomp_epicc_client(self):
        os.system("start  python %sScheduler\stomp_epicc_client.py" % PATH)
    def stop_all(self):
        os.system("taskkill /f /im python.exe")

if __name__ == "__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('start')
    # 主消息循环:
    app.master.geometry('300x300')
    app.mainloop()
