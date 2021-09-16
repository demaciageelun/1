from django.shortcuts import render, render_to_response
from django.http import HttpResponse, FileResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import EmployeeInformation, CheckInDetail, EmployeeDaysStatistics
from .function import decrypto
import json

from .function import holiday, overtime, bustravel, createmonthsta,testdata,updateemp,reportback
from .linshi import overtest, holitest


# Create your views here.
def index(request):

    # createmonthsta.calcDaliySta()
    createmonthsta.monthStatic()
    # testdata.checkinDetail()
    updateemp.getEmp()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def holi(request):
    data = json.loads(decrypto.decrypto(request.body))
    data1 = '{"success": "true"}'
    holiday.proLeaveInfor(data)
    return HttpResponse(data1)


def backs(request):
    data = json.loads(decrypto.decrypto(request.body))
    data1 = '{"success": "true"}'
    reportback.reportbackInfor(data)
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
