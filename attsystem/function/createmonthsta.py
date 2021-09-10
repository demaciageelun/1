# 创建月度报表
from ..models import EmployeeInformation, EmployeeHoildayStatistics, Cal, CheckInDetail, EmployeeOvertimeStatistics, \
    EmployeeDaysStatistics
import datetime


def calcMonthSta():
    # 获取上个月的年和月
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month - 1
    # 第一步、获取需要考勤的人员信息
    emp_info = EmployeeInformation.objects.filter(att_type=1, is_job=1)
    # 第二步、先获取上个月的日历信息，所有日期数据
    cal_info = Cal.objects.filter(years=year, months=month)
    # 第三步、获取刷卡数据，
    for emps in emp_info:
        for cals in cal_info:
            # 处理星期日和节假日。因为星期日和节假日不计考勤，只统计加班信息
            if cals.kinds == 3 or cals.kinds == 4:
                # 获取加班数据
                over_data = EmployeeOvertimeStatistics.objects.filter(bus_id=emps.bus_id, dates=cals.times)
                if len(over_data) != 0:
                    over_last_time = 0
                    # 当天加班持续时间相加（存在一天加2次班的情况）
                    for overs in over_data:
                        over_last_time += overs.overtime_last_time
                    # 获取刷卡数据()
                    check_data = CheckInDetail.objects.filter(bus_id=emps.bus_id, check_date=cals.times).order_by(
                        "checkin_time")
                    # 写入每日数据表
                    # bus_id = emps.bus_id
                    # in_time = check_data[0].checkin_time if len(check_data) > 0 else None
                    # out_time = check_data[len(check_data)].checkin_time if len(check_data) > 0 else None
                    # over_in_time = over_data[0].overtime_start_time
                    # over_out_time = over_data[0].overtime_stop_time
                    # cal_id = cals.id

                    print(emps.bus_id)
                    print(cals.times)
                    emp_days = EmployeeDaysStatistics()
                    emp_days.bus_id = emps.bus_id
                    emp_days.in_time = check_data[0].checkin_time if len(check_data) > 0 else None
                    emp_days.out_time = check_data[len(check_data)-1].checkin_time if len(check_data) > 0 else None
                    emp_days.over_in_time = over_data[0].overtime_start_time
                    emp_days.over_out_time = over_data[0].overtime_stop_time
                    emp_days.over_last_time = over_last_time
                    emp_days.cal_id = cals.id
                    emp_days.save()
            # 处理工作日。工作日统计签到考勤数据和加班请假出差数据。
            else:
                check_info = CheckInDetail.objects.filter(bus_id=emps.bus_id, years=cals.years, months=cals.months,
                                                          days=cals.days)

    # 第四步、获取请假数据或者出差数据
    # 第五步、获取加班信息
    # 第六步、遍历人员每日信息，汇总成一整条数据，并写入月度汇总表
