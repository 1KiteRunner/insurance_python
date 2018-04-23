# -*- coding:utf-8 -*-
__author__ = 'weikai'
import time
from simplethreads.ThreadPool import ThreadPool
import threading
from time import ctime,sleep
def ddd(a):
    time.sleep(5)
    print("%d" % (time.time() * 1000))
    return a

dicts={"userlist":[{"insuredPhNo":"18251867797","EngineNo":"1405110930","VEHICLE_MODELSH":"哈弗牌CC6460RM01","insuredIDNumber":"320125198711304822","carddate":"2014-12-29","address":"溧水区永阳镇中山东路290号1栋4号","insuredName":"王秋兰","LicenseNo":"苏AQ6C06","regisdate":"2014-12-29","FrameNo":"LGWEF4A56EF280301"},{"insuredPhNo":"18761529057","EngineNo":"3127348","VEHICLE_MODELSH":"马自达牌CAM7150M5","insuredIDNumber":"32012419910417303X","carddate":"2014-12-24","address":"溧水区晶桥镇邰村荷塘村15号","insuredName":"周式华","LicenseNo":"苏AB9N35","regisdate":"2014-12-24","FrameNo":"LVRHDFML8EN340221"},{"insuredPhNo":"17092589038","EngineNo":"KL1392","VEHICLE_MODELSH":"北京牌BJ7150C5E2","insuredIDNumber":"320125198610093122","carddate":"2014-12-26","address":"南京市高淳区漆桥镇老庄山76号","insuredName":"杨小香","LicenseNo":"苏AB3Q98","regisdate":"2014-12-26","FrameNo":"LNBSCCAH3EF031577"},{"insuredPhNo":"15851844024","EngineNo":"JL478QEA EC4M139626","VEHICLE_MODELSH":"长安牌SC7169B5","insuredIDNumber":"320122198710232434","carddate":"2014-12-11","address":"南京市浦口区桥林街道林东村林东社区","insuredName":"成磊","LicenseNo":"苏AK8A77","regisdate":"2014-12-11","FrameNo":"LS5A2ABE6EA175199"},{"insuredPhNo":"18721338102","EngineNo":"143120893","VEHICLE_MODELSH":"别克牌SGM7162DMAB","insuredIDNumber":"320125198901030711","carddate":"2014-12-18","address":"南京市高淳区砖墙镇大涵村万家65号","insuredName":"万立顺","LicenseNo":"苏AB0Q87","regisdate":"2014-12-18","FrameNo":"LSGPB54U3FD057155"},{"insuredPhNo":"18068329197","EngineNo":"142410788","VEHICLE_MODELSH":"别克牌SGM7161EAA2","insuredIDNumber":"320282198808156611","carddate":"2014-12-2","address":"江苏省宜兴市和桥镇闸口村张家村68号","insuredName":"钱波","LicenseNo":"苏B768TD","regisdate":"2014-12-2","FrameNo":"LSGGA54E4EH287001"},{"insuredPhNo":"13913355531","EngineNo":"EW606024","VEHICLE_MODELSH":"北京现代牌BH6440LAY","insuredIDNumber":"320123197511253445","carddate":"2014-12-30","address":"六合区横梁街道王子路30-9号","insuredName":"胡秀兰","LicenseNo":"苏AB1P05","regisdate":"2014-12-30","FrameNo":"LBELMBKC0EY555590"},{"insuredPhNo":"18761636737","EngineNo":"142493753","VEHICLE_MODELSH":"雪佛兰牌SGM7150DMAA","insuredIDNumber":"320125199003223321","carddate":"2014-12-29","address":"溧水区和凤镇双牌石八建公司楼2栋202室","insuredName":"张金香","LicenseNo":"苏AB2R68","regisdate":"2014-12-29","FrameNo":"LSGPC52H2FF017611"},{"insuredPhNo":"15952096020","EngineNo":"14096911","VEHICLE_MODELSH":"东风牌DXK6440AF3","insuredIDNumber":"320123198608064020","carddate":"2014-12-30","address":"六合区金牛湖街道八百大道288-5号","insuredName":"王仁霞","LicenseNo":"苏AB0P61","regisdate":"2014-12-30","FrameNo":"LVZA43F93EC554224"},{"insuredPhNo":"15951683827","EngineNo":"E10E19284","VEHICLE_MODELSH":"北京牌BJ6441BJV1A","insuredIDNumber":"320124196612020626","carddate":"2014-12-24","address":"南京市溧水区东屏镇柳家边村乾隆路","insuredName":"谢模平","LicenseNo":"苏AB9N73","regisdate":"2014-12-24","FrameNo":"LNBMDBAF5EU121193"},{"insuredPhNo":"13776512314","EngineNo":"EW303087","VEHICLE_MODELSH":"北京现代牌BH7180PAY","insuredIDNumber":"341224198506218224","carddate":"2014-12-25","address":"南京市浦口区铁桥镇","insuredName":"方梅","LicenseNo":"苏AK0C77","regisdate":"2014-12-25","FrameNo":"LBECFAHB3EZ138249"},{"insuredPhNo":"18626416203","EngineNo":"EW257520","VEHICLE_MODELSH":"北京现代牌BH7181PAY","insuredIDNumber":"320125199404115217","carddate":"2014-12-22","address":"南京市高淳县桠溪镇桥李村留村21号","insuredName":"张叶平","LicenseNo":"苏AB2Q60","regisdate":"2014-12-22","FrameNo":"LBECFAHB4EZ119046"}]}

createVar = locals()
listTemp=dicts['userlist']
for i,s in enumerate(listTemp):
    createVar['a'+str(i)]=s
    print('a'+str(i))

lenuser=len(dicts['userlist'])
#print(a1)
lenuser=5

#pool = ThreadPool(lenuser)

#pool.process(ddd( locals()['a'+str(1)]))


threads = []
t1 = threading.Thread(target=ddd,args=(u'爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=ddd,args=(u'阿凡达',))
threads.append(t2)


if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()








