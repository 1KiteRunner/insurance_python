# -*- coding:utf-8 -*-
import urllib
import pickle
import codecs
import time
import json
import datetime

from bs4 import BeautifulSoup

from common.sessionUtil import get_session


def xubao(licenseNo):
    try:
        startDate = datetime.date.today() + datetime.timedelta(1)
        # endDate = (str(startDate.year+1)+'-'+str(startDate.month)+'-'+str(startDate.day))
        endDateSY1 = (str(startDate.year + 1) + '-' + str(startDate.month) + '-' + str(startDate.day))
        endDateSY = datetime.datetime.strptime(endDateSY1, "%Y-%m-%d").date() + datetime.timedelta(-1)
        today = datetime.date.today()
        srssion = get_session('2')
        sessBase = srssion
        req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
        mydata = "prpCrenewalVo.policyNo=&prpCrenewalVo.othFlag=&prpCrenewalVo.engineNo=&prpCrenewalVo.frameNo=&prpCrenewalVo.vinNo=&prpCrenewalVo.licenseNo="+urllib.quote(licenseNo.encode('gb2312'))+"&prpCrenewalVo.licenseColorCode=&prpCrenewalVo.licenseType=02"
        data = req_session.post("http://10.134.136.112:8000/prpall/business/selectRenewal.do?pageSize=10&pageNo=1",data=mydata)
        carData = data.json()['data']
        if len(carData)==0:
            return 0
        for car in  carData:
            car['endDate'] = car['endDate']['time']
        carData.sort(key=lambda obj: obj.get('endDate'))
        bizNo = carData[len(carData)-1]['policyNo']
        res = req_session.post("http://10.134.136.112:8000/prpall/business/editCheckRenewal.do?bizNo="+bizNo)
        proposalNo = res.json()['data'][0]['proposalNo']
        editType = "COPY_PROPOSAL"
        if proposalNo is None:
            editType = "RENEWAL"
            proposalNo = bizNo
        url = "http://10.134.136.112:8000/prpall/business/editCitemCar.do?editType="+editType+"&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+str(startDate)+"&endDate="+str(endDateSY)+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+str(today)+"&motorFastTrack=&operatorProjectCode=&reload=&rnd934="
        carRes = req_session.get(url)
        soup =  BeautifulSoup(carRes.content, "html.parser")
        carDic = {}
        carDic['brandName'] = soup.find(id="prpCitemCar.brandName").get('value').encode('latin1').decode('gbk')#车辆型号
        carDic['enrollDate'] = soup.find(id="prpCitemCar.enrollDate").get('value')#注册时间
        carDic['engineNo'] = soup.find(id="prpCitemCar.engineNo").get('value')#发动机号
        carDic['vinNo'] = soup.find(id="prpCitemCar.vinNo").get('value')  # 车架号
        carDic['licenseNo'] = soup.find(id='prpCitemCar.licenseNo').get('value').encode('latin1').decode('gbk')#车牌号
        carDic['endDate'] = time.strftime("%Y-%m-%d",time.localtime(int(carData[len(carData)-1]['endDate'])/1000))
        personUrl="http://10.134.136.112:8000/prpall/business/editCinsured.do?editType="+editType+"&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+str(startDate)+"&endDate="+str(endDateSY)+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+str(today)+"&motorFastTrack=&operatorProjectCode=&reload=&rnd323="
        personRes = req_session.get(personUrl)
        personSoup = BeautifulSoup(personRes.content, "html.parser")
        carDic['identifyNumber'] = personSoup.find(id="prpCinsureds[0].identifyNumber").get('value')#身份证号
        carDic['insuredName'] = personSoup.find(id="prpCinsureds[0].insuredName").get('value').encode('latin1').decode('gbk')#车主姓名
        carDic['insuredAddress'] = personSoup.find(id="prpCinsureds[0].insuredAddress").get('value').encode('latin1').decode('gbk')#车主住址
        carDic['mobile'] = personSoup.find(id="prpCinsureds[0].mobile").get('value')#车主电话
        carDic['COMPANY_ID']='2'
        carDic['CCardDetail']=""
        carDic['NSeatNum']=""
        carDic['FLAG']="1"
        carDic['CModelCde']=""
        return carDic
    except Exception,e:
        return 0
if __name__=="__main__":
    startTime = time.time()
    # licenseNoList = [u"苏AQ6C06",u"苏AB1P05",u"苏AB2R68",u"苏AB0P61",u"苏AB9N73",u"苏AK0C77",u"苏AB2Q60",u"苏AB9N35",u"苏AB3Q98",u"苏AK8A77",u"苏AB0Q87",u"苏B768TD",u"苏ACT331"]
    licenseNoList = [u'苏bz970w']
    for licenseNo in licenseNoList:
        print json.dumps(xubao(licenseNo),ensure_ascii=False,indent=4)
    print time.time()-startTime