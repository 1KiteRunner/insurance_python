# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
import logging
from twisted.internet import defer, task
from stompest.config import StompConfig
from stompest.async import Stomp
from stompest.async.listener import ReceiptListener
import settings as se


class Producer(object):
    test = '/queue/test'
    QUEUE = '/queue/FILL_UP_QUEUE'
    FILL_UP_QUEUE = '/queue/FILL_UP_QUEUE'
    PICC_QUEUE = '/queue/PICC_QUEUE'
    CHINA_CONTINENT_QUEUE = '/queue/CHINA_CONTINENT_QUEUE'
    CHINA_JOINT_QUEUE = '/queue/CHINA_JOINT_QUEUE'
    COMPLETE_PLATE_NUMBER = "/queue/COMPLETE_PLATE_NUMBER"

    def __init__(self, config=None):
        if config is None:
            config = StompConfig('tcp://127.0.0.1:61613')
            # config = StompConfig('tcp://52.80.31.10:61613')
        self.config = config

    @defer.inlineCallbacks
    def run(self, _):
        client = Stomp(self.config)
        yield client.connect()
        client.add(ReceiptListener(1.0))

        dd8 = [{'insureCarId': 3797, 'firstRegister': u'', 'cityCode': '32010000', 'vinNo': u'LVBV6PDC7AH017644',
                'plateNumber': u'苏A90198', 'vehicleBrand': u'', 'companyId': ['12'], 'licenseType': '01',
                'custName': u'\u9648\u7fe0\u7ea2', 'insuranceType': [{u'carDamageBenchMarkPremium': u'1',  # 车损险不计免赔
                                                                      u'carDamagePremium': u'1',  # 车损险

                                                                      u'driverDutyPremium': {u'Amount': u'10000',
                                                                                             u'isCheck': u'0'},
                                                                      # 车上人员险（司机）
                                                                      u'driverDutyBenchMarkPremium': u'0',
                                                                      # 车上人员险（司机）不计免赔

                                                                      u'passengerDutyPremium': {u'Amount': u'10000',
                                                                                                u'isCheck': u'0'},
                                                                      # 车上人员险（乘客）
                                                                      u'passengerBenchMarkPremium': u'0',
                                                                      # 车上人员险（乘客）不计免赔

                                                                      u'carFirePremium': u'0',  # 自燃险
                                                                      u'carFireBrokenBenchMarkPremium': u'0',  # 自燃险不计免赔

                                                                      u'carTheftPremium': u'0',  # 盗抢险
                                                                      u'carTheftBenchMarkPremium': u'0',  # 盗抢险不计免赔

                                                                      u'otherHurtPremium': {u'Amount': u'1000000',
                                                                                            u'isCheck': u'1'},  # 三者险
                                                                      u'otherHurtBenchMarkPremium': u'1',  # 三者险不计免赔

                                                                      u'engineWadingPremium': u'0',  # 涉水险
                                                                      u'engineWadingBenchMarkPremium': u'0',  # 涉水险不计免赔

                                                                      u'carNickPremium': {u'Amount': u'2000',
                                                                                          u'isCheck': u'0'},  # 划痕险
                                                                      u'carNickBenchMarkPremium': u'0',  # 划痕险不计免赔

                                                                      u'nAggTax': u'1',

                                                                      u'insuranceTypeGroupId': u'183',

                                                                      u'glassBrokenPremium': u'0',  # 玻璃破碎险
                                                                      u'compulsoryInsurance': u'1',
                                                                      u'insuranceTypeGroup': u'1_11_110_12_2_20_3_30_4_5_50_6_8_20000_80_9'}, ],
                'sessionId': u'2bbcd99cd95d9b8fdf98b29e163686f6bca30736', 'engineNo': u'0651004', 'NSeatNum': u'5',
                'identitCard': u'320121197607280023', 'endDate': u'2017-04-7', 'isPhone': u'1'}, ]

        # yield client.send('/queue/COMPLETE_PLATE_NUMBER', json.dumps(dd8).encode())
        # yield client.send('/queue/BATCH_ANCHENG_QUEUE', json.dumps(dd8).encode())
        yield client.send('/queue/REAL_TIME_QUEUE', json.dumps(dd8).encode())
        # yield client.send('/queue/BATCH_ANCHENG_QUEUE', json.dumps(dd8).encode())
        # yield client.send('/queue/BATCH_PROCESS_QUEUE', json.dumps(dd8).encode())

        client.disconnect()
        yield client.disconnected  # graceful disconnect: waits until all receipts have arrived


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    task.react(Producer().run)
