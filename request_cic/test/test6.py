# -*- coding:utf-8 -*-
__author__ = 'weikai'


dc=[
  {
    "vehicleId": "4028b2b64c3599c9014c497f7b76193f",
    "insuranceJqName": "\r\r六座以下客车\r",
    "purchasePriceTax": 109800,
    "marketDate": "\r\r201503\r",
    "seat": "\r\r5\r",
    "factoryName": "\r\r一汽-大众汽车有限公司\r",
    "gCIndustryModelName": "\r\r大众FV7166BAMBG轿车\r",
    "demo": "\r\r手动档时尚型国Ⅴ\r",
    "vehicleCode": "\r\rSTD1132YQD\r",
    "kindredPrice": "\r\r\r\r"
  },
  {
    "vehicleId": "4028b2b64c3599c9014c49a00d5a1bae",
    "insuranceJqName": "\r\r六座以下客车\r",
    "purchasePriceTax": 116800,
    "marketDate": "\r\r201503\r",
    "seat": "\r\r5\r",
    "factoryName": "\r\r一汽-大众汽车有限公司\r",
    "gCIndustryModelName": "\r\r大众FV7166BAMBG轿车\r",
    "demo": "\r\r手动档舒适型国Ⅴ\r",
    "vehicleCode": "\r\rSTD1133YQD\r",
    "kindredPrice": "\r\r\r\r"
  },
  {
    "vehicleId": "4028b2b65754f3ce015774c2713836b7",
    "insuranceJqName": "\r\r六座以下客车\r",
    "purchasePriceTax": 118800,
    "marketDate": "\r\r201609\r",
    "seat": "\r\r5\r",
    "factoryName": "\r\r一汽-大众汽车有限公司\r",
    "gCIndustryModelName": "\r\r大众FV7166BAMBG轿车\r",
    "demo": "\r\r手动档时尚型国Ⅴ\r",
    "vehicleCode": "\r\rSTD1150YQD\r",
    "kindredPrice": "\r\r\r\r"
  },
  {
    "vehicleId": "4028b2b65754f3ce015774c45a1d36c7",
    "insuranceJqName": "\r\r六座以下客车\r",
    "purchasePriceTax": '125800',
    "marketDate": "\r\r201609\r",
    "seat": "\r\r5\r",
    "factoryName": "\r\r一汽-大众汽车有限公司\r",
    "gCIndustryModelName": "\r\r大众FV7166BAMBG轿车\r",
    "demo": "\r\r手动档舒适型国Ⅴ\r",
    "vehicleCode": "\r\rSTD1151YQD\r",
    "kindredPrice": "\r\r\r\r"
  }
]

#dc.sort(key=lambda obj:obj.get('purchasePriceTax'))
#print(dc)
ls1 = [{'a' : '1', 'b' : 12}, {'a' : '-1', 'b' : 11},{'a' : '12', 'b' : 9},{'a' : '6', 'b' : 42}]

ls1.sort(key=lambda obj:obj.get('a'))
print(ls1)