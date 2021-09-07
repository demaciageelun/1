import time

from django.contrib import admin
from attsystem.models import EmployeeInformation, EmployeeMonthStatistics, Cal, EmployeeHoildayStatistics, \
    EmployeeOvertimeStatistics, EmployeeBustravelStatistics
from .function import updateemp

# Register your models here.
class EmployeeInformationAdmin(admin.ModelAdmin):
    list_display = ["bus_id", "namse", "dept", "positi", "openid", "time1", "time2", "time3", "time4", "att_type"]
    list_display_links = ["namse", "dept", "positi", "openid"]
    list_per_page = 20
    search_fields = ["namse", "dept"]
    list_filter = ["dept"]
    list_editable = ["time1", "time2", "time3", "time4", "att_type"]
    # 增加自定义按钮
    actions = ['custom_button']

    def custom_button(self, request, queryset):
        updateemp.getEmp()
        self.message_user(request, "123")

    # 显示的文本，与django admin一致
    custom_button.short_description = '同步员工信息'
    # icon，参考element-ui icon与https://fontawesome.com
    custom_button.icon = 'el-icon-edit'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'primary'



class EmployeeMonthStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "attendance_days", "act_attendance_days", "sat_attendance_days", "sun_attendance_days",
                    "holi_attendance_days", "usua_overtime", "a_holi"]
    list_filter = ["months"]


class CalAdmin(admin.ModelAdmin):
    list_display = ["times", "kinds"]


class EmployeeHoildayStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "hoilday_type", "hoilday_start_time", "hoilday_stop_time", "hoilday_last_time", "dates"]
    raw_id_fields = ["bus"]


class EmployeeOvertimeStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "overtime_type", "dates",
                    "weeks", "overtime_start_time", "overtime_stop_time", "overtime_last_time"]
    raw_id_fields = ["bus"]


class EmployeeBustravelStatisticsAdmin(admin.ModelAdmin):
    list_display = ["bus", "dates",
                    "weeks", "bustravel_start_time", "bustravel_stop_time", "bustravel_last_time"]
    raw_id_fields = ["bus"]


admin.site.site_header = '谷登考勤系统后台'
admin.site.site_title = '谷登考勤系统后台'
admin.site.index_title = '欢迎使用谷登考勤系统后台'
admin.site.register(EmployeeInformation, EmployeeInformationAdmin)
admin.site.register(EmployeeMonthStatistics, EmployeeMonthStatisticsAdmin)
admin.site.register(Cal, CalAdmin)
admin.site.register(EmployeeHoildayStatistics, EmployeeHoildayStatisticsAdmin)
admin.site.register(EmployeeOvertimeStatistics, EmployeeOvertimeStatisticsAdmin)
admin.site.register(EmployeeBustravelStatistics, EmployeeBustravelStatisticsAdmin)
