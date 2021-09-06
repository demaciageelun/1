import json
import time
from urllib import parse
import requests
from ..models import EmployeeInformation


def getEmp():
    millis = int(round(time.time() * 1000))
    print(millis)

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
    print(r.json())
    employeeData = r.json()['data']
    print(employeeData)
    # 创建批量插入的数据
    data_list = []
    #   遍历员工，判断该员工在员工信息表中是否已有，没有的新增， 已有的更新。
    # for datas in employeeData:
    #     pass

    return data_list
