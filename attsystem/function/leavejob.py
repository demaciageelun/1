from attsystem.models import EmployeeInformation
import time


# 接收views接收到的请假信息，处理存入请假信息表中
def leave(data):
    try:
        openid = data["data"]["basicInfo"]["myPersonInfo"]["oid"]
        leave_time = data["data"]["formInfo"]["widgetMap"]["Da_1"]["value"]
        timeArray = time.localtime(int(str(leave_time)[:10]))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        leave_data = otherStyleTime[:10]
        EmployeeInformation.objects.filter(bus_id=openid).update(leave_date=leave_data, is_job=2)
    except Exception as e:
        print(e)
