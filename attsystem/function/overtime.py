# 加班信息处理
from attsystem.models import EmployeeInformation, EmployeeOvertimeStatistics
import time
import datetime

over_type_list = {
    "_S_INT_OVERTIME_PS": 1,
    "_S_INT_OVERTIME_ZM": 2,
    "_S_INT_OVERTIME_JQ": 3,
}


def transTime(times):
    timeArray = time.localtime(times / 1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def overTimeInfo(data):
    print(data)
    try:
        # 取企业员工工号
        # *****员工号第一个数字为0的需要重新测试*****陈勇
        bus_id = data["data"]["basicInfo"]["myPersonInfo"]["oid"]
        emp = EmployeeInformation.objects.filter(bus_id=bus_id, att_type=1, is_job=1)
        if len(emp) > 0:  # 判断这个员工是否属于员工表中的记录考勤的在职的科室人员，该系统只统计科室人员信息。
            # 取出加班列表值
            widget_value = data["data"]["formInfo"]["detailMap"]["_S_INT_OVERTIME_DETAILED"]["widgetValue"]
            # 可能有多行，循环取出
            for wv in widget_value:
                # 取出请假类型
                over_type = over_type_list[wv["_S_INT_OVERTIME_TYPE"]]
                over_last_time = wv["_S_INT_OVERTIME_HOURS"]
                over_begin_time = transTime(wv["_S_INT_OVERTIME_TIME"][0])
                over_end_time = transTime(wv["_S_INT_OVERTIME_TIME"][1])
                date = time.strptime(over_begin_time[:10], "%Y-%m-%d")
                date = datetime.datetime(date[0], date[1], date[2])
                insertOver(bus_id, over_type, over_begin_time, over_end_time, over_last_time, date.year, date.month,
                           date.day, date.weekday() + 1, date)

    except Exception as e:
        print(e)

    return


def insertOver(bus_id, types, btime, etime, last_time, years, months, days, weeks, date):
    resp = EmployeeOvertimeStatistics.objects.update_or_create(
        defaults={'bus_id': bus_id,
                  'overtime_type': types,
                  'overtime_start_time': btime,
                  'overtime_stop_time': etime,
                  'overtime_last_time': last_time,
                  'years': years,
                  'months': months,
                  'days': days,
                  'weeks': weeks,
                  'dates': date},
        bus_id=bus_id,
        overtime_type=types,
        overtime_start_time=btime,
        overtime_stop_time=etime,
        dates=date
    )
    print(resp)
