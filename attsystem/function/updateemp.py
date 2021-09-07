import json
import time
from urllib import parse
import requests


def getEmp():
    millis = int(round(time.time() * 1000))

    url = "https://yunzhijia.com/gateway/oauth2/token/getAccessToken"
    header = {
        "Content-Type": "application/json"
    }
    d = {
        "eid": "19469603",
        "secret": "h0z2REPJ0VY7lsRXOcBQ0qOG0uOsrC4O",
        "timestamp": millis,
        "scope": "resGroupSecret"
    }
    r = requests.post(url=url, data=json.dumps(d), headers=header)
    print(r.json())
    accessToken = r.json()['data']['accessToken']

    url = "https://yunzhijia.com/gateway/openimport/open/person/getall?accessToken=" + accessToken
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    d = {'eid': 19469603, 'data': {}}
    d = parse.urlencode(d)
    r = requests.post(url=url, data=d, headers=header)
    employeeData = r.json()['data']
    print(employeeData)
    # 创建批量插入的数据
    data_list = []
    # 新增或者更新数据，增加修改时间字段。循环结束后判断是否当天有过更新，没有的则置为离职不需要统计考勤。
    for datas in employeeData:

        pass
    return data_list
