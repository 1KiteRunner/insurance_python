# -*- coding:utf-8 -*-
__author__ = 'weikai'
import  request_epicc.settings as se
import requests
import urllib
import  time
import datetime
def getlatedate(i,str_date=''):
    if str_date=='':
        nowdate = datetime.date.today()#
        tomorrow = nowdate + datetime.timedelta(days=i)
        return str(tomorrow)
    else:
        str_date=datetime.datetime.strptime(str_date,"%Y-%m-%d").date()
        tomorrow = str_date + datetime.timedelta(days=i)
        return str(tomorrow)


def get_jq_epicc(dt):
    try:
        headers=se.headers
        jq_url='http://www.epicc.com.cn/wap/carProposal/calculateFee/jq'
        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/calculateFee'
        licenseno=dt['licenseno']
        identifynumber=dt['identifynumber']
        startDateCI=dt['startDateCI']
        proSelected=areaCodeLast=dt['proSelected']
        startdate=dt['startdate']
        vinno=frameno=dt['frameno']
        cityCodeLast=citySelected=dt['cityCodeLast']
        endDateCI=dt['endDateCI']
        enddate=dt['enddate']
        transferdate=dt['transferdate']
        enrolldate=dt['enrolldate']
        birthday=dt['birthday']
        engineno=dt['engineno']
        taxpayername=insuredname=dt['insuredname']
        sessionId=dt['sessionId']
        sex=dt['sex']
        seatCount=dt['seatCount']
        jq_body={
            "haveLoan": "2",
            "licenseno": licenseno,
            "endhourCI": "24",
            "ccaEntryId": "",
            "identifynumber": identifynumber,
            "weiFaName": "",
            "lastHas050500": "0",
            "beforeProposalNo": "",
            "sex": sex,
            "taxtype": "",
            "isRenewal": "0",
            "startDateCI": startDateCI,
            "proSelected": proSelected,
            "nonlocalflag": "01",
            "ccaID": "",
            "startdate": startdate,
            "endhour": "24",
            "vinno": vinno,
            "citySelected": citySelected,
            "lastHas050210": "0",
            "insuredname": insuredname,
            "carOwnerIdentifytype": "",
            "areaCodeLast": areaCodeLast,
            "sessionId": sessionId,
            "lastHas050200": "0",
            "licenseflag": "1",
            "taxpayername": taxpayername,
            "isOutRenewal": "0",
            "email": "22@QQ.COM",
            "isbuytax": "",
            "ccaFlag": "",
            "frameno": frameno,
            "fullAmountName": "",
            "channelNo": "2",
            "assignDriver": "2",
            "seatCount": seatCount,
            "LoanName": "",
            "lastHas050291": "",
            "cityCodeLast": cityCodeLast,
            "endDateCI": endDateCI,
            "starthourCI": "0",
            "enddate": enddate,
            "transferdate": transferdate,
            "mobile": "13888888888",
            "transfervehicleflag": "0",
            "identifytype": "01",
            "certificatedate": "",
            "travelMilesvalue": "",
            "seatflag": "1",
            "enrolldate": enrolldate,
            "birthday": birthday,
            "engineno": engineno,
            "runAreaCodeName": "",
            "carDrivers": "",
            "newcarflag": "0",
            "taxpayeridentno": "",
            "starthour": "0"
        }

        jq_rep=requests.post(url=jq_url,data=urllib.urlencode(jq_body),headers=headers)
        jq_rep_json=jq_rep.json()
        jq={}
        if jq_rep_json.has_key('message'):
            if "/" in jq_rep_json['message']:
                jq_body['startDateCI']=jq_rep_json['message'][1:].replace("/","-")
                jq_body['endDateCI']=getlatedate(364,jq_body['startDateCI'])
                jq_resp=requests.post(url=jq_url,data=urllib.urlencode(jq_body),headers=headers)
                jq_resp=jq_resp.json()
                if jq_resp.has_key('premiumBZ'):
                    jq['jq_startdate']=jq_body['startDateCI']
                    jq['jq_enddate']=jq_body['endDateCI']
                    jq['premiumBZ']=jq_resp['premiumBZ']
                    jq['thisPayTax']=jq_resp['thisPayTax']
                    return jq
            else:
                return None
                print(u" %s 交强险查询失败,消息不正确" % licenseno)

        elif jq_rep_json.has_key('premiumBZ'):
            jq['jq_startdate']=dt['startDateCI']
            jq['jq_enddate']=dt['startDateCI']
            jq['premiumBZ']=jq_rep_json['premiumBZ']
            jq['thisPayTax']=jq_rep_json['thisPayTax']
            return jq
    except Exception as e:
        print(e)

