# 创建月度报表
import time
import arrow
from django.db.models import Q, Sum, Count

from ..models import EmployeeInformation, EmployeeHoildayStatistics, Cal, CheckInDetail, EmployeeOvertimeStatistics, \
    EmployeeDaysStatistics, EmployeeMonthStatistics, EmployeeBustravelStatistics
import datetime


# 计算上月每日考勤状态表
def calcDaliySta():
    # 获取上个月的年和月
    # year = datetime.datetime.now().year
    # month = datetime.datetime.now().month - 1
    # 上个月的年和月
    date = arrow.now().shift(months=-1)
    # 第一步、获取需要考勤的人员信息
    emp_info = EmployeeInformation.objects.filter(att_type=1, is_job=1)
    for emps in emp_info:
        # 第二步、先获取上个月的入职日期之后，离职日期之前的日历信息
        if emps.leave_date is None and emps.entry_date is None:
            cal_info = Cal.objects.filter(years=date.year, months=date.month)
        elif emps.leave_date is not None and emps.entry_date is None:
            cal_info = Cal.objects.filter(years=date.year, months=date.month, times__lte=emps.leave_date)
        elif emps.leave_date is None and emps.entry_date is not None:
            cal_info = Cal.objects.filter(years=date.year, months=date.month, times__gte=emps.entry_date)
        else:
            cal_info = Cal.objects.filter(years=date.year, months=date.month, times__gte=emps.entry_date,
                                          times__lte=emps.leave_date)

        for cals in cal_info:
            # 第三步、获取刷卡数据，
            check_data = CheckInDetail.objects.filter(bus_id=emps.bus_id, check_date=cals.times).order_by(
                "checkin_time")
            # 刷卡数据去重

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
                    EmployeeDaysStatistics.objects.update_or_create(
                        defaults={'bus_id': emps.bus_id,
                                  'in_time': check_data[0].checkin_time if len(check_data) > 0 else None,
                                  'out_time': check_data[len(check_data) - 1].checkin_time if len(
                                      check_data) > 1 else None,
                                  'over_in_time': over_data[0].overtime_start_time,
                                  'over_out_time': over_data[0].overtime_stop_time,
                                  'over_last_time': over_last_time,
                                  'cal_id': cals.id
                                  },
                        bus_id=emps.bus_id,
                        cal_id=cals.id
                    )
            # 处理工作日。工作日统计签到考勤数据和加班请假出差数据，并且根据请假等信息判断每日出勤。
            else:
                # 先把工作日的人员信息写上
                EmployeeDaysStatistics.objects.update_or_create(
                    defaults={
                        'bus_id': emps.bus_id,
                        'cal_id': cals.id
                    },
                    bus_id=emps.bus_id,
                    cal_id=cals.id
                )
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
                # 存在一天请多次假的情况，有请假的，当天出勤要减去请假时长，并且判断上下班迟到早退的时间也随之变化
                holi_last_time = 0
                if len(holi_data) != 0:
                    holi_judeg = []
                    for holis in holi_data:
                        holi_judeg.append(holis.hoilday_start_time)
                        holi_judeg.append(holis.hoilday_stop_time)
                        holi_last_time += holis.hoilday_last_time
                    holi_judeg.sort()
                    # 计算上下班刷卡的标定时间
                    if holi_last_time >= 1:
                        # 全天请假，不考虑上下班刷卡时间
                        pass
                    else:
                        # 第一种，请假时间在time1和time4之间的，以time1和time4为准
                        if holi_judeg[0] > emps.time1 and holi_judeg[len(holi_judeg) - 1] < emps.time4:
                            check_intime = emps.time1
                            check_outtime = emps.time4
                        elif holi_judeg[0] <= emps.time1 and holi_judeg[len(holi_judeg) - 1] < emps.time2:
                            check_intime = holi_judeg[len(holi_judeg) - 1]
                            check_outtime = emps.time4
                        elif holi_judeg[0] <= emps.time1 and holi_judeg[len(holi_judeg) - 1] >= emps.time2 and \
                                holi_judeg[len(holi_judeg) - 1] <= emps.time3:
                            check_intime = emps.time3
                            check_outtime = emps.time4
                        elif holi_judeg[0] <= emps.time1 and holi_judeg[len(holi_judeg) - 1] > emps.time3 and \
                                holi_judeg[len(holi_judeg) - 1] < emps.time4:
                            check_intime = holi_judeg[len(holi_judeg) - 1]
                            check_outtime = emps.time4
                        elif holi_judeg[len(holi_judeg) - 1] >= emps.time4 and holi_judeg[0] > emps.time1 and \
                                holi_judeg[0] < emps.time2:
                            check_intime = emps.time1
                            check_outtime = holi_judeg[0]
                        elif holi_judeg[len(holi_judeg) - 1] >= emps.time4 and holi_judeg[0] > emps.time2 and \
                                holi_judeg[0] <= emps.time3:
                            check_intime = emps.time1
                            check_outtime = emps.time2
                        elif holi_judeg[len(holi_judeg) - 1] >= emps.time4 and holi_judeg[0] > emps.time3 and \
                                holi_judeg[0] < emps.time4:
                            check_intime = emps.time1
                            check_outtime = holi_judeg[0]
                            pass

                    EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                        holi_in_time=holi_data[0].hoilday_start_time,
                        holi_out_time=holi_data[len(holi_data) - 1].hoilday_stop_time,
                        hoil_last_time=holi_last_time, act_times=1 - holi_last_time, judge_in_time=check_intime,
                        judge_out_time=check_outtime)
                # 没有请假的额，则当天出勤为1
                else:
                    # 刷卡标定时间
                    check_intime = emps.time1
                    check_outtime = emps.time4
                    EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(act_times=1,
                                                                                                     judge_in_time=check_intime,
                                                                                                     judge_out_time=check_outtime)

                # 根据实际刷卡时间和标定刷卡时间判断迟到、早退、缺勤。排除请假时长一天的，不考虑。
                # 请假少于1天并且出差小于1天的，计算上下班缺卡，迟到早退等。
                if holi_last_time < 1:
                    if len(check_data) == 0:
                        # 上下班都缺卡
                        EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                            check_in_result=3, check_out_result=3)
                    elif len(check_data) == 1:
                        # 判断是上班或者下班缺卡，并判断是否迟早或者早退
                        # 1、先判断该次刷卡为上班刷卡，还是下班刷卡，则另一次为缺卡。根据这次刷卡时间与两个标定刷卡时间的比值的绝对值判断，绝对值小的，就为该次刷卡。
                        # 2、这一次还要判断是否迟到早退。
                        judge_time = time.mktime(
                            time.strptime(str(check_data[0].check_date) + " " + str(check_data[0].checkin_time),
                                          "%Y-%m-%d %H:%M:%S"))
                        judge_check_intime = time.mktime(
                            time.strptime(str(check_data[0].check_date) + " " + str(check_intime),
                                          "%Y-%m-%d %H:%M:%S"))
                        judge_check_outtime = time.mktime(
                            time.strptime(str(check_data[0].check_date) + " " + str(check_outtime),
                                          "%Y-%m-%d %H:%M:%S"))
                        abs_in_time = abs(judge_time - judge_check_intime)
                        abs_out_time = abs(judge_time - judge_check_outtime)
                        # 这个时间是下班时间，则上班为缺卡，还要判断下班是否早退
                        if abs_in_time > abs_out_time:
                            EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                check_in_result=3)
                            # 判断下班是否早退
                            if judge_time >= judge_check_outtime:
                                EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                    check_out_result=1, out_time=check_data[0].checkin_time)
                            else:
                                EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                    check_out_result=2, out_time=check_data[0].checkin_time,
                                    leaveearly_time=(judge_check_outtime - judge_time) / 60)
                        # 这个时间是上班时间，则下班是缺卡，还要判断上班是否迟到
                        else:
                            EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                check_out_result=3)
                            # 判断上班是否迟到
                            if judge_check_intime - judge_time >= -60:
                                EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                    check_in_result=1, in_time=check_data[0].checkin_time)
                            else:
                                EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                    check_in_result=2, in_time=check_data[0].checkin_time,
                                    late_time=(judge_time - judge_check_intime - 60) / 60)
                    else:
                        # 判断上下班刷卡时间，并判断是上班或者下班缺卡，并判断是否迟早或者早退
                        judge_time1 = time.mktime(
                            time.strptime(str(check_data[0].check_date) + " " + str(check_data[0].checkin_time),
                                          "%Y-%m-%d %H:%M:%S"))
                        judge_time2 = time.mktime(
                            time.strptime(
                                str(check_data[0].check_date) + " " + str(check_data[len(check_data) - 1].checkin_time),
                                "%Y-%m-%d %H:%M:%S"))
                        judge_check_intime = time.mktime(
                            time.strptime(str(check_data[0].check_date) + " " + str(check_intime),
                                          "%Y-%m-%d %H:%M:%S"))
                        judge_check_outtime = time.mktime(
                            time.strptime(str(check_data[0].check_date) + " " + str(check_outtime),
                                          "%Y-%m-%d %H:%M:%S"))
                        # 正常签到
                        if judge_time1 <= judge_check_intime + 60 and judge_time2 >= judge_check_outtime:
                            EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                check_in_result=1, check_out_result=1, in_time=check_data[0].checkin_time,
                                out_time=check_data[len(check_data) - 1].checkin_time)
                        #     上班迟到，下班正常
                        elif judge_time1 > judge_check_intime + 60 and judge_time2 >= judge_check_outtime:
                            EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                check_in_result=2, check_out_result=1, in_time=check_data[0].checkin_time,
                                out_time=check_data[len(check_data) - 1].checkin_time,
                                late_time=(judge_time1 - judge_check_intime - 60) / 60)
                        #     上班正常，下班早退
                        elif judge_time1 <= judge_check_intime + 60 and judge_time2 < judge_check_outtime:
                            check_out_result = 2
                            EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                check_in_result=1, check_out_result=2, in_time=check_data[0].checkin_time,
                                out_time=check_data[len(check_data) - 1].checkin_time,
                                leaveearly_time=(judge_check_outtime - judge_time2) / 60)
                        #     上班迟到,下班早退
                        else:
                            check_out_result = 2
                            EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                                check_in_result=2, check_out_result=2, in_time=check_data[0].checkin_time,
                                out_time=check_data[len(check_data) - 1].checkin_time,
                                late_time=(judge_time1 - judge_check_intime - 60) / 60,
                                leaveearly_time=(judge_check_outtime - judge_time2) / 60)
                # 1判断是否有出差的，2判断出差结束时间是否大于等于下班刷卡时间3是否早退
                travel_data = EmployeeBustravelStatistics.objects.filter(bus_id=emps.bus_id, dates=cals.times)
                # 一天出差几次
                if len(travel_data) > 0:
                    travel_data_list = []
                    travel_last_time = 0
                    for datas in travel_data:
                        travel_data_list.append(datas.bustravel_start_time)
                        travel_data_list.append(datas.bustravel_stop_time)
                        travel_last_time += datas.bustravel_last_time
                    travel_data_list.sort()
                    EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                        bustravel_start_time=travel_data_list[0],
                        bustravel_stop_time=travel_data_list[len(travel_data_list) - 1],
                        bustravel_last_time=travel_last_time)
                    # 出差结束时间是否大于等于下班刷卡时间并且下班缺卡，则设置为正常
                    if travel_data_list[len(travel_data_list) - 1] > check_outtime and check_out_result == 2:
                        EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id=cals.id).update(
                            check_out_result=1, leaveearly_time=None)

                    # 第四步、获取请假数据或者出差数据
                    # 第五步、获取加班信息
                    # 第六步、遍历人员每日信息，汇总成一整条数据，并写入月度汇总表
                    # 遍历出差数据，如果当日有出差数据，则将


