# -*- coding:utf-8 -*-
__author__ = 'weikai'

import time
import datetime
import threading
from request_epicc.interface import isRenewal
# def add(a):
#     print("%d" % (time.time() * 1000))
#     time.sleep(15)
#     print(a)
#     return a
#
# def execFun(arg):
#     try:
#         print "脚本%s开始运行%s" % (arg,datetime.datetime.now())
#         add(arg)
#         print "脚本%s结束运行%s" % (arg,datetime.datetime.now())
#     except Exception, e:
#         print '%s\t 运行失败,失败原因\r\n%s' % (arg,e)

def threadpool(args):
    #args={"userlist":[{"insuredPhNo":"18251867797","EngineNo":"1405110930","VEHICLE_MODELSH":"哈弗牌CC6460RM01","insuredIDNumber":"320125198711304822","carddate":"2014-12-29","address":"溧水区永阳镇中山东路290号1栋4号","insuredName":"王秋兰","LicenseNo":"苏AQ6C06","regisdate":"2014-12-29","FrameNo":"LGWEF4A56EF280301"},{"insuredPhNo":"18761529057","EngineNo":"3127348","VEHICLE_MODELSH":"马自达牌CAM7150M5","insuredIDNumber":"32012419910417303X","carddate":"2014-12-24","address":"溧水区晶桥镇邰村荷塘村15号","insuredName":"周式华","LicenseNo":"苏AB9N35","regisdate":"2014-12-24","FrameNo":"LVRHDFML8EN340221"},{"insuredPhNo":"17092589038","EngineNo":"KL1392","VEHICLE_MODELSH":"北京牌BJ7150C5E2","insuredIDNumber":"320125198610093122","carddate":"2014-12-26","address":"南京市高淳区漆桥镇老庄山76号","insuredName":"杨小香","LicenseNo":"苏AB3Q98","regisdate":"2014-12-26","FrameNo":"LNBSCCAH3EF031577"},{"insuredPhNo":"15851844024","EngineNo":"JL478QEA EC4M139626","VEHICLE_MODELSH":"长安牌SC7169B5","insuredIDNumber":"320122198710232434","carddate":"2014-12-11","address":"南京市浦口区桥林街道林东村林东社区","insuredName":"成磊","LicenseNo":"苏AK8A77","regisdate":"2014-12-11","FrameNo":"LS5A2ABE6EA175199"},{"insuredPhNo":"18721338102","EngineNo":"143120893","VEHICLE_MODELSH":"别克牌SGM7162DMAB","insuredIDNumber":"320125198901030711","carddate":"2014-12-18","address":"南京市高淳区砖墙镇大涵村万家65号","insuredName":"万立顺","LicenseNo":"苏AB0Q87","regisdate":"2014-12-18","FrameNo":"LSGPB54U3FD057155"},{"insuredPhNo":"18068329197","EngineNo":"142410788","VEHICLE_MODELSH":"别克牌SGM7161EAA2","insuredIDNumber":"320282198808156611","carddate":"2014-12-2","address":"江苏省宜兴市和桥镇闸口村张家村68号","insuredName":"钱波","LicenseNo":"苏B768TD","regisdate":"2014-12-2","FrameNo":"LSGGA54E4EH287001"},{"insuredPhNo":"13913355531","EngineNo":"EW606024","VEHICLE_MODELSH":"北京现代牌BH6440LAY","insuredIDNumber":"320123197511253445","carddate":"2014-12-30","address":"六合区横梁街道王子路30-9号","insuredName":"胡秀兰","LicenseNo":"苏AB1P05","regisdate":"2014-12-30","FrameNo":"LBELMBKC0EY555590"},{"insuredPhNo":"18761636737","EngineNo":"142493753","VEHICLE_MODELSH":"雪佛兰牌SGM7150DMAA","insuredIDNumber":"320125199003223321","carddate":"2014-12-29","address":"溧水区和凤镇双牌石八建公司楼2栋202室","insuredName":"张金香","LicenseNo":"苏AB2R68","regisdate":"2014-12-29","FrameNo":"LSGPC52H2FF017611"},{"insuredPhNo":"15952096020","EngineNo":"14096911","VEHICLE_MODELSH":"东风牌DXK6440AF3","insuredIDNumber":"320123198608064020","carddate":"2014-12-30","address":"六合区金牛湖街道八百大道288-5号","insuredName":"王仁霞","LicenseNo":"苏AB0P61","regisdate":"2014-12-30","FrameNo":"LVZA43F93EC554224"},{"insuredPhNo":"15951683827","EngineNo":"E10E19284","VEHICLE_MODELSH":"北京牌BJ6441BJV1A","insuredIDNumber":"320124196612020626","carddate":"2014-12-24","address":"南京市溧水区东屏镇柳家边村乾隆路","insuredName":"谢模平","LicenseNo":"苏AB9N73","regisdate":"2014-12-24","FrameNo":"LNBMDBAF5EU121193"},{"insuredPhNo":"13776512314","EngineNo":"EW303087","VEHICLE_MODELSH":"北京现代牌BH7180PAY","insuredIDNumber":"341224198506218224","carddate":"2014-12-25","address":"南京市浦口区铁桥镇","insuredName":"方梅","LicenseNo":"苏AK0C77","regisdate":"2014-12-25","FrameNo":"LBECFAHB3EZ138249"},{"insuredPhNo":"18626416203","EngineNo":"EW257520","VEHICLE_MODELSH":"北京现代牌BH7181PAY","insuredIDNumber":"320125199404115217","carddate":"2014-12-22","address":"南京市高淳县桠溪镇桥李村留村21号","insuredName":"张叶平","LicenseNo":"苏AB2Q60","regisdate":"2014-12-22","FrameNo":"LBECFAHB4EZ119046"}]}
    #args=args['userlist']
    #args = [1,2,3,2,2,2,2,2,2]
    try:
        if len(args) <=10:
            #线程池
            threads = []
            print "程序开始运行%s" % datetime.datetime.now()
            for arg in args:
                th = threading.Thread(target=isRenewal.isRenewal2, args=(arg,))
                th.start()
                threads.append(th)
            for th in threads:
                th.join()
            print "程序结束运行%s" % datetime.datetime.now()
        elif len(args)>10:
            rang = (len(args)+10-1)/10
            for i in range(0,rang):
                if i < rang-1:
                    threads = []
                    print "程序开始运行%s" % datetime.datetime.now()
                    for arg in args[(i*10):(10*i+10)]:
                        th = threading.Thread(target=isRenewal.isRenewal2, args=(arg,))
                        th.start()
                        threads.append(th)
                    for th in threads:
                        th.join()
                    print "程序结束运行%s" % datetime.datetime.now()
                else:
                        # 线程池
                    threads = []
                    print "程序开始运行%s" % datetime.datetime.now()
                    for arg in args[(i*10):len(args)]:
                        th = threading.Thread(target=isRenewal.isRenewal2, args=(arg,))
                        th.start()
                        threads.append(th)
                    for th in threads:
                        th.join()
                    print "程序结束运行%s" % datetime.datetime.now()
    except Exception,e:
        print(e)