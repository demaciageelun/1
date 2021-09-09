# 创建月度报表
from ..models import EmployeeInformation, EmployeeHoildayStatistics, Cal, CheckInDetail
import datetime


def calcMonthSta():
    # 获取上个月的年和月
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month - 1
    # 第一步、获取需要考勤的人员信息
    emp_info = EmployeeInformation.objects.filter(att_type=1, is_job=1)
    # 第二步、先获取上个月的日历信息，所有工作日
    cal_info = Cal.objects.filter(years=year, months=month).exclude(weeks=7)
    # 第三步、获取刷卡数据，并处理
    for emps in emp_info:
        for cals in cal_info:
            check_info = CheckInDetail.objects.filter(bus_id=emps.bus_id, years=cals.years, months=cals.months,
                                                      days=cals.days)
    # 第四步、获取请假数据或者出差数据
    # 第五步、获取加班信息
    # 第六步、遍历人员每日信息，汇总成一整条数据，并写入月度汇总表