def monthStatic():
    # 上个月的年和月
    date = arrow.now().shift(months=-1)
    # 上上个月最后一天
    arrow_date = arrow.now().shift(months=-1, days=-15)

    # 计算当月应考勤天
    cal_data = Cal.objects.filter(years=date.year, months=date.month).exclude(kinds__in=(3, 4)).count()
    # 查询所有记录考勤的人员，遍历。去除掉上个月已经离职的人员。
    # 生成上上月最后一天的日期。
    emp_data = EmployeeInformation.objects.filter(
        Q(att_type=1),
        # Q(is_job=1),
        Q(leave_date__isnull=True) | Q(leave_date__gt=arrow_date.date())
    )
    for emps in emp_data:
        # 遍历每日信息表，汇总实际出勤，周六出勤、周日出勤、平时加班、迟到、早退等信息
        # 实际出勤天
        act_attendance_days = EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id,
                                                                    cal_id__months=date.month).aggregate(
            sum=Sum("act_times"))['sum']
        # 周六出勤天
        sat_attendance_days = EmployeeDaysStatistics.objects.filter(bus_id=emps.bus_id, cal_id__months=date.month,
                                                                    cal_id__kinds=2).aggregate(
            sum=Sum("act_times"))['sum']
        # 周日出勤（周六加班+周日加班）
        sun_attendance_days = EmployeeDaysStatistics.objects.filter(
            Q(bus_id=emps.bus_id), Q(cal_id__months=date.month), Q(cal_id__kinds=2) | Q(cal_id__kinds=3)).aggregate(
            sum=Sum("over_last_time"))['sum']
        sun_attendance_days = sun_attendance_days / 8 if sun_attendance_days is not None else 0
        # 假日加班
        holi_attendance_days = EmployeeDaysStatistics.objects.filter(
            bus_id=emps.bus_id, cal_id__months=date.month, cal_id__kinds=4).aggregate(
            sum=Sum("over_last_time"))['sum']
        holi_attendance_days = holi_attendance_days / 8 if holi_attendance_days is not None else 0
        # 平时加班
        usua_overtime = EmployeeDaysStatistics.objects.filter(
            bus_id=emps.bus_id, cal_id__months=date.month, cal_id__kinds=1).aggregate(
            sum=Sum("over_last_time"))['sum']
        usua_overtime = usua_overtime if usua_overtime is not None else 0
        # 缺勤次数
        # 迟到次数和迟到时长
        lates = EmployeeDaysStatistics.objects.filter(
            bus_id=emps.bus_id, cal_id__months=date.month, check_in_result=2).aggregate(
            count=Count("check_in_result"), sum=Sum("late_time"))
        late_times = lates["count"] if lates["count"] is not None else 0
        # 迟到时长
        late_length = lates["sum"] if lates["sum"] is not None else 0
        # 早退次数和早退时长
        earlys = EmployeeDaysStatistics.objects.filter(
            bus_id=emps.bus_id, cal_id__months=date.month, check_out_result=2).aggregate(
            count=Count("check_out_result"), sum=Sum("leaveearly_time"))
        early_leave_times = earlys["count"] if earlys["count"] is not None else 0
        # 迟到时长
        early_leave_length = earlys["sum"] if earlys["sum"] is not None else 0
        # 上班缺卡次数
        miss_chock_in_times = EmployeeDaysStatistics.objects.filter(
            bus_id=emps.bus_id, cal_id__months=date.month, check_in_result=3).aggregate(
            count=Count("check_in_result"))["count"]
        miss_chock_in_times = miss_chock_in_times if miss_chock_in_times is not None else 0
        # 下班缺卡次数
        miss_chock_out_times = EmployeeDaysStatistics.objects.filter(
            bus_id=emps.bus_id, cal_id__months=date.month, check_out_result=3).aggregate(
            count=Count("check_in_result"))["count"]
        miss_chock_out_times = miss_chock_out_times if miss_chock_out_times is not None else 0
        # 各种请假汇总
        holiday_info = EmployeeHoildayStatistics.objects.filter(bus_id=emps.bus_id, years=date.year,
                                                                months=date.month).values("bus_id",
                                                                                          "hoilday_type").annotate(
            sum=Sum("hoilday_last_time"))
        a_holi = 0
        b_holi = 0
        c_holi = 0
        d_holi = 0
        e_holi = 0
        f_holi = 0
        g_holi = 0
        h_holi = 0
        i_holi = 0
        j_holi = 0
        k_holi = 0
        l_holi = 0
        if len(holiday_info) > 0:
            for holidatas in holiday_info:
                if holidatas["hoilday_type"] == "a":
                    a_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "b":
                    b_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "c":
                    c_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "d":
                    d_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "e":
                    e_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "f":
                    f_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "g":
                    g_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "h":
                    h_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "i":
                    i_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "j":
                    j_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "k":
                    k_holi = holidatas["sum"]
                elif holidatas["hoilday_type"] == "l":
                    l_holi = holidatas["sum"]
        # 实际请假天
        act_holi_days = EmployeeHoildayStatistics.objects.filter(bus_id=emps.bus_id, years=date.year,
                                                                 months=date.month).values("bus_id").annotate(
            sum=Sum("hoilday_last_time"))
        if len(act_holi_days) > 0:
            act_holi_days = act_holi_days[0]["sum"]
        else:
            act_holi_days = 0
        EmployeeMonthStatistics.objects.update_or_create(
            defaults={'bus_id': emps.bus_id,
                      'years': date.year,
                      'months': date.month,
                      'attendance_days': cal_data,
                      'act_attendance_days': act_attendance_days,
                      'sat_attendance_days': sat_attendance_days,
                      'sun_attendance_days': sun_attendance_days,
                      'holi_attendance_days': holi_attendance_days,
                      'usua_overtime': usua_overtime,
                      'miss_chock_in_times': miss_chock_in_times,
                      'miss_chock_out_times': miss_chock_out_times,
                      'late_times': late_times,
                      'late_length': late_length,
                      'early_leave_times': early_leave_times,
                      'early_leave_length': early_leave_length,
                      'a_holi': a_holi,
                      'b_holi': b_holi,
                      'c_holi': c_holi,
                      'd_holi': d_holi,
                      'e_holi': e_holi,
                      'f_holi': f_holi,
                      'g_holi': g_holi,
                      'h_holi': h_holi,
                      'i_holi': i_holi,
                      'j_holi': j_holi,
                      'k_holi': k_holi,
                      'l_holi': l_holi,
                      'act_holi_days': act_holi_days
                      },
            bus_id=emps.bus_id,
            years=date.year,
            months=date.month,

        )
