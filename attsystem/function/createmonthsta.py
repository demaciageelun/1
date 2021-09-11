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
    for emps in emp_info:
        # 第二步、先获取上个月的入职日期之后，离职日期之前的日历信息
        if emps.leave_date is None and emps.entry_date is None:
            cal_info = Cal.objects.filter(years=year, months=month)
        elif emps.leave_date is not None and emps.entry_date is None:
            cal_info = Cal.objects.filter(years=year, months=month, times__lte=emps.leave_date)
        elif emps.leave_date is None and emps.entry_date is not None:
            cal_info = Cal.objects.filter(years=year, months=month, times__gte=emps.entry_date)
        else:
            cal_info = Cal.objects.filter(years=year, months=month, times__gte=emps.entry_date,
                                          times__lte=emps.leave_date)
        # 第三步、获取刷卡数据，
        for cals in cal_info:
            # 获取刷卡数据()
            check_data = CheckInDetail.objects.filter(bus_id=emps.bus_id, check_date=cals.times).order_by(
                "checkin_time")
            # 处理星期日和节假日。因为星期日和节假日不计迟到早退信息，只统计加班信息
            if cals.kinds == 3 or cals.kinds == 4:
                # 获取加班数据
                over_data = EmployeeOvertimeStatistics.objects.filter(bus_id=emps.bus_id, dates=cals.times)
                if len(over_data) != 0:
                    over_last_time = 0
                    # 当天加班持续时间相加（存在一天加2次班的情况）
                    for overs in over_data:
                        over_last_time += overs.overtime_last_time
                    # 写入每日数据表
                    emp_days = EmployeeDaysStatistics()
                    emp_days.bus_id = emps.bus_id
                    emp_days.in_time = check_data[0].checkin_time if len(check_data) > 0 else None
                    emp_days.out_time = check_data[len(check_data) - 1].checkin_time if len(check_data) > 1 else None
                    emp_days.over_in_time = over_data[0].overtime_start_time
                    emp_days.over_out_time = over_data[0].overtime_stop_time
                    emp_days.over_last_time = over_last_time
                    emp_days.cal_id = cals.id
                    emp_days.save()
            # 处理工作日。工作日统计签到考勤数据和加班请假出差数据，并且根据请假等信息判断每日出勤。
            else:
                emp_days = EmployeeDaysStatistics()
                emp_days.bus_id = emps.bus_id
                emp_days.cal_id = cals.id
                emp_days.save()
                # 获取加班数据
                over_data = EmployeeOvertimeStatistics.objects.filter(bus_id=emps.bus_id, dates=cals.times)
                if len(over_data) != 0:
                    over_last_time = 0
                    # 当天加班持续时间相加（存在一天加2次班的情况）
                    for overs in over_data:
                        over_last_time += overs.overtime_last_time
                    EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                        over_in_time=over_data[0].overtime_start_time, over_out_time=over_data[0].overtime_stop_time,
                        over_last_time=over_last_time)
                # 获取请假数据
                holi_data = EmployeeHoildayStatistics.objects.filter(bus_id=emps.bus_id, dates=cals.times)
                # 存在一天请多次假的情况
                if len(holi_data) != 0:
                    holi_last_time = 0
                    for holis in holi_data:
                        holi_last_time += holis.hoilday_last_time
                    EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                        holi_in_time=holi_data[0].hoilday_start_time,
                        holi_out_time=holi_data[len(holi_data) - 1].hoilday_stop_time,
                        hoil_last_time=holi_last_time, act_times=1 - holi_last_time)
                else:
                    EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(act_times=1)
    # 第四步、获取请假数据或者出差数据
    # 第五步、获取加班信息
    # 第六步、遍历人员每日信息，汇总成一整条数据，并写入月度汇总表


def changeTime(data):
    pass
