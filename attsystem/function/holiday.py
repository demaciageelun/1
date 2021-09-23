# 调休假5f212e529b3004000175dccc
# 事假5f212e529b3004000175dccd
# 病假5f212e529b3004000175dcce   #
# 婚假5f212e529b3004000175dccf   #
# 产假5f212e529b3004000175dcd0   #
# 陪产假5f212e529b3004000175dcd1   #
# 哺乳假5f212e529b3004000175dcd1
# 节育假5f212e529b3004000175dcd2   #
# 工伤假5f212e529b3004000175dcd3   #
# 看护假5f212e529b3004000175dcd4   #
# 丧假5f212e529b3004000175dcd5   #
# 产检假5f212e529b3004000175dcd6
# 处理逻辑
from attsystem.models import Cal, EmployeeHoildayStatistics, EmployeeInformation
import time
import datetime
from django.db.models import Q

leave_type_list = {
    "5f212e529b3004000175dccc": "a",
    "5f212e529b3004000175dccd": "b",
    "5f212e529b3004000175dcce": "c",
    "5f212e529b3004000175dccf": "d",
    "5f212e529b3004000175dcd0": "e",
    "5f212e529b3004000175dcd1": "f",
    "5f212e529b3004000175dcd1": "g",
    "5f212e529b3004000175dcd2": "h",
    "5f212e529b3004000175dcd3": "i",
    "5f212e529b3004000175dcd4": "j",
    "5f212e529b3004000175dcd5": "k",
    "5f212e529b3004000175dcd6": "l"
}


