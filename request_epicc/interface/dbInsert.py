# -*- coding:utf-8 -*-
import datetime

import pymysql.cursors

from common.log import Logger

log = Logger()
def soupDb( PremiumInfo, data, INSURE_CAR_ID):
    connection = pymysql.connect(host='120.55.189.14',
                                 user='insurance',
                                 # password='123456',
                                 password='insurance',
                                 db='insurance',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    INSURE_CAR_ID = str(INSURE_CAR_ID)
    startDate = data[2]#保险开始时间
    endDate = data[3]#保险结束时间
    seatQuantity = int(data[4])#座位数
    otherHurtPremium = {}
    if seatQuantity < 7:
        otherHurtPremium = {'50000': '432.90', '100000': '624.65', '150000': '713.05', '200000': '774.15','300000': '874.25', '500000': '1049.10', '1000000': '1366.30', '1500000': '1568.35','2000000': '1742.49', '3000000': '2080.32', '5000000': '2735.09'}
    elif seatQuantity < 11:
        otherHurtPremium = {'50000': '400.40', '100000': '564.85', '150000': '638.30', '200000': '688.35', '300000': '770.90', '500000': '917.80', '1000000': '1195.35', '1500000': '1372.06','2000000': '1524.41', '3000000': '1819.97', '5000000': '2392.81'}
    disCount = float(PremiumInfo[0]['otherHurtPremium'][0])/(float(otherHurtPremium[str(PremiumInfo[1]['otherHurtBaoE'][0]).replace('.00','')])/0.65)

    insurance_company={
        '平安保险':'1',
        '中国人保车辆保险':'2',
        '太平洋车辆保险':'3',
        '中华联合车辆保险':'4',
        '大地车辆保险':'5',
        '天安车辆保险':'6',
        '永安车辆保险':'7',
        '阳光车辆保险':'8',
        '安邦车辆保险':'9',
        '太平车辆保险':'10'
    }
    insurance_type={
        'compulsory_insurance':'1',
        'carDamagePremium':'2',
        'otherHurtPremium':'3',
        'carTheftPremium': '4',
        'driverDutyPremium': '5',
        'passengerDutyPremium': '6',
        'glassBrokenPremium': '7',
        'carNickPremium': '8',
        'carFirePremium': '9',
        'engineWadingPremium': '11',
        'NAggTax':'12',
        'carDamageBenchMarkPremium': '20',
        'otherHurtBenchMarkPremium': '30',
        'carTheftBenchMarkPremium': '40',
        'driverDutyBenchMarkPremium': '50',
        'passengerBenchMarkPremium': '60',
        'carNickBenchMarkPremium': '80',
        'carFireBrokenBenchMarkPremium': '90',
        'engineWadingBenchMarkPremium': '110'
    }
    company = insurance_company['中国人保车辆保险']
    sql1 = "INSERT INTO `car_premium` (`INSURE_CAR_ID`, `INSURANCE_TYPE_ID`,`PREMIUM`,`COMPANY_ID`,`DISCOUNT_RATE`) VALUES (%s, %s, %s, %s, %s)"
    sql2 = "INSERT INTO `car_premium` (`INSURE_CAR_ID`, `INSURANCE_TYPE_ID`,`PREMIUM`,`COMPANY_ID`,`DISCOUNT_RATE`,`BAO_E`) VALUES (%s, %s, %s, %s, %s, %s)"

    # compulsory_insurance = soup.find(id='prpCitemKindCI.premium').get('value')#交强险
    # compulsory_insurance_rate = soup.find(id='prpCitemKindCI.adjustRate').get('value')#交强险折扣系数
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['compulsory_insurance'],compulsory_insurance,company,compulsory_insurance_rate,startDate,endDate))
    #     connection.commit()
    # except:
    #     connection.close()

    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['compulsory_insurance'] is not None:
                compulsory_insurance = PremiumInfo[0]['compulsory_insurance']  # 车损险含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['compulsory_insurance'], compulsory_insurance, company, ""))
            if PremiumInfo[0]['NAggTax'] is not None:
                NAggTax = PremiumInfo[0]['NAggTax']  # 车损险不计免赔含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['NAggTax'], NAggTax, company,1.0))
        connection.commit()
    except:
        connection.close()

    # carDamageBenchMarkRate = soup.find(id="prpCitemKindsTemp[10].rate").get('value')#车损险不计免赔费率
    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['carDamagePremium'] is not False:
                carDamagePremium = PremiumInfo[0]['carDamagePremium'][0]  # 车损险含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carDamagePremium'], carDamagePremium, company, disCount))
            if PremiumInfo[2]['carDamageBenchMarkPremium'] is not False:
                carDamageBenchMarkPremium = PremiumInfo[2]['carDamageBenchMarkPremium'][0] # 车损险不计免赔含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carDamageBenchMarkPremium'], carDamageBenchMarkPremium,company, disCount))
        connection.commit()
    except:
        connection.close()


    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['carTheftPremium'] is not False:
                carTheftPremium = PremiumInfo[0]['carTheftPremium'][0] #盗抢险含税保费
                cursor.execute(sql1, ( INSURE_CAR_ID, insurance_type['carTheftPremium'], carTheftPremium, company, disCount))
            if PremiumInfo[2]['carTheftBenchMarkPremium'] is not False:
                carTheftBenchMarkPremium = PremiumInfo[2]['carTheftBenchMarkPremium'][0]  #盗抢险的含税不计免赔保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carTheftBenchMarkPremium'], carTheftBenchMarkPremium, company,disCount))
        connection.commit()
    except:
        connection.close()


    if PremiumInfo[0]['otherHurtPremium'] is not False:
        otherHurtPremium = PremiumInfo[0]['otherHurtPremium'][0]#三者责任险的含税保费
        # otherHurtQuota = PremiumInfo[1]['otherHurtBaoE']#三者责任险的保额
        # otherHurtBenchMarkPremium = PremiumInfo[2]['otherHurtBenchMarkPremium']#三者责任险的不计免赔
        # otherHurtBenchMarkRate = soup.find(id="prpCitemKindsTemp[11].rate").get('value')#三者责任险的不计免赔费率
        otherHurtBenchMarkRate = int(float(PremiumInfo[2]['otherHurtBenchMarkPremium'][0])/float(PremiumInfo[0]['otherHurtPremium'][0])*100)
        if seatQuantity<7:
            otherHurtPremium = {'50000':'432.90','100000':'624.65','150000':'713.05','200000':'774.15','300000':'874.25','500000':'1049.10','1000000':'1366.30','1500000':'1568.35','2000000':'1742.49','3000000':'2080.32','5000000':'2735.09'}
        elif seatQuantity<11:
            otherHurtPremium = {'50000': '400.40', '100000': '564.85', '150000': '638.30', '200000': '688.35', '300000': '770.90', '500000': '917.80', '1000000': '1195.35', '1500000': '1372.06', '2000000': '1524.41', '3000000': '1819.97', '5000000': '2392.81'}
        for (d, x) in otherHurtPremium.items():
            m = float(x)/0.65*float(disCount)
            n = float(x)/0.65*float(disCount)*float(otherHurtBenchMarkRate)/100
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['otherHurtPremium'],m,company,disCount,d))
                    cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['otherHurtBenchMarkPremium'],n, company, disCount, d))
                connection.commit()
            except:
                connection.close()


    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['driverDutyPremium'] is not False:
                driverDutyPremium = PremiumInfo[0]['driverDutyPremium'][0] #盗抢险含税保费
                driverDutyQuota = PremiumInfo[1]['driverDutyBaoE'][0]  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['driverDutyPremium'], driverDutyPremium, company, disCount, driverDutyQuota))
            if PremiumInfo[2]['driverDutyBenchMarkPremium'] is not False:
                driverDutyBenchMarkPremium = PremiumInfo[2]['driverDutyBenchMarkPremium'][0]  #盗抢险的含税不计免赔保费
                driverDutyQuota = PremiumInfo[1]['driverDutyBaoE'][0]  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['driverDutyBenchMarkPremium'], driverDutyBenchMarkPremium, company,disCount, driverDutyQuota))
        connection.commit()
    except:
        connection.close()


    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['passengerDutyPremium'] is not False:
                passengerDutyPremium = PremiumInfo[0]['passengerDutyPremium'][0] #盗抢险含税保费
                passengerDutyQuota = PremiumInfo[1]['passengerDutyBaoe'][0]  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['passengerDutyPremium'], passengerDutyPremium, company, disCount, passengerDutyQuota))
            if PremiumInfo[2]['passengerBenchMarkPremium'] is not False:
                passengerBenchMarkPremium = PremiumInfo[2]['passengerBenchMarkPremium'][0]  #盗抢险的含税不计免赔保费
                passengerDutyQuota = PremiumInfo[1]['driverDutyBaoE'][0]  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['passengerBenchMarkPremium'], passengerBenchMarkPremium, company,disCount, passengerDutyQuota))
        connection.commit()
    except:
        connection.close()

    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['carNickPremium'] is not False:
                carNickPremium = PremiumInfo[0]['carNickPremium'][0] #盗抢险含税保费
                carNickQuota = PremiumInfo[1]['carNickBaoE'][0]  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['carNickPremium'], carNickPremium, company, disCount, carNickQuota))
            if PremiumInfo[2]['carNickBenchMarkPremium'] is not False:
                carNickBenchMarkPremium = PremiumInfo[2]['carNickBenchMarkPremium'][0]  #盗抢险的含税不计免赔保费
                carNickQuota = PremiumInfo[1]['carNickBaoE'][0]  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['carNickBenchMarkPremium'], carNickBenchMarkPremium, company,disCount, carNickQuota))
        connection.commit()
    except:
        connection.close()

    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['glassBrokenPremium'] is not False:
                glassBrokenPremium = PremiumInfo[0]['glassBrokenPremium'][0] #盗抢险含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['glassBrokenPremium'], glassBrokenPremium, company, disCount))
        connection.commit()
    except:
        connection.close()

    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['carFirePremium'] is not False:
                carFirePremium = PremiumInfo[0]['carFirePremium'][0] #盗抢险含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carFirePremium'], carFirePremium, company, disCount))
            if PremiumInfo[2]['carFireBrokenBenchMarkPremium'] is not False:
                carFireBrokenBenchMarkPremium = PremiumInfo[2]['carFireBrokenBenchMarkPremium'][0]  #盗抢险的含税不计免赔保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carFireBrokenBenchMarkPremium'], carFireBrokenBenchMarkPremium, company,disCount))
        connection.commit()
    except:
        connection.close()

    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0]['engineWadingPremium'] is not False:
                engineWadingPremium = PremiumInfo[0]['engineWadingPremium'][0] #盗抢险含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['engineWadingPremium'], engineWadingPremium, company, disCount))
            if PremiumInfo[2]['engineWadingBenchMarkPremium'] is not False:
                engineWadingBenchMarkPremium = PremiumInfo[2]['engineWadingBenchMarkPremium'][0]  #盗抢险的含税不计免赔保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['engineWadingBenchMarkPremium'], engineWadingBenchMarkPremium, company,disCount))
        connection.commit()
    except:
        connection.close()

    sql3 = "UPDATE insure_car SET PREMINU_START_DATE=%s,PREMINU_END_DATE=%s,CRAWL_DATE=%s,FLAG=1 WHERE INSURE_CAR_ID = %s"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql3, (startDate, endDate, str(datetime.datetime.now()), INSURE_CAR_ID))
        connection.commit()
    except:
        connection.close()








