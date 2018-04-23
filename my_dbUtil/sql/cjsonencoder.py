#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'wk'

import  json
from datetime import *
from decimal import Decimal
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        elif isinstance(obj, date):
            return obj.__str__()
        elif isinstance(obj,Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)