# -*- coding:utf-8 -*-
import pymysql.cursors
import datetime
import  common.config as conf
def soupDb(PremiumInfo,data):
    connection = pymysql.connect(host=conf.MYSQLHOST,
                                 user=conf.MYSQLUSER,
                                 password=conf.MYSQLPASSWORD,
                                 db=conf.MYSQLDB,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    #data=[开始时间,结束时间，座位数，组合id，车辆id，公司id]
    startDate = data[0]#保险开始时间
    endDate = data[1]#保险结束时间
    seatQuantity = int(data[2])#座位数
    INSURANCE_TYPE_GROUP_ID=data[3] #组合id
    INSURE_CAR_ID=str(data[4]) #车辆id
    company=data[5] #公司id

    disCount = float(PremiumInfo[3].get('sy_disCount','0'))
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
    insurance_type = {
        'compulsory_insurance': '1',
        'carDamagePremium': '2',
        'otherHurtPremium': '3',
        'carTheftPremium': '4',
        'driverDutyPremium': '5',
        'passengerDutyPremium': '6',
        'glassBrokenPremium': '7',
        'carNickPremium': '8',
        'carFirePremium': '9',
        'engineWadingPremium': '11',
        'NAggTax': '12',
        'repairFactoryPremium': '13',
        'carDamageBenchMarkPremium': '20',
        'otherHurtBenchMarkPremium': '30',
        'carTheftBenchMarkPremium': '40',
        'driverDutyBenchMarkPremium': '50',
        'passengerBenchMarkPremium': '60',
        'carNickBenchMarkPremium': '80',
        'carFireBrokenBenchMarkPremium': '90',
        'engineWadingBenchMarkPremium': '110'
    }
    #company = insurance_company['中国人保车辆保险']
    sql1 = "INSERT INTO `car_premium` (`INSURE_CAR_ID`, `INSURANCE_TYPE_ID`,`PREMIUM`,`COMPANY_ID`,`DISCOUNT_RATE`,`INSURANCE_TYPE_GROUP_ID`) VALUES (%s, %s, %s, %s, %s,%s)"
    sql2 = "INSERT INTO `car_premium` (`INSURE_CAR_ID`, `INSURANCE_TYPE_ID`,`PREMIUM`,`COMPANY_ID`,`DISCOUNT_RATE`,`BAO_E`,`INSURANCE_TYPE_GROUP_ID`) VALUES (%s, %s, %s, %s, %s, %s,%s)"

    try:
        with connection.cursor() as cursor:
            if PremiumInfo[0].get("compulsory_insurance",None) is not None:
                jq_disCount = float(PremiumInfo[3]['jq_disCount'])
                compulsory_insurance = PremiumInfo[0]['compulsory_insurance']  # 交强险
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['compulsory_insurance'], compulsory_insurance, company,jq_disCount,INSURANCE_TYPE_GROUP_ID))


            if PremiumInfo[0].get("compulsory_insurance",None) is not None:
                NAggTax = PremiumInfo[0]['NAggTax']  # 车船税
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['NAggTax'], NAggTax, company, 1.0,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get("carDamagePremium",None) is not None:
                carDamagePremium = PremiumInfo[0]['carDamagePremium']  # 车损险含税保费
                carDamageQuota = PremiumInfo[1]['carDamageBaoE']
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['carDamagePremium'], carDamagePremium, company, disCount, carDamageQuota,INSURANCE_TYPE_GROUP_ID))
            if PremiumInfo[2].get("carDamageBenchMarkPremium",None) is not None:
                carDamageBenchMarkPremium = PremiumInfo[2]['carDamageBenchMarkPremium'] # 车损险不计免赔含税保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carDamageBenchMarkPremium'], carDamageBenchMarkPremium,company, disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get("driverDutyPremium",None) is not None:
                driverDutyPremium = PremiumInfo[0]['driverDutyPremium'] #司机座位险
                driverDutyQuota = PremiumInfo[1]['driverDutyBaoE'] # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['driverDutyPremium'], driverDutyPremium, company, disCount, driverDutyQuota,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[2].get("driverDutyBenchMarkPremium",None) is not None:
                driverDutyBenchMarkPremium = PremiumInfo[2]['driverDutyBenchMarkPremium']  #盗抢险的含税不计免赔保费
                driverDutyQuota = PremiumInfo[1]['driverDutyBaoE']  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['driverDutyBenchMarkPremium'], driverDutyBenchMarkPremium, company,disCount, driverDutyQuota,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get('passengerDutyPremium',None) is not None:
                passengerDutyPremium = PremiumInfo[0]['passengerDutyPremium'] #车上人员责任险（乘客）含税保费
                passengerDutyQuota = PremiumInfo[1]['passengerDutyBaoe']  # 车上人员责任险（乘客）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['passengerDutyPremium'], passengerDutyPremium, company, disCount, passengerDutyQuota,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[2].get("passengerBenchMarkPremium",None) is not None:
                passengerBenchMarkPremium = PremiumInfo[2]['passengerBenchMarkPremium']  #车上人员责任险（乘客）含税保费不计免赔
                passengerDutyQuota = PremiumInfo[1]['passengerDutyBaoe']  # 车上人员责任险（司机）额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['passengerBenchMarkPremium'], passengerBenchMarkPremium, company,disCount, passengerDutyQuota,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get("otherHurtPremium",None) is not None:
                otherHurtPremium = PremiumInfo[0]['otherHurtPremium']  # 三者责任险的含税保费
                if seatQuantity < 7:
                    otherHurtPremium = {'50000': '432.90', '100000': '624.65', '150000': '713.05', '200000': '774.15','300000': '874.25', '500000': '1049.10', '1000000': '1366.30','1500000': '1568.35', '2000000': '1742.49', '3000000': '2080.32','5000000': '2735.09'}
                elif seatQuantity < 11:
                    otherHurtPremium = {'50000': '400.40', '100000': '564.85', '150000': '638.30', '200000': '688.35','300000': '770.90', '500000': '917.80', '1000000': '1195.35','1500000': '1372.06', '2000000': '1524.41', '3000000': '1819.97','5000000': '2392.81'}
                for (d, x) in otherHurtPremium.items():
                    m = round(float(x) / 0.65 * float(disCount),2)
                    cursor.execute(sql2,(INSURE_CAR_ID, insurance_type['otherHurtPremium'], m, company, disCount, d,INSURANCE_TYPE_GROUP_ID))



            if  PremiumInfo[2].get("otherHurtBenchMarkPremium",None) is not None:
                if seatQuantity < 7:
                    otherHurtPremium = {'50000': '432.90', '100000': '624.65', '150000': '713.05', '200000': '774.15','300000': '874.25', '500000': '1049.10', '1000000': '1366.30','1500000': '1568.35', '2000000': '1742.49', '3000000': '2080.32','5000000': '2735.09'}
                elif seatQuantity < 11:
                    otherHurtPremium = {'50000': '400.40', '100000': '564.85', '150000': '638.30', '200000': '688.35','300000': '770.90', '500000': '917.80', '1000000': '1195.35','1500000': '1372.06', '2000000': '1524.41', '3000000': '1819.97','5000000': '2392.81'}
                otherHurtBenchMarkRate = 15
                for (d, x) in otherHurtPremium.items():
                    n = round(float(x) / 0.65 * float(disCount) * float(otherHurtBenchMarkRate) / 100,2)
                    cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['otherHurtBenchMarkPremium'], n, company, disCount, d,INSURANCE_TYPE_GROUP_ID))



            if PremiumInfo[0].get("repairFactoryPremium",None) is not None:
                repairFactoryPremium = PremiumInfo[0]['repairFactoryPremium']  # 指定修理厂
                cursor.execute(sql1,(INSURE_CAR_ID, insurance_type['repairFactoryPremium'], repairFactoryPremium, company, disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get("carFirePremium",None) is not None:
                carFirePremium = PremiumInfo[0]['carFirePremium']  # 自燃险
                cursor.execute(sql1,(INSURE_CAR_ID, insurance_type['carFirePremium'], carFirePremium, company, disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[2].get("carFireBrokenBenchMarkPremium",None) is not None:
                carFireBrokenBenchMarkPremium = PremiumInfo[2]['carFireBrokenBenchMarkPremium']  #自燃险不计免赔
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carFireBrokenBenchMarkPremium'], carFireBrokenBenchMarkPremium, company,disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get('carNickPremium',None) is not None:
                carNickPremium = PremiumInfo[0]['carNickPremium']  # 划痕险
                carNickQuota = PremiumInfo[1]['carNickBaoE']  # 划痕险额度
                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['carNickPremium'], carNickPremium, company, disCount, carNickQuota,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[2].get("carNickBenchMarkPremium",None) is not None:
                carNickBenchMarkPremium = PremiumInfo[2]['carNickBenchMarkPremium']  #划痕险不计免赔
                carNickQuota = PremiumInfo[1]['carNickBaoE']  # 划痕险额度

                cursor.execute(sql2, (INSURE_CAR_ID, insurance_type['carNickBenchMarkPremium'], carNickBenchMarkPremium, company,disCount, carNickQuota,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get("glassBrokenPremium",None) is not None:
                glassBrokenPremium = PremiumInfo[0]['glassBrokenPremium']  # 玻璃破碎险
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['glassBrokenPremium'], glassBrokenPremium, company, disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get("carTheftPremium",None) is not None:
                carTheftPremium = PremiumInfo[0]['carTheftPremium']  # 盗抢险含税保费
                cursor.execute(sql1,(INSURE_CAR_ID, insurance_type['carTheftPremium'], carTheftPremium, company, disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[2].get("carTheftBenchMarkPremium",None) is not None:
                carTheftBenchMarkPremium = PremiumInfo[2]['carTheftBenchMarkPremium']  # 盗抢险的含税不计免赔保费
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['carTheftBenchMarkPremium'], carTheftBenchMarkPremium, company, disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[0].get("engineWadingPremium",None) is not None:
                engineWadingPremium = PremiumInfo[0]['engineWadingPremium'] #发动机涉水险
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['engineWadingPremium'], engineWadingPremium, company, disCount,INSURANCE_TYPE_GROUP_ID))

            if PremiumInfo[2].get("engineWadingBenchMarkPremium",None) is not None:
                engineWadingBenchMarkPremium = PremiumInfo[2]['engineWadingBenchMarkPremium']  #发动机涉水险不计免赔
                cursor.execute(sql1, (INSURE_CAR_ID, insurance_type['engineWadingBenchMarkPremium'], engineWadingBenchMarkPremium, company,disCount,INSURANCE_TYPE_GROUP_ID))

            sql3 = "UPDATE insure_car SET CRAWL_DATE=%s,FLAG=1 WHERE INSURE_CAR_ID = %s"
            cursor.execute(sql3, ( str(datetime.datetime.now()), INSURE_CAR_ID))

        connection.commit()
    except Exception,e:
        import traceback
        print traceback.format_exc()
        connection.close()

if __name__=="__main__":
    data=["2010-11-11","2010-11-11","5","555","13111","13"]
    startDate = data[0]#保险开始时间
    endDate = data[1]#保险结束时间
    seatQuantity = int(data[2])#座位数
    INSURANCE_TYPE_GROUP_ID=data[3] #组合id
    INSURE_CAR_ID=str(data[4]) #车辆id
    company=data[5] #公司id
    dd=[{'driverDutyPremium': 64.97, 'otherHurtPremium': 1008.27, 'passengerDutyPremium': 24.99, 'carDamagePremium': 671.01, 'compulsory_insurance': 665.0, 'carTheftPremium': 126.68, 'carNickPremium': 381.07, 'seatCount': u'5', 'engineWadingPremium': 33.55, 'NAggTax': 300, 'glassBrokenPremium': 36.56, 'carFirePremium': 36.94}, {'carTheftBaoE': 19712, 'passengerDutyBaoe': 10000.0, 'otherHurtBaoE': 500000.0, 'driverDutyBaoE': 40000, 'carNickBaoE': 2000.0, 'carDamageBaoE': 19712}, {'carDamageBenchMarkPremium': 100.65, 'driverDutyBenchMarkPremium': 9.75, 'otherHurtBenchMarkPremium': 151.24, 'carTheftBenchMarkPremium': 25.34, 'engineWadingBenchMarkPremium': 5.04, 'carNickBenchMarkPremium': 57.16, 'passengerBenchMarkPremium': 3.75, 'carFireBrokenBenchMarkPremium': 7.39}, {'jq_disCount': u'0.624752', 'sy_disCount': 0.7}]

    soupDb(dd,data)










