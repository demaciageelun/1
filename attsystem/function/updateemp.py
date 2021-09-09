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
    add_num = 0
    update_num = 0
    for datas in employeeData:
        bus_id = datas['jobNo']
        namse = datas['name']
        dept = datas['department']
        positi = datas['jobTitle']
        openid = datas['openId']
        # 根据bus_id是否为空判断是否为管建的人，管建的人不统计。
        if bus_id != "":
            is_exist = EmployeeInformation.objects.filter(bus_id=bus_id)
            # 根据bus_id判断是否有这个人，没有就新增，有就更新
            if len(is_exist) > 0:
                emp = EmployeeInformation.objects.get(bus_id=bus_id)
                emp.positi = positi
                emp.dept = dept
                emp.is_job = 1
                emp.save()
                update_num = update_num + 1
            else:
                emps = EmployeeInformation()
                emps.bus_id = bus_id
                emps.namse = namse
                emps.dept = dept
                emps.positi = positi
                emps.openid = openid
                emps.is_job = 1
                emps.save()
                add_num += 1
    return "更新了" + str(update_num) + "位员工，新增了" + str(add_num) + "位员工"
