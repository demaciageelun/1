from attsystem.models import EmployeeInformation, EmployeeHoildayStatistics, Cal
from openpyxl import load_workbook
import datetime
import time
from django.db.models import Q

# 假期类型：a（调休假），b（事假），c（病假），d（婚假），e（产假），f（陪产假），g（哺乳假），h（节育假）
# i（工伤假），j（看护假），k（丧假），l（产检假）
leave_type_list = {
    "调休假": "a",
    "事假": "b",
    "病假": "c",
    "婚假": "d",
    "产假": "e",
    "陪产假": "f",
    "哺乳假": "g",
    "节育假": "h",
    "工伤假": "i",
    "看护假": "j",
    "丧假": "k",
    "产检假": "l"
}


def judge(data):
    if data == "调休假":
        return "a"
    if data == "事假":
        return "b"
    if data == "病假":
        return "c"
    if data == "婚假":
        return "d"
    if data == "产假":
        return "e"
    if data == "陪产假":
        return "f"
    if data == "哺乳假":
        return "g"
    if data == "节育假":
        return "h"
    if data == "工伤假":
        return "i"
    if data == "看护假":
        return "j"
    if data == "丧假":
        return "k"
    if data == "产检假":
        return "l"


def insert_hoilday():
    # fileName 这里是指文件路径
    fileName = "static/HR011.xlsx"
    # 以只读模式打开工作簿
    wb = load_workbook(filename=fileName, read_only=True)
    # sheetName 就是 sheet页的名称
    sheetName = "1"
    # 通过 工作表名 获取 工作表
    ws = wb[sheetName]
    # 按行读取 工作表的内容
    data_list = []
    for row in ws.rows:
        bus_id = row[4].value
        leave_type = row[13].value
        begin_time = row[11].value
        end_time = row[12].value
        hoilday_last_time = float(row[14].value)
        print(bus_id)
        emp = EmployeeInformation.objects.filter(bus_id=bus_id, att_type=1)
        if len(emp) > 0:  # 判断这个员工是否属于员工表中的科室人员，该系统只统计科室人员信息。
            # 取出人员信息，获取该人员的理论打卡时间，来计算每个请假日的请假时间。
            time1 = emp[0].time1
            time2 = emp[0].time2
            time3 = emp[0].time3
            time4 = emp[0].time4
            # 判断请假开始时间和请假结束时间之间是否隔天,有隔天的，把隔天的请假信息也写入请假表中，请假时间为8小时，首尾两天分别填写。
            print(str(begin_time)[:10])
            date1 = time.strptime(str(begin_time)[:10], "%Y-%m-%d")
            date2 = time.strptime(str(end_time)[:10], "%Y-%m-%d")
            date1 = datetime.datetime(date1[0], date1[1], date1[2])
            date2 = datetime.datetime(date2[0], date2[1], date2[2])
            # 返回两个变量相差的值，就是相差天数。天数大于1的，从数据库工作日历表中查询之间的工作日，再把所有这几天写入请假表中。
            # 第一个请假开始时间早于8点的，按8点算，最后一个请假结束时间晚于17点30的，按17点30算。
            sub_data = (date2 - date1).days
            # >2表示开始和结束中间有间隔，查询工作日历表中的工作日，写入请假信息表
            if sub_data > 2:
                data_list = getInforFromCal(str(begin_time)[:10], str(end_time)[:10])
                # 开始那天调用一次函数
                # 判断请假开始当天请假了多久
                begin_leave_days2 = firstDay(time1, time2, time3, time4, begin_time)
                if begin_leave_days2 > 0:  # 排除有人在下班后的时间申请请假
                    insertHoli(bus_id, leave_type_list[leave_type], str(begin_time)[11:], time4, begin_leave_days2,
                               date1.year,
                               date1.month, date1.day, date1.weekday() + 1, str(begin_time)[:10])
                #     根据data_list遍历写入请假信息表，中间时长均为8小时
                for data in data_list:
                    insertHoli(bus_id, leave_type_list[leave_type], time1, time4, 1,
                               data.years,
                               data.months, data.days, data.weeks, data.times)
                # 结束那天调用下函数
                # 判断请假结束当天请假了多久
                end_leave_days2 = lastDay(time1, time2, time3, time4, end_time)
                if end_leave_days2 > 0:
                    insertHoli(bus_id, leave_type_list[leave_type], time1, str(end_time)[11:], end_leave_days2,
                               date2.year,
                               date2.month, date2.day, date2.weekday() + 1, str(end_time)[:10])

            # =1表示开始和结束是连续两天
            elif sub_data == 1:
                # 开始那天调用一次函数
                # 判断请假开始当天请假了多久
                begin_leave_days1 = firstDay(time1, time2, time3, time4, begin_time)
                if begin_leave_days1 > 0:  # 排除有人在下班后的时间申请请假
                    insertHoli(bus_id, leave_type_list[leave_type], str(begin_time)[11:], time4, begin_leave_days1,
                               date1.year,
                               date1.month, date1.day, date1.weekday() + 1, str(begin_time)[:10])
                # 结束那天调用下函数
                # 判断请假结束当天请假了多久
                end_leave_days1 = lastDay(time1, time2, time3, time4, end_time)
                if end_leave_days1 > 0:
                    insertHoli(bus_id, leave_type_list[leave_type], time1, str(end_time)[11:], end_leave_days1,
                               date2.year,
                               date2.month, date2.day, date2.weekday() + 1, str(end_time)[:10])
            # =0表示开始和结束时间是同一天
            else:
                insertHoli(bus_id, leave_type_list[leave_type], str(begin_time)[11:], str(end_time)[11:],
                           hoilday_last_time,
                           date1.year,
                           date1.month, date1.day, date1.weekday() + 1, str(begin_time)[:10])


