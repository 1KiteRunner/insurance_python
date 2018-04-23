# -*- coding:utf-8 -*-
__author__ = 'weikai'
import jsonpath
from charTools import is_number
# 类型包括 T1 T2 T3 货车 挂车
car_type = [{"type": "货车", "key": "XXY", "desc": "厢式车"}, {"type": "T2", "key": "XLC", "desc": "冷藏车"},
            {"type": "T2", "key": "XBW", "desc": "保温车"}, {"type": "T3", "key": "XQC", "desc": "囚车"},
            {"type": "T3", "key": "XF", "desc": "消防车"}, {"type": "T2", "key": "GJB", "desc": "混凝土搅拌车"},
            {"type": "T2", "key": "THB", "desc": "混凝土泵车"}, {"type": "T1", "key": "GJY", "desc": "加油车"},
            {"type": "T2", "key": "GSS", "desc": "洒水车"}, {"type": "T3", "key": "XJH", "desc": "救护车"},
            {"type": "T3", "key": "XYC", "desc": "运钞车"}, {"type": "T2", "key": "TSL", "desc": "扫路车"},
            {"type": "T2", "key": "JGK", "desc": "高空作业车"}, {"type": "货车", "key": "JSQ", "desc": "随车起重车"},
            {"type": "T2", "key": "JQZ", "desc": "汽车起重车"}, {"type": "货车", "key": "XQY", "desc": "爆破器材运输车"},
            {"type": "T3", "key": "DY", "desc": "电源车"}, {"type": "T3", "key": "DS", "desc": "电视车"},
            {"type": "T3", "key": "BDSNG", "desc": "数字卫星通信车"}, {"type": "T3", "key": "XTX", "desc": "通讯车"},
            {"type": "T2", "key": "GLQ", "desc": "沥青洒布车"}, {"type": "T2", "key": "TYH", "desc": "路面养护车"},
            {"type": "T3", "key": "XYL", "desc": "医疗专用车"}, {"type": "T3", "key": "XTJ", "desc": "体检医疗车"},
            {"type": "T2", "key": "ZYS", "desc": "压缩式垃圾车"}, {"type": "T2", "key": "ZLJ", "desc": "自卸式垃圾车"},
            {"type": "T2", "key": "GXE", "desc": "吸粪清洁车"}, {"type": "T2", "key": "GXW", "desc": "吸污车"},
            {"type": "T1", "key": "GYS", "desc": "液态食品运输车"}, {"type": "挂车", "key": "TCL", "desc": "车辆运输半挂车"},
            {"type": "挂车", "key": "TJZ", "desc": "集装箱运输半挂车"}, {"type": "T2", "key": "TQZ", "desc": "清障车"},
            {"type": "T3", "key": "XJB", "desc": "警备车"}, {"type": "T2", "key": "XLJ", "desc": "旅居车"},
            {"type": "T2", "key": "TSN", "desc": "固井水泥车"}, {"type": "T2", "key": "GGQ", "desc": "高压气体运输(长管)半挂车"},
            {"type": "T3", "key": "XZD", "desc": "医用X射线诊断车"}, {"type": "T3", "key": "XCX", "desc": "采血车"},
            {"type": "T2", "key": "GFL", "desc": "粉粒物料运输车"}, {"type": "T1", "key": "GHY", "desc": "化工液体运输车"},
            {"type": "T1", "key": "GYQ", "desc": "液化气体运输车"}, {"type": "挂车", "key": "TD", "desc": "低平板半挂车"},
            {"type": "挂车", "key": "ZZX", "desc": "自卸半挂车"}, {"type": "T3", "key": "GXFSG", "desc": "水罐消防车"},
            {"type": "T3", "key": "GXFPM", "desc": "泡沫消防车"}, {"type": "T3", "key": "XYZ", "desc": "邮政车"},
            {"type": "T2", "key": "TCJ", "desc": "测井车"}, {"type": "T2", "key": "TXJ", "desc": "修井机"},
            {"type": "T2", "key": "GPS", "desc": "喷洒车"}, {"type": "T1", "key": "GYY", "desc": "运油车"}]


def get_specical_car_type(carModel):
    '''
    :param carModel: 解放CA3160K2A80
    :return:{"type": "T2", "key": "TCJ", "desc": "测井车"} else None
    '''
    flag1 = 0
    carModel_list = list(carModel)
    for i in carModel_list:
        if is_number(i):
            if int(i) == 5:
                flag1 = 1
                break
    key = ""
    for s in car_type:
        if s['key'] in carModel:
            key = s['key']
            break
    re = "$.[?(@.key=='" + key + "')"
    out = jsonpath.jsonpath(car_type, re)
    if flag1 == 1 and out is not False:
        return out[0]


def get_main_cartype(carModel):
    '''
    #信达计算车辆大类 A 客车 G挂车  H货车  特1 T1 T2 T3 T4  BG半挂牵引车
    载货汽车	1
    越野汽车	2
    自卸汽车 	3
    牵引汽车  	4
    专用汽车 	5
    客车 	6
    轿车 	7
    半挂车及专用半挂车	9
    '''
    carModel_list = list(carModel)
    for i in carModel_list:
        if is_number(i):
            if int(i) == 2 or int(i) == 6 or int(i) == 7:
                return "A"
            if int(i) == 4:
                return "BG"
            else:
                return None





if __name__ == "__main__":
    str = u"东风DFL1160BX9载货汽车"
    print get_main_cartype(str)
