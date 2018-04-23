# coding:utf8
from common.getSpecialType import get_specical_car_type
from common.log import Logger
from request_ancheng.settings import TEZHONGCHE_EXCEL

log = Logger()


def get_car_class(car_info):
    CPlateNo = car_info.get('CPlateNo', '')
    Vhl_CModelNme = car_info.get('Vhl_CModelNme', '')
    HAULAGE = car_info.get('HAULAGE', '0')
    LIMIT_LOAD = car_info.get('LIMIT_LOAD', '0')
    VEHICLE_CATEGORY = car_info.get('VEHICLE_CATEGORY', '')
    Vhl_CRegVhlTyp = car_info.get('Vhl_CRegVhlTyp', '')
    seats = car_info.get('seats', '')
    VEHICLE_STYLE = car_info.get("VEHICLE_STYLE", '')
    Vhl_NTonage = "0.000000"  # 吨位（获取）
    is_tezhongche = 0
    is_guache = 0

    code = VEHICLE_STYLE[0] if VEHICLE_STYLE else ''

    licenseType = car_info.get("licenseType", "02")
    if '挂' in CPlateNo:
        log.info('挂车 - {0}'.format(CPlateNo))
        is_guache = 1
        is_tezhongche = 1
        SY_Vhl_CUsageCde = '345019012'  # 挂车
        JQ_Vhl_CUsageCde = ''

        SY_Vhl_CBizMrk = '345018002'  # 营业以及特种车
        JQ_Vhl_CBizMrk = ''

        SY_Vhl_CVhlTyp = '345002032'  # 特种车一挂车（默认）
        JQ_Vhl_CVhlTyp = ''

        Vhl_NTonage = "0.000000"  # 吨位（获取）
        if len(HAULAGE) > len(LIMIT_LOAD):
            Vhl_NTonage_TMP = HAULAGE
        else:
            Vhl_NTonage_TMP = LIMIT_LOAD

        if isinstance(float(Vhl_NTonage_TMP), float):
            Vhl_NTonage = float(Vhl_NTonage_TMP) / 1000
            Vhl_NTonage = str(Vhl_NTonage)

        if float(Vhl_NTonage) >= 6:
            SY_Vhl_CMonDespRate = '0.009'
        else:
            SY_Vhl_CMonDespRate = '0.009'

        car_type = get_specical_car_type(Vhl_CModelNme)
        if car_type:
            type = car_type['type']
            if type == 'T1':
                SY_Vhl_CVhlTyp = '345002032'  # 特种车一挂车
            elif type == 'T2':
                SY_Vhl_CVhlTyp = '345002033'  # 特种车二挂车
            elif type == 'T3':
                SY_Vhl_CVhlTyp = '345002034'  # 特种车三挂车
            elif type == 'T4':
                SY_Vhl_CVhlTyp = '345002035'  # 特种车四挂车

    # 如果是货车或特种车
    elif licenseType == "01" or licenseType == "02" and code != 'K':

        Vhl_CVhlTyp = None
        # 匹配车辆编码
        if VEHICLE_CATEGORY:
            if VEHICLE_CATEGORY in ['21', '22', '23', '24']:
                is_tezhongche = 0

            # elif VEHICLE_CATEGORY in ['25', '26', '27', '28']:
            #     is_tezhongche = 1
            #     SY_Vhl_CUsageCde = '345019012'  # 挂车
            #     JQ_Vhl_CUsageCde = '345019012'  # 挂车
            elif VEHICLE_CATEGORY in ['31']:
                is_tezhongche = 1
                Vhl_CVhlTyp = '345002020'  # 特种车一
            elif VEHICLE_CATEGORY in ['40', '41']:
                is_tezhongche = 1
                Vhl_CVhlTyp = '345002021'  # 特种车二
            elif VEHICLE_CATEGORY in ['50', '51']:
                is_tezhongche = 1
                Vhl_CVhlTyp = '345002022'  # 特种车三
            elif VEHICLE_CATEGORY in ['60', '61']:
                is_tezhongche = 1
                Vhl_CVhlTyp = '345002023'  # 特种车四

        # 匹配EXCEL判断是不是特种车
        else:
            if Vhl_CRegVhlTyp in TEZHONGCHE_EXCEL:
                is_tezhongche = 1
                car_type = get_specical_car_type(Vhl_CModelNme)
                if car_type:
                    type = car_type['type']
                    if type == 'T1':
                        Vhl_CVhlTyp = '345002020'  # 特种车一
                    elif type == 'T2':
                        Vhl_CVhlTyp = '345002021'  # 特种车二
                    elif type == 'T3':
                        Vhl_CVhlTyp = '345002022'  # 特种车三
                    elif type == 'T4':
                        Vhl_CVhlTyp = '345002023'  # 特种车四

        if is_tezhongche:
            log.info(u'判断为是特种车 - {0}'.format(CPlateNo))
            SY_Vhl_CBizMrk = '345018002'  # 营业车及特种车
            JQ_Vhl_CBizMrk = '345009005'  # 营业个人

            SY_Vhl_CUsageCde = '345019009'  # 特种车
            JQ_Vhl_CUsageCde = '345010006'  # 特种车

            if not Vhl_CVhlTyp:
                log.error(u'无法获取特种车类型')
                return None

            SY_Vhl_CVhlTyp = Vhl_CVhlTyp
            JQ_Vhl_CVhlTyp = Vhl_CVhlTyp

            SY_Vhl_CMonDespRate = '0.009'

        else:
            log.info(u'判断为是货车 - {0}'.format(CPlateNo))

            SY_Vhl_CBizMrk = "345018002"  # 营业以及特种车
            JQ_Vhl_CBizMrk = "345009005"  # 营业个人

            SY_Vhl_CUsageCde = "345019008"  # 营业货车
            JQ_Vhl_CUsageCde = "345010004"  # 货车

            Vhl_NTonage = "0.000000"  # 吨位（获取）
            if len(HAULAGE) > len(LIMIT_LOAD):
                Vhl_NTonage_TMP = HAULAGE
            else:
                Vhl_NTonage_TMP = LIMIT_LOAD

            if isinstance(float(Vhl_NTonage_TMP), float):
                Vhl_NTonage = float(Vhl_NTonage_TMP) / 1000
                Vhl_NTonage = str(Vhl_NTonage)

            if float(Vhl_NTonage) >= 6:
                SY_Vhl_CMonDespRate = '0.009'
            else:
                SY_Vhl_CMonDespRate = '0.009'

            if float(Vhl_NTonage) >= 10:
                Vhl_CVhlTyp = "345002011"
            elif float(Vhl_NTonage) < 10 and float(Vhl_NTonage) >= 5:
                Vhl_CVhlTyp = "345002010"
            elif float(Vhl_NTonage) < 5 and float(Vhl_NTonage) > 2:
                Vhl_CVhlTyp = "345002009"
            else:
                Vhl_CVhlTyp = "345002008"

            SY_Vhl_CVhlTyp = Vhl_CVhlTyp  # 商 车辆种类细分
            JQ_Vhl_CVhlTyp = Vhl_CVhlTyp  # 交 车辆种类细分
            if float(
                    Vhl_NTonage) <= 1 and '物流' not in Vhl_CModelNme and '租赁' not in Vhl_CModelNme and '快递' not in Vhl_CModelNme:
                SY_Vhl_CBizMrk = "345018001"  # 非营业用车
                SY_Vhl_CUsageCde = "345019008"  # 非营业货车

            if float(
                    Vhl_NTonage) <= 1 and '物流' not in Vhl_CModelNme and '租赁' not in Vhl_CModelNme and '快递' not in Vhl_CModelNme:
                JQ_Vhl_CBizMrk = "345009001"  # 非营业用车

    else:
        log.info(u'判断为是小型车 - {0}'.format(CPlateNo))

        SY_Vhl_CBizMrk = "345018001"  # 非营业用车
        JQ_Vhl_CBizMrk = "345009001"  # 非营业个人

        SY_Vhl_CUsageCde = "345019001"  # 非营业个人客车
        JQ_Vhl_CUsageCde = "345010001"  # 客车

        if int(seats) <= 6:
            SY_Vhl_CVhlTyp = "345002001"
            JQ_Vhl_CVhlTyp = "345002001"
        elif int(seats) > 6 and int(seats) <= 10:
            SY_Vhl_CVhlTyp = "345002002"
            JQ_Vhl_CVhlTyp = "345002002"
        else:
            SY_Vhl_CVhlTyp = "345002003"
            JQ_Vhl_CVhlTyp = "345002003"

        SY_Vhl_CMonDespRate = '0.006'

    data = {
        'SY_Vhl_CBizMrk': SY_Vhl_CBizMrk,
        'JQ_Vhl_CBizMrk': JQ_Vhl_CBizMrk,

        'SY_Vhl_CUsageCde': SY_Vhl_CUsageCde,
        'JQ_Vhl_CUsageCde': JQ_Vhl_CUsageCde,

        'SY_Vhl_CVhlTyp': SY_Vhl_CVhlTyp,
        'JQ_Vhl_CVhlTyp': JQ_Vhl_CVhlTyp,

        'Vhl_NTonage': Vhl_NTonage,

        'is_tezhongche': is_tezhongche,
        'is_guache': is_guache,

        'SY_Vhl_CMonDespRate': SY_Vhl_CMonDespRate
    }

    log.info(u'获取车辆类型编码 - {data}'.format(data=data))
    return data
