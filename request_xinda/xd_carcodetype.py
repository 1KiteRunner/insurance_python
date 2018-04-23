# -*- coding:utf-8 -*-
__author__ = 'weikai'
import sys
from common.log import Logger

reload(sys)
sys.setdefaultencoding('utf-8')
# vin查询返回的险种|信达车辆类型描述|编号|common中自定义编号
# 1 　6座以下|2 6-10座 |3 10座以上|4 10-20座 | 5 20座以上 |6  2吨以下 | 7 2-5吨|8 5-10吨|9 10吨以上 |10 低速载货汽车 |11 20－36座|12 36座以上
car_type_list = [u"六座以下客车|6座以下|1|1",
                 u"六座至十座以下客车|6-10座|2|",
                 u"十座至二十座以下客车|10-20座|3|4",
                 u"二十座至三十六座以下客车|20-36座|4|11",
                 u"三十六座以上客车|36座以上|5|12",
                 u"二吨以下货车|2吨以下|6|6",
                 u"二吨至五吨以下货车|2-5吨|7|7",
                 u"五吨至十吨以下货车|5-10吨|8|8",
                 u"十吨以上货车|10吨以上|9|9",
                 u"|低速载货|10|10",
                 u"特种车一|特一|11",
                 u"特种车二|特二|12",
                 u"特种车三|特三|13",
                 u"特种车四|特四|14",
                 u"|特一挂|15",
                 u"|特二挂|16",
                 u"|特三挂|17",
                 u"|摩托车|18",
                 u"|拖拉机|19"
                 ]

log = Logger()


def get_car_type(syName):
    for i in car_type_list:
        if syName in i:
            type_list = i.split("|")
            return type_list


def get_bi_rate(permium_dict):
    '''
    :param permium_dict:
    :param expected:期望费率
    :return:
    '''
    # 商车费改优惠系数调整
    ClaimAdjustValueBI = permium_dict['SubmitBI']['ClaimAdjustValueBI']
    PeccancyAdjustValueBI = permium_dict['SubmitBI']['PeccancyAdjustValueBI']
    # 渠道系数
    channelRateBI = permium_dict['Rules']['sumChannelRateBI']
    adjustRateBI = permium_dict['Rules']['sumAdjustRateBI']
    # 总和实际费率
    rate = (float(ClaimAdjustValueBI) + 1) * (float(PeccancyAdjustValueBI) + 1) * (float(channelRateBI)) * (
        float(adjustRateBI))
    tonCountBC = permium_dict['vehicle']['tonCountBC']  # 质量
    insuranceType = permium_dict['insuranceType']
    otherHurtPremium = insuranceType.get("otherHurtPremium", {}).get("isCheck", "0")
    carDamagePremium = insuranceType.get("carDamagePremium", "0")
    filed_rate = 0.7225
    # rateFactorsTotalBI = permium_dict.get("Rules", {}).get("rateFactorsTotalBI", "")
    expected_rate = rate
    # 5吨以上，单三责 综合系数不得低于0.7；如车损+三责，综合系数不得低于0.6
    if float(tonCountBC) > 5.0 and otherHurtPremium == "1" and carDamagePremium == "0":
        expected_rate = 0.7
    elif float(tonCountBC) > 5.0 and otherHurtPremium == "1" and carDamagePremium == "1":
        expected_rate = 0.6
        # 其他规则另行增加
    if expected_rate > rate:
        rate = expected_rate
        filed_rate = rate / ((float(ClaimAdjustValueBI) + 1) * (float(PeccancyAdjustValueBI) + 1))
        if filed_rate > 1.3225:
            filed_rate = 1.3225
        if filed_rate < 0.8500:
            adjustRateBI = 0.8500
            channelRateBI = round(filed_rate / (float(adjustRateBI)), 4)
        elif filed_rate > 1.1500:
            adjustRateBI = 1.1500
            channelRateBI = round(filed_rate / (float(adjustRateBI)), 4)
        else:
            adjustRateBI = 1.0000
            channelRateBI = filed_rate
        log.info("filed_rate = %s ,channelRateBI = %s ,adjustRateBI =%s,discountBI = %s ", expected_rate, channelRateBI,
                 adjustRateBI, (float(ClaimAdjustValueBI) + 1) * (float(PeccancyAdjustValueBI) + 1))
        permium_dict['Rules']['sumChannelRateBI'] = channelRateBI
        permium_dict['Rules']['sumAdjustRateBI'] = adjustRateBI
        permium_dict['Rules']['rateFactorsTotalBI'] = filed_rate


