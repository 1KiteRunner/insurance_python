#!/usr/bin/python
# -*- coding: UTF-8 -*-
# if i%10==0:
#    m = i/10
# els:
#    m = i/10+1
args = '12345678901234567890123456789012345678901231231312123123'
rang = (len(args)+10-1)/10
for i in range(0, rang):
   if i < rang - 1:
      print args[(i * 10):(10 * i + 10)]
   else:
      print args[(i * 10):len(args)]