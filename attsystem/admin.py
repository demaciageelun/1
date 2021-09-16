import json
import time
from django.http import HttpResponse, FileResponse
from django.contrib import admin
from attsystem.models import EmployeeInformation, EmployeeMonthStatistics, Cal, EmployeeHoildayStatistics, \
    EmployeeOvertimeStatistics, EmployeeBustravelStatistics, CheckInDetail, EmployeeDaysStatistics
from .function import updateemp, getcheckdata
from openpyxl import Workbook


# Register your models here.
class EmployeeInformationAdmin(admin.ModelAdmin):
    list_display = ["bus_id", "namse", "dept", "positi", "time1", "time2", "time3", "time4", "att_type",
                    "is_job", "entry_date", "leave_date"]
    list_display_links = ["namse", "dept", "positi"]
    list_per_page = 20
    search_fields = ["bus_id", "namse", "dept"]
    list_filter = ["dept", "att_type", "is_job"]
    list_editable = ["time1", "time2", "time3", "time4", "att_type", "is_job", "entry_date", "leave_date"]
    # 增加自定义按钮
    actions = ['update']

    def update(self, request, queryset):
        resp = updateemp.getEmp()
        self.message_user(request, resp)

    # 显示的文本，与django admin一致
    update.short_description = '同步员工信息'
    # icon，参考element-ui icon与https://fontawesome.com
    update.icon = 'el-icon-edit'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    update.type = 'primary'
    update.confirm = '确定更新？'


class EmployeeMonthStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "dept", "positi", "years", "months", "attendance_days", "act_attendance_days",
                    "sat_attendance_days",
                    "sun_attendance_days",
                    "holi_attendance_days", "evection_days", "usua_overtime", "absence_time", "miss_chock_in_times",
                    "miss_chock_out_times", "late_times", "late_length", "early_leave_times", "early_leave_length",
                    "a_holi", "b_holi", "c_holi", "d_holi", "e_holi", "f_holi", "g_holi", "h_holi", "i_holi", "j_holi",
                    "k_holi", "l_holi", "act_holi_days"]

    def dept(self, obj):
        return obj.bus.dept

    def positi(self, obj):
        return obj.bus.positi

    dept.short_description = "部门"
    positi.short_description = "岗位"

    list_filter = ["bus", "years", "months", "bus__dept"]
    # 增加自定义按钮
    actions = ['download']
    list_per_page = 20

    def bus(self, obj):
        return obj.bus.dept

    def download(self, request, queryset):
        # 创建excel
        # 创建一个Workbook对象
        wb = Workbook()
        # 获取当前活跃的sheet，默认是第一个sheet
        ws = wb.active
        row1 = ['员工姓名', '考勤年', '考勤月', '部门', '岗位', '应出勤(天)', '实际出勤(天)', '周六出勤(天)', '周日出勤(天)', '节假日出勤(天)', '出差(天)',
                '平常加班(时)', '缺勤时间',
                '上班缺卡次数', '下班缺卡次数', '迟到次数', '迟到时长(分钟)', '早退次数', '早退时长(分钟)', '调休假(天)', '事假(天)', '病假(天)', '婚假(天)',
                '产假(天)',
                '陪产假(天)', '哺乳假(天)', '节育假(天)', '工伤假(天)', '看护假(天)', '丧假(天)', '产检假(天)', '实际请假(天)']
        ws.append(row1)
        for data in queryset:
            print(data.bus.dept)
            row2 = [str(data.bus), str(data.years), str(data.months),
                    str(data.bus.dept) if str(data.bus.dept) != "None" else "",
                    str(data.bus.positi) if str(data.bus.positi) != "None" else "",
                    str(data.attendance_days) if str(data.attendance_days) != "None" else "",
                    str(data.act_attendance_days) if str(data.act_attendance_days) != "None" else "",
                    str(data.sat_attendance_days) if str(data.sat_attendance_days) != "None" else "",
                    str(data.sun_attendance_days) if str(data.sun_attendance_days) != "None" else "",
                    str(data.holi_attendance_days) if str(data.holi_attendance_days) != "None" else "",
                    str(data.evection_days) if str(data.evection_days) != "None" else "",
                    str(data.usua_overtime) if str(data.usua_overtime) != "None" else "",
                    str(data.absence_time) if str(data.absence_time) != "None" else "",
                    str(data.miss_chock_in_times) if str(data.miss_chock_in_times) != "None" else "",
                    str(data.miss_chock_out_times) if str(data.miss_chock_out_times) != "None" else "",
                    str(data.late_times) if str(data.late_times) != "None" else "",
                    str(data.late_length) if str(data.late_length) != "None" else "",
                    str(data.early_leave_times) if str(data.early_leave_times) != "None" else "",
                    str(data.early_leave_length) if str(data.early_leave_length) != "None" else "",
                    str(data.a_holi) if str(data.a_holi) != "None" else "",
                    str(data.b_holi) if str(data.b_holi) != "None" else "",
                    str(data.c_holi) if str(data.c_holi) != "None" else "",
                    str(data.d_holi) if str(data.d_holi) != "None" else "",
                    str(data.e_holi) if str(data.e_holi) != "None" else "",
                    str(data.f_holi) if str(data.f_holi) != "None" else "",
                    str(data.g_holi) if str(data.g_holi) != "None" else "",
                    str(data.h_holi) if str(data.h_holi) != "None" else "",
                    str(data.i_holi) if str(data.i_holi) != "None" else "",
                    str(data.j_holi) if str(data.j_holi) != "None" else "",
                    str(data.k_holi) if str(data.k_holi) != "None" else "",
                    str(data.l_holi) if str(data.l_holi) != "None" else "",
                    str(data.act_holi_days) if str(data.act_holi_days) != "None" else ""]
            ws.append(row2)

        wb.save('static/data.xlsx')

        #     下载
        file = open('static/data.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="BatchPayTemplate.xlsx"'
        # self.message_user(request, "123")
        return response

    download.short_description = '下载数据'
    # icon，参考element-ui icon与https://fontawesome.com
    download.icon = 'el-icon-edit'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    download.type = 'primary'
    # download.confirm = '确定下载？'


class CalAdmin(admin.ModelAdmin):
    list_display = ["times", "kinds"]


class EmployeeHoildayStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "hoilday_type", "hoilday_start_time", "hoilday_stop_time", "hoilday_last_time", "dates"]
    raw_id_fields = ["bus"]
    list_filter = ["bus", "hoilday_type", "dates"]


class EmployeeOvertimeStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "overtime_type", "dates",
                    "weeks", "overtime_start_time", "overtime_stop_time", "overtime_last_time"]
    raw_id_fields = ["bus"]
    list_filter = ["bus", "overtime_type", "dates", "weeks"]


class EmployeeBustravelStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "dates",
                    "weeks", "bustravel_start_time", "bustravel_stop_time", "bustravel_last_time", "go_out_type",
                    "serial"]
    raw_id_fields = ["bus"]


class CheckInDetailAdmin(admin.ModelAdmin):
    list_display = ["bus", "check_date", "weeks", "checkin_time"]
    list_filter = ["bus", "weeks", "check_date"]
    actions = ["get_check_data", "test"]

    def get_check_data(self, request, queryset):
        resp = getcheckdata.checkinDetail()
        self.message_user(request, resp)

    get_check_data.short_description = '获取考勤数据'
    # icon，参考element-ui icon与https://fontawesome.com
    get_check_data.icon = 'el-icon-edit'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    get_check_data.type = 'primary'

    def test(self, request, queryset):
        pass

    test.short_description = '测试按钮'
    # icon，参考element-ui icon与https://fontawesome.com
    test.icon = 'el-icon-edit'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    test.type = 'primary'
    test.acts_on_all = True


class EmployeeDaysStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "cal", "cal_weeks", "act_times", "in_time", "out_time", "judge_in_time", "judge_out_time",
                    "holi_in_time", "holi_out_time", "hoil_last_time",
                    "over_in_time", "over_out_time", "over_last_time", "check_in_result", "check_out_result",
                    "late_time",
                    "leaveearly_time", "absence_times"]
    list_filter = ["bus", "cal", "cal__years", "cal__months", "cal__days", "check_in_result", "check_out_result"]

    def cal_weeks(self, obj):
        return obj.cal.weeks

    cal_weeks.short_description = "周几"
    list_per_page = 20


admin.site.site_header = '谷登考勤系统后台'
admin.site.site_title = '谷登考勤系统后台'
admin.site.index_title = '欢迎使用谷登考勤系统后台'
admin.site.register(EmployeeInformation, EmployeeInformationAdmin)
admin.site.register(EmployeeMonthStatistics, EmployeeMonthStatisticsAdmin)
admin.site.register(Cal, CalAdmin)
admin.site.register(EmployeeHoildayStatistics, EmployeeHoildayStatisticsAdmin)
admin.site.register(EmployeeOvertimeStatistics, EmployeeOvertimeStatisticsAdmin)
admin.site.register(EmployeeBustravelStatistics, EmployeeBustravelStatisticsAdmin)
admin.site.register(CheckInDetail, CheckInDetailAdmin)
admin.site.register(EmployeeDaysStatistics, EmployeeDaysStatisticsAdmin)
