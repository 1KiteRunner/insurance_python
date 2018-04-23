# -*- coding:utf-8 -*-
import datetime


def dt_init():
    dt={
        'operatorCode':'A320100906',
        'makeCom': '32012105',
        'operator_homephone': '13809040202',
        'operatorProjectCode': 'KBDAA201632010000000501,KBDAA201632010000000873',
        'randomProposalNo': '6358560951487830052655 ',
        'agentCode': '320021101233',
        'useYear': '9',
        'enrollDate' : '',
        'operationTimeStamp':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'today' : str(datetime.datetime.date.today()),
        'taxPlatFormTime': '2016-1-8'
    }
    return dt