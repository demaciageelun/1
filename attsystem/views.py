# from django.shortcuts import render, render_to_response
from django.http import HttpResponse, FileResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import EmployeeInformation, CheckInDetail, EmployeeDaysStatistics
from .function import decrypto
import json

from .function import holiday, overtime, bustravel, createmonthsta, testdata, updateemp, reportback, getcheckdata, \
    leavejob
from .linshi import overtest as ot, holitest, checkdata


# Create your views here.
def index(request):
    # createmonthsta.calcDaliySta()
    # createmonthsta.monthStatic()
    # testdata.checkinDetail()
    # updateemp.getEmp()
    print('test123')
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


def overtest(request):
    ot.insert_hoilday()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def hoiltest(request):
    holitest.insert_hoilday()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def updateEmp(request):
    updateemp.getEmp()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def checkdata(request):
    getcheckdata.checkinDetail()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def daliy(request):
    # createmonthsta.calcDaliySta()
    data1 = createmonthsta.calcDaliySta()
    return HttpResponse(data1)


def monthliy(request):
    # createmonthsta.monthStatic()
    data1 = createmonthsta.monthStatic()
    return HttpResponse(data1)


def leaveinterface(request):
    data = json.loads(decrypto.decrypto(request.body))
    leavejob.leave(data)
    data1 = '{"success": "true"}'
    return HttpResponse(data1)


def testcheckdata(request):
    checkdata.checkinDetail()
    data1 = '{"success": "true"}'
    return HttpResponse(data1)
