from django.shortcuts import render, render_to_response
from django.http import HttpResponse, FileResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import EmployeeInformation
from .function import decrypto
import json

from .function import holiday, overtime, bustravel
from .linshi import overtest, holitest


# Create your views here.
def index(request):
    print(request)
    file = open('static/HR01.xlsx', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="BatchPayTemplate.xls"'
    return response


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


