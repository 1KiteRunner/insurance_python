import urlparse

data4 = 'http:www.baidu.com?channelNo=2&sessionId=7523bed2-4cc2-4249-8e4f-0f2e828c6501&proSelected=32000000&citySelected=32010000&carOwnerIdentifytype=&areaCodeLast=32000000&cityCodeLast=32010000&mobile=13888888888&email=22%40QQ.COM&identifytype=01&identifynumber=320125198610093122&birthday=1986%2F10%2F09&sex=2&startdate=2017-01-22&starthour=0&enddate=2018-01-21&endhour=24&isRenewal=0&licenseno=%E8%8B%8FAB3Q98&nonlocalflag=01&licenseflag=1&engineno=KL1392&vinno=LNBSCCAH3EF031577&frameno=LNBSCCAH3EF031577&newcarflag=0&isOutRenewal=0&lastHas050200=0&lastHas050210=0&lastHas050500=0&lastHas050291=&enrolldate=2014-12-26&transfervehicleflag=0&insuredname=%E6%9D%A8%E5%B0%8F%E9%A6%99&fullAmountName=&beforeProposalNo=&startDateCI=2017-02-19&starthourCI=0&endDateCI=2018-02-18&endhourCI=24&taxpayeridentno=&taxpayername=%E6%9D%A8%E5%B0%8F%E9%A6%99&taxtype=&certificatedate=&transferdate=2017%2F01%2F20&runAreaCodeName=&assignDriver=2&haveLoan=2&LoanName=&weiFaName=&seatCount=5&seatflag=1&carDrivers=&ccaFlag=&ccaID=&ccaEntryId=&travelMilesvalue=&isbuytax='


def url2dict(url):
    query=urlparse.urlparse(url).query
   # print(urlparse.parse_qs(query,1).items())
    return dict([(k,v[0]) for k,v in urlparse.parse_qs(query,1).items()])
print url2dict(data4)