# 查询工作日历表中在请假开始和结束时间中间的工作日信息
def getInforFromCal(time1, time2):
    lists = Cal.objects.filter(
        Q(times__gt=time1),
        Q(times__lt=time2),
        Q(kinds=1) | Q(kinds=2)
    )
    return lists


def insertHoli(bus_id, types, btime, etime, last_time, years, months, days, weeks, date):
    # 判断请假日期类型，是工作日请假，还是周六请假，还是包含周日的请假。通过查询工作日历表，来确定今天的工作状态。
    lists = Cal.objects.filter(times=date)
    hoilday_day_type = lists[0].kinds
    resp = EmployeeHoildayStatistics.objects.create(bus_id=bus_id, hoilday_type=types,
                                                    hoilday_day_type=hoilday_day_type,
                                                    hoilday_start_time=btime,
                                                    hoilday_stop_time=etime, hoilday_last_time=last_time, years=years,
                                                    months=months, days=days, weeks=weeks, dates=date)
    print(resp)


# 判断第一天的请假时长
def firstDay(time1, time2, time3, time4, btime):
    data = 0
    times1 = time.mktime(time.strptime(str(btime)[:10] + " " + str(time1), "%Y-%m-%d %H:%M:%S"))
    times2 = time.mktime(time.strptime(str(btime)[:10] + " " + str(time2), "%Y-%m-%d %H:%M:%S"))
    times3 = time.mktime(time.strptime(str(btime)[:10] + " " + str(time3), "%Y-%m-%d %H:%M:%S"))
    times4 = time.mktime(time.strptime(str(btime)[:10] + " " + str(time4), "%Y-%m-%d %H:%M:%S"))
    # btimes = time.mktime(time.strptime(str(btime), "%Y-%m-%d %H:%M"))
    if len(str(btime)) == 16:
        btimes = time.mktime(time.strptime(str(btime), "%Y-%m-%d %H:%M"))
    else:
        btimes = time.mktime(time.strptime(str(btime), "%Y-%m-%d %H:%M:%S"))

    # 根据4个时间点和请假开始时间判断请假开始当天请假时长
    if btimes <= times1:
        data = 1
    elif times1 < btimes < times2:
        data = (times4 - btimes - 5400) / 28800
    elif times2 < btimes < times3:
        data = (times4 - times3) / 28800
    elif times3 < btimes < times4:
        data = (times4 - btimes) / 28800
    elif btimes >= times4:
        data = 0
    return data


# 判断最后一天的请假时长
def lastDay(time1, time2, time3, time4, etime):
    data = 0
    times1 = time.mktime(time.strptime(str(etime)[:10] + " " + str(time1), "%Y-%m-%d %H:%M:%S"))
    times2 = time.mktime(time.strptime(str(etime)[:10] + " " + str(time2), "%Y-%m-%d %H:%M:%S"))
    times3 = time.mktime(time.strptime(str(etime)[:10] + " " + str(time3), "%Y-%m-%d %H:%M:%S"))
    times4 = time.mktime(time.strptime(str(etime)[:10] + " " + str(time4), "%Y-%m-%d %H:%M:%S"))
    if len(str(etime)) == 16:
        etimes = time.mktime(time.strptime(str(etime), "%Y-%m-%d %H:%M"))
    else:
        etimes = time.mktime(time.strptime(str(etime), "%Y-%m-%d %H:%M:%S"))
    # 根据4个时间点和请假开始时间判断请假开始当天请假时长
    if etimes <= times1:
        data = 0
    elif times1 < etimes < times2:
        data = (etimes - times1) / 28800
    elif times2 < etimes < times3:
        data = (times2 - times1) / 28800
    elif times3 < etimes < times4:
        data = (etimes - times1 - 5400) / 28800
    elif etimes >= times4:
        data = 1
    return data
