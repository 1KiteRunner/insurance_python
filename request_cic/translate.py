# -*- coding:utf-8 -*-
def getPriumeInf(result):
    fee_flase_0 = lambda x: x if x != False else 0
    sy_disCount = float(result['SY']['SY_PrmCoef_NCoef']) if result['SY'][
                                                                 'SY_PrmCoef_NCoef'] != "" else False  # 商业险优惠系数
    jq_disCount = float(result['JQ']['JQ_PrmCoef_NCoef']) if result['JQ'][
                                                                 'JQ_PrmCoef_NCoef'] != "" else False  # 交强险的优惠系数

    Premium = {
        "compulsory_insurance": result['JQ']['JQ_Base_NPrm'] if result['JQ']['JQ_Base_NPrm'] is not "" else False,
        # 交强险
        "NAggTax": result['JQ']['VsTax_NAggTax'] if result['JQ']['VsTax_NAggTax'] is not "" else False,  # 车船税
        "carDamagePremium": round(float(fee_flase_0(result.get("036001", {}).get("NBefPrm", False))) * sy_disCount, 2),
        # 指定修理厂
        "repairFactoryPremium": round(float(fee_flase_0(result.get("036022", {}).get("NBefPrm", False))) * sy_disCount,
                                      2),
        # 车损险
        "carTheftPremium": round(float(fee_flase_0(result.get("036005", {}).get("NBefPrm", False))) * sy_disCount, 2),
        # 盗抢险
        "otherHurtPremium": round(float(fee_flase_0(result.get("036002", {}).get("NBefPrm", False))) * sy_disCount, 2),
        # 三者险
        "driverDutyPremium": round(float(fee_flase_0(result.get("036003", {}).get("NBefPrm", False))) * sy_disCount, 2),
        # 车上人员险（司机）
        "passengerDutyPremium": round(float(fee_flase_0(result.get("036004", {}).get("NBefPrm", False))) * sy_disCount,
                                      2),  # 车上人员险(乘客)
        "carNickPremium": round(float(fee_flase_0(result.get("036013", {}).get("NBefPrm", False))) * sy_disCount, 2),
        # 划痕险
        "glassBrokenPremium": round(float(fee_flase_0(result.get("036006", {}).get("NBefPrm", False))) * sy_disCount,
                                    2),  # 玻璃破碎险
        "carFirePremium": round(float(fee_flase_0(result.get("036007", {}).get("NBefPrm", False))) * sy_disCount, 2),
        # 自燃损失险
        "engineWadingPremium": round(float(fee_flase_0(result.get("036012", {}).get("NBefPrm", False))) * sy_disCount,
                                     2),  # 发动机涉水险
        "seatCount": ""
    }
    BaoE = {
        "carTheftBaoE": fee_flase_0(result.get("036005", {}).get("NAmt", False)),
        "carDamageBaoE": fee_flase_0(result.get("036001", {}).get("NAmt", False)),
        "otherHurtBaoE": fee_flase_0(result.get("036002", {}).get("NIndemLmt", False)),
        "driverDutyBaoE": fee_flase_0(result.get("036003", {}).get("NPerAmt", False)),
        "passengerDutyBaoe": fee_flase_0(result.get("036004", {}).get("NAmt", False)),
        "carNickBaoE": fee_flase_0(result.get("036013", {}).get("NIndemLmt", False))
    }

    MarkPremium = {
        "carDamageBenchMarkPremium": round(float(result.get("036001", {}).get("NDductPrm", False)) * sy_disCount, 2),
        # 车损险不计免赔
        "carTheftBenchMarkPremium": round(float(result.get("036005", {}).get("NDductPrm", False)) * sy_disCount, 2),
        # 盗抢险不计免赔
        "otherHurtBenchMarkPremium": round(float(result.get("036002", {}).get("NDductPrm", False)) * sy_disCount, 2),
        # 三者责任险的不计免赔
        "driverDutyBenchMarkPremium": round(float(result.get("036003", {}).get("NDductPrm", False)) * sy_disCount, 2),
        # 车上人员责任险（司机）不计免赔含税保费
        "passengerBenchMarkPremium": round(float(result.get("036004", {}).get("NDductPrm", False)) * sy_disCount, 2),
        # 车上人员责任险（乘客）不计免赔含税保费
        "carNickBenchMarkPremium": round(float(result.get("036013", {}).get("NDductPrm", False)) * sy_disCount, 2),
        # 划痕险不计免赔含税保费
        "carFireBrokenBenchMarkPremium": round(float(result.get("036007", {}).get("NDductPrm", False)) * sy_disCount,
                                               2),  # 自燃损失险不计免赔含税保费
        "engineWadingBenchMarkPremium": round(float(result.get("036012", {}).get("NDductPrm", False)) * sy_disCount, 2)
        # 发动机涉水险不计免赔含税保费
    }
    disCount = {
        "sy_disCount": sy_disCount,
        "jq_disCount": jq_disCount
    }
    Premium2 = {}
    BaoE2 = {}
    MarkPremium2 = {}
    disCount2 = {}
    for i in Premium:
        if Premium[i] != 0.0:
            Premium2[i] = Premium[i]

    for i in BaoE:
        if BaoE[i] != 0:
            BaoE2[i] = BaoE[i]

    for i in MarkPremium:
        if MarkPremium[i] != 0.0:
            MarkPremium2[i] = MarkPremium[i]
    for i in disCount:
        if disCount[i] != False:
            disCount2[i] = disCount[i]
    PremiumInfo = [Premium2, BaoE2, MarkPremium2, disCount2]
    return PremiumInfo


