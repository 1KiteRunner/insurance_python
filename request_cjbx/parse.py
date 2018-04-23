# coding: utf8
__author__ = 'Administrator'
from bs4 import BeautifulSoup
import re
import jsonpath
import json
import time
import json
import datetime
import re


def parse_query_car(html):
    soup = BeautifulSoup(html, 'html.parser')

    box = soup.find_all(class_="box")
    tr = box[0].table.find_all("tr")
    alldata = {}
    list0 = []
    if len(tr) > 2:
        for i in range(1, len(tr)):
            onedict = {}
            # tr[i].input.get('value') #投保确认码
            onedict['company_id'] = tr[i].findAll('td')[1].getText()  # 投保公司
            onedict['permium_id'] = tr[i].findAll('td')[2].getText()  # 保单号
            onedict['toubao_time'] = tr[i].findAll('td')[3].getText()
            onedict['start_time'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
            onedict['end_time'] = conver_timestamp(tr[i].findAll('td')[5].getText())  # 保单开始时间
            onedict['palte_number'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
            list0.append(onedict)
            list0.sort(key=lambda obj: obj.get('end_time'), reverse=True)
    alldata["sy"] = list0

    list1 = []
    tr = box[1].table.find_all("tr")
    if len(tr) > 2:
        for i in range(1, len(tr)):
            onedict = {}
            # tr[i].input.get('value') #投保确认码
            onedict['company_id'] = tr[i].findAll('td')[1].getText()  # 投保公司
            onedict['permium_id'] = tr[i].findAll('td')[2].getText()  # 保单号
            onedict['toubao_time'] = tr[i].findAll('td')[3].getText()
            onedict['start_time'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
            onedict['end_time'] = conver_timestamp(tr[i].findAll('td')[5].getText())  # 保单开始时间
            onedict['palte_number'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
            list1.append(onedict)
            list1.sort(key=lambda obj: obj.get('end_time'), reverse=True)
    alldata["sy_chuxian"] = list1

    list2 = []
    tr = box[2].table.find_all("tr")
    if len(tr) > 2:
        for i in range(1, len(tr)):
            onedict = {}
            # tr[i].input.get('value') #投保确认码
            onedict['company_id'] = tr[i].findAll('td')[1].getText()  # 投保公司
            onedict['permium_id'] = tr[i].findAll('td')[2].getText()  # 保单号
            onedict['toubao_time'] = tr[i].findAll('td')[3].getText()
            onedict['start_time'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
            onedict['end_time'] = conver_timestamp(tr[i].findAll('td')[5].getText())  # 保单jieshu时间
            onedict['palte_number'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
            list2.append(onedict)
            list2.sort(key=lambda obj: obj.get('end_time'), reverse=True)
    alldata["jq"] = list2
    list3 = []
    tr = box[3].table.find_all("tr")
    if len(tr) > 2:
        for i in range(1, len(tr)):
            onedict = {}
            # tr[i].input.get('value') #投保确认码
            onedict['company_id'] = tr[i].findAll('td')[1].getText()  # 投保公司
            onedict['permium_id'] = tr[i].findAll('td')[2].getText()  # 保单号
            onedict['toubao_time'] = tr[i].findAll('td')[3].getText()
            onedict['start_time'] = tr[i].findAll('td')[4].getText()  # 保单开始时间
            onedict['end_time'] = conver_timestamp(tr[i].findAll('td')[5].getText())  # 保单开始时间
            onedict['palte_number'] = tr[i].findAll('td')[6].getText()  # 保单开始时间
            list3.append(onedict)
            list3.sort(key=lambda obj: obj.get('end_time'), reverse=True)
    alldata["jq_chuxian"] = list3
    return alldata


def conver_timestamp(dt="2016-05-05 20:28:54"):
    # 时间带个.
    dt = dt.split(".")[0]
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)


def conver_time(timestamp=1462451334):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def parse_car_detail(html):
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    try:
        box = soup.find_all(class_="massage overflowH")
        # print box

        leftbox_1 = box[0].find(class_="leftbox")
        # print leftbox
        if leftbox_1 != None:
            p_all = leftbox_1.find_all("p")
            # print p_all

            leftbox_2 = box[1].find(class_="leftbox")
            # print leftbox

            p = leftbox_2.find("p")
            data["CUST_NAME"] = p.get_text()
            data["PLATE_NUMBER"] = p_all[0].get_text() if p_all[0].get_text() else ""
            data["FRAME_NUMBER"] = p_all[1].get_text() if p_all[1].get_text() else ""
            data["VEHICLE_TYPE"] = p_all[2].get_text() if p_all[2].get_text() else ""
            data["VEHICLE_MODEL"] = p_all[3].get_text() if p_all[3].get_text() else ""
            data["ENGLISH_BRAND"] = p_all[4].get_text() if p_all[4].get_text() else ""
            data["VEHICLE_USE"] = p_all[5].get_text() if p_all[5].get_text() else ""
            data["VEHICLE_STATE"] = p_all[6].get_text() if p_all[6].get_text() else ""
            data["SEATING_CAPACITY"] = p_all[7].get_text() if p_all[7].get_text() else ""
            data["LATEST_INSPECTION_DATE"] = p_all[8].get_text() if p_all[8].get_text() else ""
            data["INSPECTION_VALID_DATE"] = p_all[9].get_text() if p_all[9].get_text() else ""
            data["ENERGY_TYPES"] = p_all[10].get_text() if p_all[10].get_text() else ""

            rightbox_1 = box[0].find(class_="rightbox")
            # print rightbox

            p_all = rightbox_1.find_all("p")

            data["PLATE_TYPE"] = p_all[0].get_text() if p_all[0].get_text() else ""
            data["ENGINE_NUMBER"] = p_all[1].get_text() if p_all[1].get_text() else ""
            data["INITIAL_REGISTRATION_DATE"] = p_all[2].get_text() if p_all[2].get_text() else ""
            data["BODY_COLOR"] = p_all[3].get_text() if p_all[3].get_text() else ""
            data["CHINESE_BRAND"] = p_all[4].get_text() if p_all[4].get_text() else ""
            data["TRANSFER_DATE"] = p_all[5].get_text() if p_all[5].get_text() else ""
            data["MANUFACTURER"] = p_all[6].get_text() if p_all[6].get_text() else ""
            data["APPROVED_LOAD"] = p_all[7].get_text() if p_all[7].get_text() else ""
            data["DISPLACEMENT"] = p_all[8].get_text() if p_all[8].get_text() else ""
            data["TRACTION_MASS"] = p_all[9].get_text() if p_all[9].get_text() else ""
            data["CURB_WEIGHT"] = p_all[10].get_text() if p_all[10].get_text() else ""

            return data
        else:
            return 0
    except Exception as e:
        print(e)
        return 0


# # 解析html
def bs4_query_car(html):
    # html = query_car()
    soup = BeautifulSoup(html, 'html.parser')

    dict_1, dict_2, dict_3, dict_4 = {}, {}, {}, {}

    list_1, list_2, list_3, list_4 = [], [], [], []

    box = soup.find_all(class_="box")
    # print len(box)

    if not box[0].find_all('td')[0].find("font"):
        tr = box[0].find_all('tr')
        for i in range(1, len(tr)):
            td = tr[i].find_all('td')
            if td:
                dict_1['key_1'] = td[1].get_text()
                dict_1['key_2'] = td[4].get_text()
                dict_1['key_3'] = td[5].get_text()

                list_1.append(dict_1)

    if not box[1].find_all('td')[0].find("font"):
        tr = box[1].find_all('tr')
        for i in range(1, len(tr)):
            td = tr[i].find_all('td')
            if td:
                dict_2['key_1'] = td[1].get_text()
                dict_2['key_2'] = td[4].get_text()
                dict_2['key_3'] = td[5].get_text()

                list_2.append(dict_2)

    if not box[2].find_all('td')[0].find("font"):
        tr = box[2].find_all('tr')
        for i in range(1, len(tr)):
            td = tr[i].find_all('td')
            if td:
                dict_3['key_1'] = td[1].get_text()
                dict_3['key_2'] = td[4].get_text()
                dict_3['key_3'] = td[5].get_text()

                list_3.append(dict_3)

    if not box[3].find_all('td')[0].find("font"):
        tr = box[3].find_all('tr')

        for i in range(1, len(tr)):
            td = tr[i].find_all('td')
            if td:
                dict_4['key_1'] = td[1].get_text()
                dict_4['key_2'] = td[4].get_text()
                dict_4['key_3'] = td[5].get_text()

                list_4.append(dict_4)

    all_data = {}
    all_data['list_1'] = list_1
    all_data['list_2'] = list_2
    all_data['list_3'] = list_3
    all_data['list_4'] = list_4

    return all_data




