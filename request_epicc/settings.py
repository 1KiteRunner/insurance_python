# -*- coding:utf-8 -*-
__author__ = 'weikai'

headers={'Host':'www.epicc.com.cn',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Accept-Encoding':'gzip, deflate',
         'Accept-Language':'zh-CN,zh;q=0.8',
         'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
         'Referer':'http://www.epicc.com.cn/m/',
         'Upgrade-Insecure-Requests':'1',
         'Content-Type':'application/x-www-form-urlencoded',
         #'Cookie':'EcutH7WVc8=MDAwM2IyYWQzNzQwMDAwMDAwMDIwNH58TlsxNDgyNzUyMTgw; epicc_tid=10.130.67.33.1482747407207253; 8rtCaPoAWP=MDAwM2IyYWQ0ZjQwMDAwMDAwMjIwBTt2TQ8xNDgyNzU0MTIy; JSESSIONID=gvwqYgnP2Xvpc5fnHMPrQcpj7KnzCtp0smbKVCGL02dl5Z4WzKbp!-1797979247; s_fid=505A05B9862FFD4E-350112192DECB88A; vid=0889b9826e8c844e4dbcbb888f453795; s_getNewRepeat=1482747415990-New; s_vnum=1514283415990%26vn%3D1; s_invisit=true; s_cc=true; __ag_cm_=1; ag_fid=vRvlvLXnz4P8VaHF; svid=F530034D7057877; PiccMobSaleSession1=kNvqYgnQG1qcKXCgsTtcvvpTJjtfJ30HdV0jGs3pnTBF8B2kY1q0!736736254; DX8XXaUM2S=MDAwM2IyYWQ0ZjQwMDAwMDAwMjYwUVl5bjAxNDgyNzU0MTIz; PiccMobSaleSession=vLQ0YgnQTQ39Lfp4QZwL1FF8nh06SnQZxL1Jd49C7xLnZfGL7VYS!-1712403248; _gscu_793357708=827474153e0pmi20; _gscs_793357708=82747415tnhi1f20|pv:2; _gscbrs_793357708=1'
          'Cookie':'ist_lt=1484219861873; epicc_tid=10.130.67.32.1484019128014420; EcutH7WVc8=MDAwM2IyYWQzNzQwMDAwMDAwMDIwIwwFMj8xNDg0MjI0MzI2; 8rtCaPoAWP=MDAwM2IyYWQ0ZjQwMDAwMDAwMjIwDkg/QG8xNDg0MjI2MjY3; JSESSIONID=2n7qY3ldQxPfn0hY5BctQvNz8DQ1YSyLxbKKmNVpHXSKw5KYXy5F!-1475256138; s_fid=07D9B72B027DF493-28219A29CA6687A5; vid=733312d3117f1d5e1f4f4aa47f63d144; s_getNewRepeat=1484219862184-Repeat; s_vnum=1515555126433%26vn%3D2; svid=89E367EED97F1152; _gscu_793357708=84019132e2tm0t15; s_invisit=true; s_cc=true; _gscs_793357708=84219861vevdh115|pv:1; _gscbrs_793357708=1'
}

#获取sessionid 此页面是输入第一个用户信息
carInput1_url='http://www.epicc.com.cn/wap/carProposal/car/carInput1'
isRenewal_url='http://www.epicc.com.cn/wap/carProposal/renewal/isRenewal'
carDataReuse_url = "http://www.epicc.com.cn/wap/carProposal/car/carDataReuse"
CreateImage_url='http://www.epicc.com.cn/wap/CreateImage'
#huo获取用户信息
queryRenewal_url='http://www.epicc.com.cn/wap/carProposal/renewal/queryRenewal'
interim_url = "http://www.epicc.com.cn/wap/carProposal/car/interim"
getVerifQueryCar_url = "http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode"
postVerifQueryCar_url = "http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar"
check_url = "http://www.epicc.com.cn/wap/carProposal/underWrite/underwriteCheckProfitAjax"
firstTimeCalculate_url = 'http://www.epicc.com.cn/wap/carProposal/calculateFee/renewalfee'
secondTimeCalculate_url = "http://www.epicc.com.cn/wap/carProposal/calculateFee/sy"
query_carData_url = "http://www.epicc.com.cn/wap/carProposal/car/query_carDataReuse"
imagePath = "C:\\Users\\Administrator\\Desktop\\request_epicc\\image\\"
# imagePath = "D:\\insurance-python\\request_epicc\\image\\"




# ===================打码平台配置===========================================
DAMA2_USERNAME='229051923'
DAMA2_PWD='qwer1234'
