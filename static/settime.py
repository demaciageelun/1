import time
import requests

# 定时执行任务
localtime = time.localtime(time.time())  # 创建时间对象

while True:
    time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新\
    # 每晚8点自动校对云之家员工，自动覆盖部门岗位信息。
    if time_now == "20:00:00":
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        url = "http://127.0.0.1:37214/att/updateEmp/"
        r = requests.post(url=url)
        accessToken = r.json()
        print(accessToken)
        time.sleep(2)  # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次
    #     每天早上10点30获取刷卡数据
    if time_now == "10:30:00":
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        url = "http://127.0.0.1:37214/att/checkdata/"
        r = requests.post(url=url)
        accessToken = r.json()
        print(accessToken)
    date_now = time.strftime("%d", time.localtime())
    #     每天早上7点创建前3日的每日信息表（该表可覆盖，建议一次性更新前几日的信息，防止有审批数据不及时的现象）
    if time_now == "07:00:00":
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        url = "http://127.0.0.1:37214/att/daliy/"
        r = requests.post(url=url)
        accessToken = r.json()
        print(accessToken)
    date_now = time.strftime("%d", time.localtime())
    # 每月5号计算月度信息汇总表
    if date_now == "05":
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        url = "http://127.0.0.1:37214/att/monthliy/"
        r = requests.post(url=url)
        accessToken = r.json()
        print(accessToken)
