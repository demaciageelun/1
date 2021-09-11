from django.shortcuts import render, render_to_response
from django.http import HttpResponse, FileResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import EmployeeInformation, CheckInDetail, EmployeeDaysStatistics
from .function import decrypto
import json

from .function import holiday, overtime, bustravel, createmonthsta,testdata
from .linshi import overtest, holitest


# Create your views here.
def index(request):
    # emp_days = EmployeeDaysStatistics()
    # emp_days.bus_id = "20080103"
    # emp_days.in_time = None
    # emp_days.out_time = None
    # emp_days.cal_id = 2
    # emp_days.save()
    createmonthsta.calcMonthSta()
    # testdata.getTests()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def holi(request):
    data = json.loads(decrypto.decrypto(request.body))
    data1 = '{"success": "true"}'
    holiday.proLeaveInfor(data)
    return HttpResponse(data1)


def over(request):
    data = json.loads(decrypto.decrypto(request.body))
    data1 = '{"success": "true"}'
    overtime.overTimeInfo(data)
    return HttpResponse(data1)


def travel(request):
    data = json.loads(decrypto.decrypto(request.body))
    data1 = '{"success": "true"}'
    bustravel.bustravelInfo(data)
    return HttpResponse(data1)


def test(request):
    overtest.insert_hoilday()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def hoiltest(request):
    holitest.insert_hoilday()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)
