# -*- coding:utf-8 -*-
__author__ = 'weikai'
import sys, re
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
from common.timeUtil import get_timestamp
from common.log import Logger

log = Logger()


def parse_query_all(html):
    soup = BeautifulSoup(html, 'html.parser')
    box = soup.find_all(class_="box")
    tr = box[0].table.find_all("tr")
    alldata = {}
    list0 = []
    try:
        if len(tr) > 1 and "没有" not in tr[1].text:
            for i in range(1, len(tr)):
                onedict = {}
                onedict['INSURE_CODE'] = tr[i].findAll('td')[0].getText()  # 投保确认码
                onedict['COMPANY'] = tr[i].findAll('td')[1].getText()  # 投保公司
                onedict['POLICY_NO'] = tr[i].findAll('td')[2].getText()  # 保单号
                onedict['INSURED_QUERY_TIME'] = tr[i].findAll('td')[3].getText()
                onedict['START_DATE'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
                onedict['END_DATE'] = tr[i].findAll('td')[5].getText()  # 保单开始时间
                onedict['PLATE_NO'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
                onedict['FRAME_NO'] = tr[i].findAll('td')[7].getText()  # 保单开始时间
                onedict['ENGINE_NO'] = tr[i].findAll('td')[8].getText()  # 保单开始时间
                onedict['VEHICLE_CODE'] = tr[i].findAll('td')[9].getText()  # 保单开始时间
                onedict['VEHICLEUSE_CODE'] = tr[i].findAll('td')[10].getText()  # 保单开始时间
                onedict['OWNER_NAME'] = tr[i].findAll('td')[11].getText()  # 保单开始时间
                onedict['OWNER_CATEGORY'] = tr[i].findAll('td')[12].getText()  # 保单开始时间
                onedict["TYPE"] = "1"
                list0.append(onedict)
                # list0.sort(key=lambda obj: obj.get('end_time'), reverse=True)
        alldata["JQ"] = list0

        list1 = []
        tr = box[1].table.find_all("tr")
        if len(tr) > 1 and "没有" not in tr[1].text:
            for i in range(1, len(tr)):
                onedict = {}
                onedict['CLAIM_CODE'] = tr[i].findAll('td')[0].getText()  # 理赔编码
                onedict['COMPANY'] = tr[i].findAll('td')[1].getText()  # 投保公司
                onedict['POLICY_NO'] = tr[i].findAll('td')[2].getText()  # 保单号
                onedict['CLOSE_TIME'] = tr[i].findAll('td')[3].getText()
                onedict['START_TIME'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
                onedict['END_TIME'] = tr[i].findAll('td')[5].getText()  # 保单开始时间
                onedict['PALTE_NO'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
                onedict['PLATE_TYPE'] = tr[i].findAll('td')[7].getText()  # 保单开始时间
                onedict['FRAME_NO'] = tr[i].findAll('td')[8].getText()  # 车架
                onedict['ENGINE_NO'] = tr[i].findAll('td')[9].getText()  # 车架
                onedict['DANGER_TIME'] = tr[i].findAll('td')[10].getText()  # 出现时间
                onedict['REPORT_TIME'] = tr[i].findAll('td')[11].getText()  # 报案时间
                onedict['CLAIM_TYPE'] = tr[i].findAll('td')[12].getText()  # 报案时间
                onedict['TOTAL_AMOUNT'] = tr[i].findAll('td')[13].getText()  # 赔款总额
                list1.append(onedict)
                # list1.sort(key=lambda obj: obj.get('end_time'), reverse=True)
        alldata["JQ_CHUXIAN"] = list1

        list2 = []
        tr = box[2].table.find_all("tr")
        if len(tr) > 1 and "没有" not in tr[1].text:
            for i in range(1, len(tr)):
                onedict = {}
                onedict['INSURE_CODE'] = tr[i].findAll('td')[0].getText()  # 投保确认码
                onedict['COMPANY'] = tr[i].findAll('td')[1].getText()  # 投保公司
                onedict['POLICY_NO'] = tr[i].findAll('td')[2].getText()  # 保单号
                onedict['INSURED_QUERY_TIME'] = tr[i].findAll('td')[3].getText()
                onedict['START_DATE'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
                onedict['END_DATE'] = tr[i].findAll('td')[5].getText()  # 保单开始时间
                onedict['PLATE_NO'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
                onedict['FRAME_NO'] = tr[i].findAll('td')[7].getText()  # 保单开始时间
                onedict['ENGINE_NO'] = tr[i].findAll('td')[8].getText()  # 保单开始时间
                onedict['VEHICLE_CODE'] = tr[i].findAll('td')[9].getText()  # 保单开始时间
                onedict['VEHICLEUSE_CODE'] = tr[i].findAll('td')[10].getText()  # 保单开始时间
                onedict['OWNER_NAME'] = tr[i].findAll('td')[11].getText()  # 保单开始时间
                onedict['OWNER_CATEGORY'] = tr[i].findAll('td')[12].getText()  # 保单开始时间
                onedict["TYPE"] = "2"
                list2.append(onedict)
                # list2.sort(key=lambda obj: obj.get('end_time'), reverse=True)
        alldata["SY"] = list2
        list3 = []
        tr = box[3].table.find_all("tr")
        if len(tr) > 1 and "没有" not in tr[1].text:
            for i in range(1, len(tr)):
                onedict = {}
                onedict['CLAIM_CODE'] = tr[i].findAll('td')[0].getText()  # 理赔编码
                onedict['COMPANY'] = tr[i].findAll('td')[1].getText()  # 投保公司
                onedict['POLICY_NO'] = tr[i].findAll('td')[2].getText()  # 保单号
                onedict['CLOSE_TIME'] = tr[i].findAll('td')[3].getText()
                onedict['START_TIME'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
                onedict['END_TIME'] = tr[i].findAll('td')[5].getText()  # 保单开始时间
                onedict['PALTE_NO'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
                onedict['PLATE_TYPE'] = tr[i].findAll('td')[7].getText()  # 保单开始时间
                onedict['FRAME_NO'] = tr[i].findAll('td')[8].getText()  # 车架
                onedict['ENGINE_NO'] = tr[i].findAll('td')[9].getText()  # 车架
                onedict['DANGER_TIME'] = tr[i].findAll('td')[10].getText()  # 出现时间
                onedict['REPORT_TIME'] = tr[i].findAll('td')[11].getText()  # 报案时间
                onedict['CLAIM_TYPE'] = tr[i].findAll('td')[12].getText()  # 赔款总额
                onedict['TOTAL_AMOUNT'] = tr[i].findAll('td')[13].getText()  # 赔款总额
                list3.append(onedict)
                # list3.sort(key=lambda obj: obj.get('end_time'), reverse=True)
        alldata["SY_CHUXIAN"] = list3

        tr = box[4].table.find_all("tr")
        # 车主信息
        if len(tr) > 1 and "没有" not in tr[1].text:
            for i in range(1, 2):
                alldata['PALTE_NO'] = tr[i].findAll('td')[0].getText()
                alldata['PLATE_TYPE'] = tr[i].findAll('td')[1].getText()
                alldata['FRAME_NO'] = tr[i].findAll('td')[2].getText()  # 车架
                alldata['ENGINE_NO'] = tr[i].findAll('td')[3].getText()  # 车架
                alldata['OWNER_NAME'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
                alldata['TRANSFE_TIME'] = tr[i].findAll('td')[5].getText()  # 转移登记日期
                alldata['UPDATE_TIME'] = tr[i].findAll('td')[6].getText()  # 交管更新时间

        # 历年交管违法信息
        list4 = []
        tr = box[5].table.find_all("tr")
        if len(tr) > 1 and "没有" not in tr[1].text:
            for i in range(1, len(tr)):
                onedict = {}
                onedict['ILLEGAL_CODE'] = tr[i].findAll('td')[0].getText()  # 违法编号
                onedict['PALTE_NO'] = tr[i].findAll('td')[1].getText()  # 保单开始时间
                onedict['PLATE_TYPE'] = tr[i].findAll('td')[2].getText()  # 保单开始时间
                onedict['FRAME_NO'] = tr[i].findAll('td')[3].getText()  # 车架
                onedict['ENGINE_NO'] = tr[i].findAll('td')[4].getText()  # 车架
                onedict['ILLEGAL_TIME'] = tr[i].findAll('td')[5].getText()  # 违法时间
                onedict['ILLEGAL_ACTIVE'] = tr[i].findAll('td')[6].getText()  # 违法行为
                onedict['ILLEGAL_TYPE'] = tr[i].findAll('td')[7].getText()  # 违法类型
                onedict['DECISION_NO'] = tr[i].findAll('td')[8].getText()  # 决定书编号
                onedict['ILLEGAL_TYPE'] = tr[i].findAll('td')[9].getText()  # 赔款总额
                list4.append(onedict)
                # list3.sort(key=lambda obj: obj.get('end_time'), reverse=True)
        alldata["JG_ILLEGAL"] = list4

        # 历年交管违事故信息 Accident ACCIDENT_CODE
        list5 = []
        tr = box[6].table.find_all("tr")
        if len(tr) > 1 and "没有" not in tr[1].text:
            print(len(tr) > 1 and "没有" not in tr[1].text)
            for i in range(1, len(tr)):
                onedict = {}
                onedict['ACCIDENT_CODE'] = tr[i].findAll('td')[0].getText()  # 事故号
                onedict['REG_TIME'] = tr[i].findAll('td')[1].getText()  # 登记日期
                onedict['REPORT_TIME'] = tr[i].findAll('td')[2].getText()  # 报案日期
                onedict['ACCIDENT_TIME'] = tr[i].findAll('td')[3].getText()  # 事故日期
                onedict['ACCIDENT_PLACE'] = tr[i].findAll('td')[4].getText()  # 事故地点
                onedict['ACCIDENT_TYPE'] = tr[i].findAll('td')[5].getText()  # 事故碰撞类型
                onedict['REPOET_PLATE'] = tr[i].findAll('td')[6].getText()  # 报警车牌
                onedict['REPOET_TEL'] = tr[i].findAll('td')[7].getText()  # 报警电话
                onedict['ACCIDENT_CITY'] = tr[i].findAll('td')[8].getText()  # 事故所在城市
                list5.append(onedict)
                # list3.sort(key=lambda obj: obj.get('end_time'), reverse=True)
        alldata["JG_ACCIDENT"] = list5
        alldata['UPDATE_TIME'] = get_timestamp()

        return alldata
    except Exception as e:
        log.error(traceback.format_exc())
        return {}


def parse_insuranceType(body):
    amountall = re.findall(r"<p>(.+?)</p>", body, re.S)[2]
    if "元" in amountall:
        amountall = amountall[0:-1]
    else:
        amountall = "0"
    info = ""
    soup1 = BeautifulSoup(body, 'html.parser')
    info = soup1.select('.leftbox')[0].getText().replace("\n", "|")

    tables = re.findall(r"<!--<tbody>(.+?)</tbody>", body, re.S)[0]
    soup2 = BeautifulSoup(tables, 'html.parser')
    trs = soup2.findAll('tr')
    list1 = []
    for i in xrange(len(trs)):
        tds = trs[i].findAll('td')
        tmp = {}
        for s in xrange(len(tds)):
            td = tds[s].getText().replace("\t", "").replace("\r", "").replace("\n", "").replace("元", "")  # 依次为 险种 保费 保额
            if s == 0:
                tmp['PremiumType'] = td
            elif s == 1:
                tmp['Premium'] = td
            elif s == 2:
                tmp['insuredAmount'] = td
        list1.append(tmp)

    import json
    import jsonpath
    # print jsonpath.jsonpath(list1,"$.[?(@.PremiumType=='三者险')]")
    otherHurtPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='三者险')]")
    otherHurtPremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（三者险）')]")

    carDamagePremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='车损险')]")
    carDamagePremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（车损险）')]")

    driverDutyPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='车上人员责任险（司机）')]")
    driverDutyPremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（车上人员责任险（司机））')]")

    passengerDutyPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='车上人员责任险（乘客）')]")
    passengerDutyPremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（车上人员责任险（乘客））')]")

    carNickPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='划痕险')]")
    carNickPremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（划痕险）')]")

    glassBrokenPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='玻璃破碎险')]")

    carFirePremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='自燃险')]")
    carFirePremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（自燃险）')]")

    engineWadingPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='发动机涉水险')]")
    engineWadingPremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（发动机涉水险）')]")

    carTheftPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='盗抢险')]")
    carTheftPremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（盗抢险）')]")
    repairFactoryPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='指定修理厂险')]")
    carGoodsPremium = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='车上货物责任险')]")
    carGoodsPremiumBench = jsonpath.jsonpath(list1, "$.[?(@.PremiumType=='不计免赔率（车上货物责任险）')]")

    type = {
        'compulsoryInsurance': "1", 'nAggTax': "1",
        'otherHurtPremium': {"isCheck": ("1" if otherHurtPremium != False else "0"),
                             "Amount": (otherHurtPremium[0]['insuredAmount'] if otherHurtPremium != False else "0")},
        'carNickPremium': {"isCheck": ("1" if carNickPremium != False else "0"),
                           "Amount": (carNickPremium[0]['insuredAmount'] if carNickPremium != False else "0")},
        'driverDutyPremium': {"isCheck": ("1" if driverDutyPremium != False else "0"),
                              "Amount": (driverDutyPremium[0]['insuredAmount'] if driverDutyPremium != False else "0")},
        'passengerDutyPremium': {"isCheck": ("1" if passengerDutyPremium != False else "0"), "Amount": (
            passengerDutyPremium[0]['insuredAmount'] if passengerDutyPremium != False else "0")},
        'glassBrokenPremium': ("1" if glassBrokenPremium != False else "0"),
        'carFirePremium': ("1" if carFirePremium != False else "0"),
        'engineWadingPremium': ("1" if engineWadingPremium != False else "0"),
        'carTheftPremium': ("1" if carTheftPremium != False else "0"),
        'carDamagePremium': ("1" if carDamagePremium != False else "0"),
        'carDamageBenchMarkPremium': ("1" if carDamagePremiumBench != False else "0"),
        'otherHurtBenchMarkPremium': ("1" if otherHurtPremiumBench != False else "0"),
        'carTheftBenchMarkPremium': ("1" if carTheftPremiumBench != False else "0"),
        'driverDutyBenchMarkPremium': ("1" if driverDutyPremiumBench != False else "0"),
        'passengerBenchMarkPremium': ("1" if passengerDutyPremiumBench != False else "0"),
        'carNickBenchMarkPremium': ("1" if carNickPremiumBench != False else "0"),
        'carFireBrokenBenchMarkPremium': ("1" if carFirePremiumBench != False else "0"),
        'engineWadingBenchMarkPremium': ("1" if engineWadingPremiumBench != False else "0"),
        'repairFactoryPremium': ("1" if repairFactoryPremium != False else "0"),
        "carGoodsPremium": ("1" if carGoodsPremium != False else "0"),
        "carGoodsPremiumBench": ("1" if carGoodsPremiumBench != False else "0"),
        'SySumPremium': amountall,
        'JqSumPremium': "0"
    }
    return {"insuranceType": type, "Info": info}


if __name__ == "__main__":
    f = open("C:\Users\weikai\Desktop\\0000.html")
    body = f.read()
    s = parse_query_all(body)
    from common.mongodb.mongoUtils import mg_update_insert, mg_find
    # mg_update_insert('InsuranceInfo',{'BODY.FRAME_NO': 'LFV5A24F6B3005646'},s)
    # print client.update_insert('InsuranceInfo', {'BODY.FRAME_NO': 'LFV5A24F6B3005646'}, {"$set": {"BODY": s['BODY']}})
    # data = mg_find('InsuranceInfo', {'BODY.FRAME_NO': 'LFV5A24F6B3005646'})
    # data=client.find('InsuranceInfo', {'BODY.PALTE_NO': '苏A5112D'})
    # print data.has_key('_id')
    # data.pop('_id')

    print s
