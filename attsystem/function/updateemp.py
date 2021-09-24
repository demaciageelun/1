import json
import time
from urllib import parse
import requests
from ..models import EmployeeInformation


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
    # print(r.json())
    accessToken = r.json()['data']['accessToken']

    url = "https://yunzhijia.com/gateway/openimport/open/person/getall?accessToken=" + accessToken
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    d = {'eid': 19469603, 'data': {}}
    d = parse.urlencode(d)
    r = requests.post(url=url, data=d, headers=header)
    employeeData = r.json()['data']
    # print(employeeData)
    # 创建批量插入的数据
    # 新增或者更新数据，增加修改时间字段。循环结束后判断是否当天有过更新，没有的则置为离职不需要统计考勤。
    for datas in employeeData:
        bus_id = datas['openId']
        namse = datas['name']
        dept = datas['department']
        positi = datas['jobTitle']
        openid = datas['jobNo']
        if dept == "离职人员":
            is_job = 2
        else:
            is_job = 1
        # 根据bus_id是否为空判断是否为管建的人，管建的人不统计。
        if openid != "" and dept[:4] != "江苏管建" and str(openid[:6]) != "210732":
            entry_date = "20" + str(openid[:2]) + "-" + str(openid[2:4]) + "-" + str(openid[4:6])
            print(openid)
            print(namse)
            print(entry_date)
            # 根据bus_id判断是否有这个人，没有就新增，有就更新
            EmployeeInformation.objects.update_or_create(
                defaults={
                    'bus_id': bus_id,
                    'namse': namse,
                    'dept': dept,
                    'positi': positi,
                    'openid': openid,
                    'is_job': is_job,
                    'entry_date': entry_date,
                    'att_type': 1,
                    'time1': '08:30',
                    'time4': '17:30'
                },
                bus_id=bus_id
            )
            # EmployeeInformation.objects.filter(bus_id=openid).update(openid=str(bus_id))
    return "更新成功"