if __name__ == "__main__":
    print get_car_type('六座以下客车')
    mais = {
        'Rules': {'rateFactorsTotalBI': u'0.7225', 'channelLowerRateBI': u'1.0000', 'rateFactorsTotalMaxBI': u'2.2041',
                  'sumAdjustRateBI': u'0.8500', 'channelRateBI': 1.1462, 'adjustTopRateBI': u'2.2041',
                  'rateFactorsTotalOriginBI': u'0.7225',
                  'RateFactorsImfTemp': u'\u5728\u6211\u53f8\u7eed\u4fdd\u5e74\u9650@_@1.1@_@0.9@_@\u65b0\u8f66\u3001\u5e73\u53f0\u65b0\u4fdd\u3001\u8f6c\u4fdd\u53ca\u5176\u4ed6@_@A2-\u5728\u6211\u53f8\u7eed\u4fdd\u5e74\u9650|_|\u5173\u8054\u4ea4\u5f3a\u9669\u4fdd\u5355NCD@_@1.2@_@1.0@_@\u4e24\u4e2a\u5e74\u5ea6\u672a\u53d1\u751f\u6709\u8d23\u4efb\u9053\u8def\u4ea4\u901a\u4e8b@_@A7-\u5173\u8054\u4ea4\u5f3a\u9669\u4fdd\u5355NCD|_|\u5546\u4e1a\u9669\u9669\u522b\u7ec4\u5408@_@1.2@_@1.0@_@\u540c\u4fdd\u8f66\u635f+\u4e09\u8005@_@A1-\u5546\u4e1a\u9669\u9669\u522b\u7ec4\u5408|_|\u65e0\u8d54\u6b3e\u4f18\u5f85@_@1.15@_@0.95@_@\u8fde\u7eed2\u5e74\u6ca1\u6709\u53d1\u751f\u8d54\u6b3e@_@A6-\u65e0\u8d54\u6b3e\u4f18\u5f85|_|\u8f66\u8f86\u79cd\u7c7b@_@1.1@_@0.9@_@\u666e\u901a\u8f7d\u8d27@_@A5-\u8f66\u8f86\u79cd\u7c7b|_|\u4f7f\u7528\u6027\u8d28@_@1.1@_@0.9@_@\u8425\u4e1a\u8d27\u8fd0@_@A4-\u4f7f\u7528\u6027\u8d28|_|\u5428\u4f4d\u6570@_@1.0@_@0.85@_@5-10\u5428@_@A3-\u5428\u4f4d\u6570',
                  'sumChannelRateBI': u'0.8500', 'adjustRateBI': u'0.8500', 'additionalCostRateBI': u'0.3500',
                  'adjustLowerRateBI': u'0.5887', 'rateFactorsTotalMinBI': u'0.5887', 'deductiblesCoefficient': u'1.0',
                  'channelTopRateBI': u'1.0000'}, 'jq_insuranceEndTime': '2017-06-27',
        'carVinInfo': {'completeKerbMassNewBC': u'5515', 'exhaustScaleBC': u'4.752', 'cartonnage': u'9.99',
                       'compromisePrice': u'114000.0',
                       'syName': u'\u4e94\u5428\u81f3\u5341\u5428\u4ee5\u4e0b\u8d27\u8f66', 'carKindCodeBC': 'H0',
                       'brandNameBC': u'\u4e1c\u98ceDFL1160BX9\u8f7d\u8d27\u6c7d\u8f66', 'BrandCode': u'DFCKKD0088',
                       'carclassName': u'', 'seatCountBC': u'3', 'VEHICLEMODEL': u'DFL1160BX9', 'useNatureCodeBC': '9D',
                       'jqName': u'\u4e94\u5428\u81f3\u5341\u5428\u4ee5\u4e0b\u8d27\u8f66', 'mainCarKindCodeBC': 'H'},
        'SubmitBI': {'PeccancyAdjustReasonBI': u'\u65e0\u8fdd\u6cd5\u4fe1\u606f;', 'lossConditionCodeBI': u'02',
                     'PeccancyAdjustValueBI': u'-0.1', 'ClaimAdjustValueBI': u'-0.3',
                     'lossConditionBI': u'2\u5e74\u672a\u51fa\u9669', 'illegal_list': '',
                     'modelCodeBC': u'BDFRTKUA0225', 'comLossConditionBI': u'2\u5e74\u672a\u51fa\u9669',
                     'ClaimAdjustReasonBI': u'\u65e0\u8d54\u6b3e\u4f18\u5f85-\u8fde\u7eed2\u5e74\u6ca1\u6709\u53d1\u751f\u8d54\u6b3e',
                     'claimInfoSize': u'0', 'comLossConditionCI': u'2\u5e74\u672a\u51fa\u9669',
                     'query_codeBI': u'PDCXC01XDCXJS1701495696630020523', 'pureRiskPremium': u'2572.434800',
                     'query_sequence_noBI': u'V0101XDCX320017001495697137720'},
        'insuranceType': {'driverDutyPremium': {'Amount': '10000', 'isCheck': '0'}, 'carDamagePremium': '1',
                          'otherHurtBenchMarkPremium': '1', 'passengerBenchMarkPremium': '0',
                          'compulsoryInsurance': '1', 'carFirePremium': '0',
                          'otherHurtPremium': {'Amount': '1000000', 'isCheck': '1'},
                          'repairFactoryPremium': {'rate': '', 'isCheck': '0'}, 'engineWadingBenchMarkPremium': '0',
                          'insuranceTypeGroupId': '1541', 'carFireBrokenBenchMarkPremium': '0', 'nAggTax': '1',
                          'carDamageBenchMarkPremium': '1', 'passengerDutyPremium': {'Amount': '10000', 'isCheck': '0'},
                          'driverDutyBenchMarkPremium': '0', 'carTheftBenchMarkPremium': '0',
                          'carNickPremium': {'Amount': '', 'isCheck': '0'},
                          'insuranceTypeGroup': '1_12_2_20_3_30_5_50_6_60', 'glassBrokenPremium': '0',
                          'carNickBenchMarkPremium': '0', 'engineWadingPremium': '0', 'carTheftPremium': '0'},
        'actualValue': {'printBrandNameBC': u'24966.0', 'carKind': u'\u8f7d\u8d27\u6c7d\u8f66',
                        'riskPremium': u'2572.434800', 'useYears': '5', 'actualValueBC': u'24966.0',
                        'modelCodeBC': u'BDFRTKUA0225', 'searchSequenceNoBC': u'BDFRTKUA022510A1'},
        'vehicle': {'appliNatureBC': '4', 'vehicle_brand_2CI': u'\u4e1c\u98ce\u724c', 'countryNatureBC': u'A',
                    'carTypeCodeBC': u'8', 'insuredNatureBC': '4', 'seatCountBC': '0', 'tonCountBC': u'9.99',
                    'CheckCodeJS': u'cr52', 'completeKerbMassNewBC': u'5515', 'licenseKindCodeBC': u'01',
                    'carOwnerBC': u'\u6c5f\u9634\u5e02\u5927\u80dc\u7269\u6d41\u6709\u9650\u516c\u53f8',
                    'licenseCategoryBC': 'H21', 'carOwnerNature1BC': '2', 'myCarTypeCodeBC': u'8',
                    'CheckNoJS': u'72XDCX320017001495697117036615', 'carOwnerIdentifyTypeCI': '10',
                    'EngineNo': u'B3000332', 'pmUseNatureCodeBC': u'F', 'vehicle_modelCI': u'DFL1160BX9',
                    'exhaustScaleBC': u'4.752', 'vehicleBrandTemp': u'\u4e1c\u98ce\u724c',
                    'licenseNoBC': u'\u82cfBD1566', 'enrollDateBC': u'2011-06-30',
                    'madeFactoryBI': u'\u4e1c\u98ce\u6c7d\u8f66\u6709\u9650\u516c\u53f8',
                    'frameNoBC': u'LGAC2A132B1008021'}, 'sy_insuranceEndTime': '2017-06-27',
        'query_sequence_noCI': u'01XDCX320017001495697130335686'}
    print get_bi_rate(mais)
