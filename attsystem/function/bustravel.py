# 出差记录处理
from django.db.models import Q

from attsystem.models import Cal, EmployeeBustravelStatistics, EmployeeInformation

import time
import datetime


def transTime(times):
    timeArray = time.localtime(times / 1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def bustravelInfo(data):
    print(data)
    try:
        # 取企业员工工号
        bus_id = data["data"]["basicInfo"]["myPersonInfo"]["jobNo"]
        emp = EmployeeInformation.objects.filter(bus_id=bus_id)
        if len(emp) > 0:  # 判断这个员工是否属于员工表中的科室人员，该系统只统计科室人员信息。
            # 取出人员信息，获取该人员的理论打卡时间，来计算每个出差日的出差时间。
            time1 = emp[0].time1
            time2 = emp[0].time2
            time3 = emp[0].time3
            time4 = emp[0].time4
            # 取出请假列表值
            widget_value = data["data"]["formInfo"]["detailMap"]["_S_INT_ON_BUSINESS_DETAILED"]["widgetValue"]

            # 可能有多行，循环取出
            for wv in widget_value:
                # 出差开始时间
                begin_time = transTime(wv["_S_INT_ON_BUSINESS_TIME"][0])
                # 出差结束时间
                end_time = transTime(wv["_S_INT_ON_BUSINESS_TIME"][1])
                # 请假时长（天）
                travel_days = wv["_S_INT_ON_BUSINESS_DAYS"]

                # 判断出差开始时间和出差结束时间之间是否隔天,有隔天的，把隔天的请假信息也写入出差表中，出差时间为8小时，首尾两天分别填写。
                date1 = time.strptime(begin_time[:10], "%Y-%m-%d")
                date2 = time.strptime(end_time[:10], "%Y-%m-%d")
                date1 = datetime.datetime(date1[0], date1[1], date1[2])
                date2 = datetime.datetime(date2[0], date2[1], date2[2])
                # 返回两个变量相差的值，就是相差天数。天数大于1的，从数据库工作日历表中查询之间的工作日，再把所有这几天写入出差表中。
                # 第一个出差开始时间早于8点的，按8点算，最后一个请假结束时间晚于17点30的，按17点30算。
                sub_data = (date2 - date1).days
                print(sub_data)
                # >1表示开始和结束中间有间隔，查询工作日历表中的工作日，写入出差信息表
                if sub_data > 1:
                    data_list = getInforFromCal(begin_time[:10], end_time[:10])
                    # 开始那天调用一次函数
                    # 判断出差开始当天出差了多久
                    begin_travel_days = firstDay(time1, time2, time3, time4, begin_time)
                    if begin_travel_days > 0:  # 排除有人在下班后的时间申请出差
                        insertBustravel(bus_id, begin_time[11:], time4, begin_travel_days,
                                        date1.year,
                                        date1.month, date1.day, date1.weekday() + 1, begin_time[:10])
                    #     根据data_list遍历写入出差信息表，中间时长均为8小时
                    for data in data_list:
                        print(data.times)
                        insertBustravel(bus_id, time1, time4, 1,
                                        data.years,
                                        data.months, data.days, data.weeks, data.times)
                    # 结束那天调用下函数
                    # 判断出差结束当天出差了多久
                    end_travel_days = lastDay(time1, time2, time3, time4, end_time)
                    if end_travel_days > 0:
                        insertBustravel(bus_id, time1, end_time[11:], end_travel_days,
                                        date2.year,
                                        date2.month, date2.day, date2.weekday() + 1, end_time[:10])

                # =1表示开始和结束是连续两天
                elif sub_data == 1:
                    # 开始那天调用一次函数2
                    # 判断出差开始当天出差了多久
                    begin_travel_days = firstDay(time1, time2, time3, time4, begin_time)
                    if begin_travel_days > 0:  # 排除有人在下班后的时间申请出差
                        insertBustravel(bus_id, begin_time[11:], time4, begin_travel_days,
                                        date1.year,
                                        date1.month, date1.day, date1.weekday() + 1, begin_time[:10])
                    # 结束那天调用下函数
                    # 判断出差结束当天出差了多久
                    end_travel_days = lastDay(time1, time2, time3, time4, end_time)
                    if end_travel_days > 0:
                        insertBustravel(bus_id, time1, end_time[11:], end_travel_days,
                                        date2.year,
                                        date2.month, date2.day, date2.weekday() + 1, end_time[:10])
                # =0表示开始和结束时间是同一天
                else:
                    insertBustravel(bus_id, begin_time[11:], end_time[11:], travel_days,
                                    date1.year,
                                    date1.month, date1.day, date1.weekday() + 1, begin_time[:10])
        else:  # 不是科室人员，不统计请假信息。
            pass
    except Exception as e:
        print(e)


# 查询工作日历表中在出差开始和出差时间中间的工作日信息
def getInforFromCal(time1, time2):
    lists = Cal.objects.filter(
        Q(times__gt=time1),
        Q(times__lt=time2),
        Q(kinds=1) | Q(kinds=2)
    )
    return lists


# 判断第一天的出差时长
def firstDay(time1, time2, time3, time4, btime):
    times1 = time.mktime(time.strptime(btime[:10] + " " + str(time1), "%Y-%m-%d %H:%M:%S"))
    times2 = time.mktime(time.strptime(btime[:10] + " " + str(time2), "%Y-%m-%d %H:%M:%S"))
    times3 = time.mktime(time.strptime(btime[:10] + " " + str(time3), "%Y-%m-%d %H:%M:%S"))
    times4 = time.mktime(time.strptime(btime[:10] + " " + str(time4), "%Y-%m-%d %H:%M:%S"))
    btimes = time.mktime(time.strptime(btime, "%Y-%m-%d %H:%M:%S"))
    # 根据4个时间点和出差开始时间判断出差开始当天请假时长
    if btimes < times1:
        begin_travel_days = 1
    elif times1 < btimes < times2:
        begin_travel_days = (times4 - btimes - 5400) / 28800
    elif times2 < btimes < times3:
        begin_travel_days = (times4 - times3) / 28800
    elif times3 < btimes < times4:
        begin_travel_days = (times4 - btimes) / 28800
    elif btimes > times4:
        begin_travel_days = 0
    return begin_travel_days


# 判断最后一天的出差时长
def lastDay(time1, time2, time3, time4, etime):
    times1 = time.mktime(time.strptime(etime[:10] + " " + str(time1), "%Y-%m-%d %H:%M:%S"))
    times2 = time.mktime(time.strptime(etime[:10] + " " + str(time2), "%Y-%m-%d %H:%M:%S"))
    times3 = time.mktime(time.strptime(etime[:10] + " " + str(time3), "%Y-%m-%d %H:%M:%S"))
    times4 = time.mktime(time.strptime(etime[:10] + " " + str(time4), "%Y-%m-%d %H:%M:%S"))
    etimes = time.mktime(time.strptime(etime, "%Y-%m-%d %H:%M:%S"))
    # 根据4个时间点和出差结束时间判断出差结束当天出差时长
    if etimes < times1:
        end_travel_days = 0
    elif times1 < etimes < times2:
        end_travel_days = (etimes - times1) / 28800
    elif times2 < etimes < times3:
        end_travel_days = (times2 - times1) / 28800
    elif times3 < etimes < times4:
        end_travel_days = (etimes - times1 - 5400) / 28800
    elif etimes > times4:
        end_travel_days = 1
    return end_travel_days


def insertBustravel(bus_id, btime, etime, last_time, years, months, days, weeks, date):
    resp = EmployeeBustravelStatistics.objects.create(bus_id=bus_id,
                                                      bustravel_start_time=btime,
                                                      bustravel_stop_time=etime, bustravel_last_time=last_time,
                                                      years=years,
                                                      months=months, days=days, weeks=weeks, dates=date)
    print(resp)