def transTime(times):
    timeArray = time.localtime(times / 1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


# 接收views接收到的请假信息，处理存入请假信息表中
def proLeaveInfor(data):
    print(data)
    try:
        # 取企业员工工号
        bus_id = data["data"]["basicInfo"]["myPersonInfo"]["oid"]
        emp = EmployeeInformation.objects.filter(bus_id=bus_id, att_type=1, is_job=1)
        if len(emp) > 0:  # 判断这个员工是否属于员工表中的记录考勤的在职的科室人员，该系统只统计科室人员信息。
            # 取出人员信息，获取该人员的理论打卡时间，来计算每个请假日的请假时间。
            time1 = emp[0].time1
            time2 = emp[0].time2
            time3 = emp[0].time3
            time4 = emp[0].time4
            # 取出请假列表值
            widget_value = data["data"]["formInfo"]["detailMap"]["_S_INT_LEAVE_DETAILED"]["widgetValue"]
            # 取出流水号
            serial = data["data"]["formInfo"]["widgetMap"]["_S_SERIAL"]["value"]
            # 可能有多行，循环取出
            for wv in widget_value:
                # 请假开始时间
                begin_time = transTime(wv["_S_INT_LEAVE_TIME"][0])
                # 请假结束时间
                end_time = transTime(wv["_S_INT_LEAVE_TIME"][1])
                # 请假时长（天）
                leave_days = wv["_S_INT_LEAVE_DAYS"]
                # 请假类型
                leave_type = wv["_S_INT_LEAVE_TYPE"]
                # 判断请假开始时间和请假结束时间之间是否隔天,有隔天的，把隔天的请假信息也写入请假表中，请假时间为8小时，首尾两天分别填写。
                date1 = time.strptime(begin_time[:10], "%Y-%m-%d")
                date2 = time.strptime(end_time[:10], "%Y-%m-%d")
                date1 = datetime.datetime(date1[0], date1[1], date1[2])
                date2 = datetime.datetime(date2[0], date2[1], date2[2])
                # 返回两个变量相差的值，就是相差天数。天数大于1的，从数据库工作日历表中查询之间的工作日，再把所有这几天写入请假表中。
                # 第一个请假开始时间早于8点的，按8点算，最后一个请假结束时间晚于17点30的，按17点30算。
                sub_data = (date2 - date1).days
                # >2表示开始和结束中间有间隔，查询工作日历表中的工作日，写入请假信息表
                if sub_data > 2:
                    data_list = getInforFromCal(begin_time[:10], end_time[:10])
                    # 开始那天调用一次函数
                    # 判断请假开始当天请假了多久
                    begin_leave_days = firstDay(time1, time2, time3, time4, begin_time)
                    if begin_leave_days > 0:  # 排除有人在下班后的时间申请请假
                        insertHoli(bus_id, leave_type_list[leave_type], begin_time[11:], time4, begin_leave_days,
                                   date1.year,
                                   date1.month, date1.day, date1.weekday() + 1, begin_time[:10], serial)
                    #     根据data_list遍历写入请假信息表，中间时长均为8小时
                    for data in data_list:
                        insertHoli(bus_id, leave_type_list[leave_type], time1, time4, 1,
                                   data.years,
                                   data.months, data.days, data.weeks, data.times, serial)
                    # 结束那天调用下函数
                    # 判断请假结束当天请假了多久
                    end_leave_days = lastDay(time1, time2, time3, time4, end_time)
                    if end_leave_days > 0:
                        insertHoli(bus_id, leave_type_list[leave_type], time1, end_time[11:], end_leave_days,
                                   date2.year,
                                   date2.month, date2.day, date2.weekday() + 1, end_time[:10], serial)

                # =1表示开始和结束是连续两天
                elif sub_data == 2:
                    # 开始那天调用一次函数
                    # 判断请假开始当天请假了多久
                    begin_leave_days = firstDay(time1, time2, time3, time4, begin_time)
                    if begin_leave_days > 0:  # 排除有人在下班后的时间申请请假
                        insertHoli(bus_id, leave_type_list[leave_type], begin_time[11:], time4, begin_leave_days,
                                   date1.year,
                                   date1.month, date1.day, date1.weekday() + 1, begin_time[:10], serial)
                    # 结束那天调用下函数
                    # 判断请假结束当天请假了多久
                    end_leave_days = lastDay(time1, time2, time3, time4, end_time)
                    if end_leave_days > 0:
                        insertHoli(bus_id, leave_type_list[leave_type], time1, end_time[11:], end_leave_days,
                                   date2.year,
                                   date2.month, date2.day, date2.weekday() + 1, end_time[:10], serial)
                # =0表示开始和结束时间是同一天
                else:
                    insertHoli(bus_id, leave_type_list[leave_type], begin_time[11:], end_time[11:], leave_days,
                               date1.year,
                               date1.month, date1.day, date1.weekday() + 1, begin_time[:10], serial)
        else:  # 不是科室人员，不统计请假信息。
            pass
    except Exception as e:
        print(e)


# 查询工作日历表中在请假开始和结束时间中间的工作日信息
def getInforFromCal(time1, time2):
    lists = Cal.objects.filter(
        Q(times__gt=time1),
        Q(times__lt=time2),
        Q(kinds=1) | Q(kinds=2)
    )
    return lists


def insertHoli(bus_id, types, btime, etime, last_time, years, months, days, weeks, date, serial):
    # 判断请假日期类型，是工作日请假，还是周六请假，还是包含周日的请假。通过查询工作日历表，来确定今天的工作状态。
    lists = Cal.objects.filter(times=date)
    hoilday_day_type = lists[0].kinds

    resp = EmployeeHoildayStatistics.objects.update_or_create(
        defaults={
            'bus_id': bus_id,
            'hoilday_type': types,
            'hoilday_day_type': hoilday_day_type,
            'hoilday_start_time': btime,
            'hoilday_stop_time': etime,
            'hoilday_last_time': last_time,
            'years': years,
            'months': months,
            'days': days,
            'weeks': weeks,
            'dates': date,
            'serial': serial
        },
        bus_id=bus_id,
        hoilday_type=types,
        hoilday_start_time=btime,
        hoilday_stop_time=etime,
        dates=date
    )
    print(resp)


# 判断第一天的请假时长
def firstDay(time1, time2, time3, time4, btime):
    times1 = time.mktime(time.strptime(btime[:10] + " " + str(time1), "%Y-%m-%d %H:%M:%S"))
    times2 = time.mktime(time.strptime(btime[:10] + " " + str(time2), "%Y-%m-%d %H:%M:%S"))
    times3 = time.mktime(time.strptime(btime[:10] + " " + str(time3), "%Y-%m-%d %H:%M:%S"))
    times4 = time.mktime(time.strptime(btime[:10] + " " + str(time4), "%Y-%m-%d %H:%M:%S"))
    btimes = time.mktime(time.strptime(btime, "%Y-%m-%d %H:%M:%S"))
    # 根据4个时间点和请假开始时间判断请假开始当天请假时长
    if btimes <= times1:
        begin_leave_days = 1
    elif times1 < btimes < times2:
        begin_leave_days = (times4 - btimes - 5400) / 28800
    elif times2 < btimes < times3:
        begin_leave_days = (times4 - times3) / 28800
    elif times3 < btimes < times4:
        begin_leave_days = (times4 - btimes) / 28800
    elif btimes >= times4:
        begin_leave_days = 0
    return begin_leave_days


# 判断最后一天的请假时长
def lastDay(time1, time2, time3, time4, etime):
    times1 = time.mktime(time.strptime(etime[:10] + " " + str(time1), "%Y-%m-%d %H:%M:%S"))
    times2 = time.mktime(time.strptime(etime[:10] + " " + str(time2), "%Y-%m-%d %H:%M:%S"))
    times3 = time.mktime(time.strptime(etime[:10] + " " + str(time3), "%Y-%m-%d %H:%M:%S"))
    times4 = time.mktime(time.strptime(etime[:10] + " " + str(time4), "%Y-%m-%d %H:%M:%S"))
    etimes = time.mktime(time.strptime(etime, "%Y-%m-%d %H:%M:%S"))
    # 根据4个时间点和请假开始时间判断请假开始当天请假时长
    if etimes <= times1:
        end_leave_days = 0
    elif times1 < etimes < times2:
        end_leave_days = (etimes - times1) / 28800
    elif times2 < etimes < times3:
        end_leave_days = (times2 - times1) / 28800
    elif times3 < etimes < times4:
        end_leave_days = (etimes - times1 - 5400) / 28800
    elif etimes >= times4:
        end_leave_days = 1
    return end_leave_days
