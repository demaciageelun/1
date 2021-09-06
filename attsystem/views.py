from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import EmployeeInformation
from .function import decrypto
import json

from .function import holiday, overtime, bustravel, getemployee
from .linshi import overtest, holitest


# Create your views here.
def index(request):
    # data = EmployeeInformation.objects.order_by('bus_id')[:5]
    # print(data)
    # template = loader.get_template("emp/index.html")
    # context = {
    #     "data": data
    # }
    return render(request, "emp/index.html")


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


def empInfo(request):
    getemployee.getEmp()
    data1 = '{"success": "12313"}'
    return HttpResponse(data1)
