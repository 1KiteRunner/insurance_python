# -*- coding:utf-8 -*-
__author__ = 'weikai'


from request_cic.login import *
from request_cic.vhlPlatform import *
searchVin='LFV2A11K8F4192886'

requesteicc=logincic()
dt = getCarInof(requesteicc,searchVin)

