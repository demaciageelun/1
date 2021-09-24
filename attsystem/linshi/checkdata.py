import datetime
import json
import time
import calendar
from urllib import parse

import arrow
import requests
from ..models import EmployeeInformation, CheckInDetail


def get_daylis(year, month):
    day_lis = []
    for day in range(calendar.monthrange(year, month)[1] + 1)[1:]:
        day_lis.append('%s-%s-%s' % (year, '%02d' % month, '%02d' % (day)))
    # print(day_lis)
    return day_lis


def checkinDetail():
    millis = int(round(time.time() * 1000))
    url = "https://yunzhijia.com/gateway/oauth2/token/getAccessToken"
    header = {
        "Content-Type": "application/json"
    }
    d = {
        "eid": "19469603",
        "secret": "6tvR5xDVAEj3zGNBSbB09YDMDS0RZMmp",
        "timestamp": millis,
        "scope": "resGroupSecret"
    }
    r = requests.post(url=url, data=json.dumps(d), headers=header)
    # print(r.json())
    accessToken = r.json()['data']['accessToken']
    # 获取当前年和月
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month - 1
    # 获取当月所有日期
    time_list = get_daylis(year, month)
    # 查询所有用户的id和openid
    id_list = EmployeeInformation.objects.filter(att_type=1, is_job=1).values_list("bus_id", "openid")
    key = []
    value = []
    for idl in id_list:
        key.append(idl[1])
        value.append(idl[0])
    idd_list = dict(zip(key, value))
    # print(idd_list)
    resp = ""
    # for data in time_list:
    check_time = arrow.now().shift(days=-3)
    resp = detail_data_inter(accessToken, check_time, idd_list, 1)
    return resp


def detail_data_inter(accessToken, data, idd_list, start):
    url = "https://yunzhijia.com/gateway/attendance-data/v1/clockIn/day/list?accessToken=" + accessToken
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    d = {'eid': 19469603, 'day': data, 'start': start}
    d = parse.urlencode(d)
    r = requests.post(url=url, data=d, headers=header)
    retu_data = r.json()['data']
    if retu_data is not None:
        for datas in retu_data:
            check_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(datas["time"] / 1000))
            try:
                # cid = CheckInDetail()
                # cid.bus_id = datas['openId']
                # cid.check_date = check_time[:10]
                # cid.checkin_time = check_time[11:]
                # cid.weeks = datetime.datetime.strptime(check_time[:10], "%Y-%m-%d").weekday() + 1
                # cid.years = check_time[:4]
                # cid.months = check_time[5:7]
                # cid.days = check_time[8:10]
                # cid.save()
                CheckInDetail.objects.update_or_create(
                    defaults={
                        "bus_id": datas['openId'],
                        "check_date": check_time[:10],
                        "checkin_time": check_time[11:],
                        "weeks": datetime.datetime.strptime(check_time[:10], "%Y-%m-%d").weekday() + 1,
                        "years": check_time[:4],
                        "months": check_time[5:7],
                        "days": check_time[8:10],
                    },
                    bus_id=datas['openId'],
                    check_date=check_time[:10],
                    checkin_time=check_time[11:]
                )
            except Exception as e:
                print(e)
        if len(retu_data) == 200:
            detail_data_inter(accessToken, data, idd_list, start + 1)
        return "更新成功"
    else:
        return "请不要在上下班高峰期使用"
