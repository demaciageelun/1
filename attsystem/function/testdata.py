from ..models import EmployeeOvertimeStatistics, EmployeeMonthStatistics
from django.db.models import Sum, Count, Max, Min, Avg


def getTests():
    over_data = EmployeeOvertimeStatistics.objects.filter(weeks=7).values("bus_id").annotate(
        sum=Sum("overtime_last_time") / 8)
    for datas in over_data:
        EmployeeMonthStatistics.objects.filter(bus_id=datas["bus_id"]).update(sun_attendance_days=datas["sum"])
