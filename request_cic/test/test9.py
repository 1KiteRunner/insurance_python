data='''
	Line 2:         "index": "${index}",
	Line 12:             _-b"${lNSeqNo}"
	Line 20:             _-b"${lCCvrgNo}"
	Line 24:             _-b"${lNAmt}"
	Line 28:             _-b"${lCDductMrk}"
	Line 32:             _-b"${lNBasePrm}"
	Line 36:             _-b"${lNPrm}"
	Line 40:             _-b"${lNPerAmt}"
	Line 44:             _-b"${lNLiabDaysLmt}"
	Line 48:             _-b"${lNIndemLmt}"
	Line 52:             _-b"${lNRate}"
	Line 92:             _-b"${s30}"
	Line 96:             _-b"${s29}"
	Line 108:             _-b"${lCIndemLmtLvl}"
	Line 112:             _-b"${lNDductRate}"
	Line 132:             _-b"${lNVhlActVal}"
'''

import  re
flow_id=re.findall(r"{(.+?)}",data,re.S)
print(len(flow_id))
s = set(flow_id)
c = [i for i in s]
print len(c)
sss=""
for i in xrange(len(c)):
    one=c[i]+"="+c[i]+","
    print(one)