if __name__ == "__main__":
    # from test9 import jsobbody
    bod2 = {'SY': {'SY_Base_NNoTaxPrm': u'1770.78', 'SY_Base_NPrm': u'1877.03', 'SY_Base_NAddedTax': u'106.25',
                   'SY_PrmCoef_NCoef': u'0.7225', 'SY_Base_NAmt': u'635765.00'},
            'JQ': {'JQ_Base_NNoTaxPrm': u'716.98', 'VsTax_NAggTax': u'360.00', 'JQ_Base_NAmt': u'122000.00',
                   'JQ_Base_NPrm': u'760.00', 'JQ_Base_NAddedTax': u'43.02', 'JQ_PrmCoef_NCoef': u'0.8'},
            u'036003': {'NPureRiskPremium': u'26.000000', 'CCvrgNo': u'036003', 'NDductPrm': u'6',
                        'NNonDeductPureRiskPrm': u'3.90', 'NBefPrm': u'40.00', 'NPerAmt': u'10000', 'NPrm': u'33.24'},
            u'036002': {'NPureRiskPremium': u'1049.100000', 'CCvrgNo': u'036002', 'NDductPrm': u'242.1',
                        'NNonDeductPureRiskPrm': u'157.37', 'NIndemLmt': u'500000.00', 'NBefPrm': u'1614.00',
                        'NPrm': u'1341.04'},
            u'036005': {'NPureRiskPremium': u'312.138450', 'CCvrgNo': u'036005', 'NDductPrm': u'96.04',
                        'NAmt': u'85765.00', 'NNonDeductPureRiskPrm': u'62.43', 'NBefPrm': u'480.21',
                        'NPrm': u'416.34'},
            u'036004': {'NPureRiskPremium': u'67.600000', 'CCvrgNo': u'036004', 'NDductPrm': u'15.6', 'NAmt': 40000,
                        'NNonDeductPureRiskPrm': u'10.14', 'NBefPrm': u'104.00', 'NPrm': u'86.41'},
            u'033201': {'NPureRiskPremium': u'', 'CCvrgNo': u'033201', 'NDductPrm': u'', 'NAmt': u'122000.00',
                        'NNonDeductPureRiskPrm': u'', 'NBefPrm': u'950.00', 'NPrm': u'760.00'}}
    bod1 = {
        'SY': {
            'SY_Base_NNoTaxPrm': u'',
            'SY_Base_NPrm': u'',
            'SY_Base_NAddedTax': u'',
            'SY_PrmCoef_NCoef': u'',
            'SY_Base_NAmt': u''
        },
        u'033201': {
            'NPureRiskPremium': u'',
            'CCvrgNo': u'033201',
            'NDductPrm': u'',
            'NAmt': u'122000.00',
            'NNonDeductPureRiskPrm': u'',
            'NBefPrm': u'1100.00',
            'NPrm': u'880.00'
        },
        'JQ': {
            'JQ_Base_NNoTaxPrm': u'830.19',
            'VsTax_NAggTax': u'360.00',
            'JQ_Base_NAmt': u'122000.00',
            'JQ_Base_NPrm': u'880.00',
            'JQ_Base_NAddedTax': u'49.81',
            'JQ_PrmCoef_NCoef': u'0.8'
        }
    }
    # print getPriumeInf(bod2, 5)
    print getPriumeInf(bod1)
