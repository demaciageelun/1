from attsystem.models import EmployeeInformation, EmployeeOvertimeStatistics
from openpyxl import load_workbook
import datetime


def judge(data):
    if data == '工作日加班':
        return 1
    elif data == '周末加班':
        return 2
    else:
        return 3


def insert_hoilday():
    print(1)
    # fileName 这里是指文件路径
    fileName = "static/HR02.xlsx"
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
        months = row[13].value[5:7]
        overtime_type = judge(row[11].value)
        overtime_start_time = row[13].value
        overtime_stop_time = row[14].value
        overtime_last_time = float(row[15].value)
        weeks = datetime.datetime.strptime(overtime_start_time[:10], "%Y-%m-%d").weekday() + 1
        years = datetime.datetime.strptime(overtime_start_time[:10], "%Y-%m-%d").year
        months = datetime.datetime.strptime(overtime_start_time[:10], "%Y-%m-%d").month
        days = datetime.datetime.strptime(overtime_start_time[:10], "%Y-%m-%d").day
        insertOver(bus_id, overtime_type, overtime_start_time, overtime_stop_time, overtime_last_time, years, months,
                   days, weeks, overtime_start_time[:10])


def insertOver(bus_id, types, btime, etime, last_time, years, months, days, weeks, date):
    resp = EmployeeOvertimeStatistics.objects.create(bus_id=bus_id, overtime_type=types,
                                                     overtime_start_time=btime,
                                                     overtime_stop_time=etime, overtime_last_time=last_time,
                                                     years=years,
                                                     months=months, days=days, weeks=weeks, dates=date)
    print(resp)
