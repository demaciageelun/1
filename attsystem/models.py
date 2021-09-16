# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AttsystemTest(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'attsystem_test'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


choice = (
    (1, '普通工作日'),
    (2, '周六工作日'),
    (3, '周日'),
    (4, '节假日')
)


class Cal(models.Model):
    times = models.DateField(blank=True, null=True, verbose_name="日期")
    years = models.IntegerField(blank=True, null=True, verbose_name="年")
    months = models.IntegerField(blank=True, null=True, verbose_name="月")
    days = models.IntegerField(blank=True, null=True, verbose_name="日")
    weeks = models.IntegerField(blank=True, null=True, verbose_name="周几")
    kinds = models.IntegerField(blank=True, null=True, verbose_name="类型", choices=choice)

    def __str__(self):
        return str(self.times)

    class Meta:
        managed = False
        db_table = 'cal'
        verbose_name = '工作日历'


class CheckInDetail(models.Model):
    bus = models.ForeignKey('EmployeeInformation', models.DO_NOTHING, verbose_name="员工名字")
    check_date = models.DateField(verbose_name="刷卡日期")
    checkin_time = models.TimeField(verbose_name="刷卡时间")
    weeks = models.IntegerField(verbose_name="周几")
    years = models.IntegerField(blank=True, null=True)
    months = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'check_in_detail'
        verbose_name = '刷卡流水表'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


check_in_result_choice = (
    (1, "正常"),
    (2, "迟到"),
    (3, "缺卡"),
)
check_out_result_choice = (
    (1, "正常"),
    (2, "早退"),
    (3, "缺卡"),
)


class EmployeeDaysStatistics(models.Model):
    bus = models.ForeignKey('EmployeeInformation', models.DO_NOTHING, verbose_name="员工名字")
    in_time = models.TimeField(blank=True, null=True, verbose_name="上班刷卡时间")
    out_time = models.TimeField(blank=True, null=True, verbose_name="下班刷卡时间")
    judge_in_time = models.TimeField(blank=True, null=True, verbose_name="标定上班刷卡时间")
    judge_out_time = models.TimeField(blank=True, null=True, verbose_name="标定下班刷卡时间")
    act_times = models.FloatField(blank=True, null=True, verbose_name="实际出勤(天)")
    holi_in_time = models.TimeField(blank=True, null=True, verbose_name="请假开始时间")
    holi_out_time = models.TimeField(blank=True, null=True, verbose_name="请假结束时间")
    hoil_last_time = models.FloatField(blank=True, null=True, verbose_name="请假持续时间(天)")
    over_in_time = models.DateTimeField(blank=True, null=True, verbose_name="加班开始时间")
    over_out_time = models.DateTimeField(blank=True, null=True, verbose_name="加班结束时间")
    over_last_time = models.FloatField(blank=True, null=True, verbose_name="加班持续时长(小时)")
    check_in_result = models.IntegerField(blank=True, null=True, verbose_name="上班签到结果",
                                          choices=check_in_result_choice)
    check_out_result = models.IntegerField(blank=True, null=True, verbose_name="下班签到结果",
                                           choices=check_out_result_choice)
    late_time = models.IntegerField(blank=True, null=True, verbose_name="迟到时长")
    leaveearly_time = models.IntegerField(blank=True, null=True, verbose_name="早退时长")
    absence_times = models.IntegerField(blank=True, null=True, verbose_name="缺勤次数")
    cal = models.ForeignKey('Cal', models.DO_NOTHING, verbose_name="工作日历")

    class Meta:
        managed = False
        db_table = 'employee_days_statistics'
        verbose_name = '每日出勤状况表'


hoilday_type_choice = (
    ("a", '调休假'),
    ("b", '事假'),
    ("c", '病假'),
    ("d", '婚假'),
    ("e", '产假'),
    ("f", '陪产假'),
    ("g", '哺乳假'),
    ("h", '节育假'),
    ("i", '工伤假'),
    ("j", '看护假'),
    ("k", '丧假'),
    ("l", '产检假')
)
hoilday_day_type_choice = (
    (1, '普通工作日请假'),
    (2, '周六工作日请假'),
    (3, '周日请假'),
    (4, '节假日请假')
)


class EmployeeHoildayStatistics(models.Model):
    bus = models.ForeignKey('EmployeeInformation', models.DO_NOTHING, verbose_name="员工名字")
    hoilday_type = models.CharField(max_length=255, choices=hoilday_type_choice, verbose_name="请假类型")
    hoilday_day_type = models.CharField(max_length=255, choices=hoilday_day_type_choice, verbose_name="请假日类型")
    hoilday_start_time = models.TimeField(blank=True, null=True, verbose_name="请假开始时间")
    hoilday_stop_time = models.TimeField(blank=True, null=True, verbose_name="请假结束时间")
    hoilday_last_time = models.FloatField(verbose_name="请假时长(天)")
    years = models.IntegerField(blank=True, null=True)
    months = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    weeks = models.IntegerField(blank=True, null=True)
    dates = models.DateField(blank=True, null=True, verbose_name="请假日期")
    serial = models.CharField(blank=True, null=True, max_length=255, verbose_name="云之家流水号")

    class Meta:
        managed = False
        db_table = 'employee_hoilday_statistics'
        verbose_name = '请假信息统计表'


go_out_type_choice = (
    (1, "公干"),
    (2, "出差"),

)


class EmployeeBustravelStatistics(models.Model):
    bus = models.ForeignKey('EmployeeInformation', models.DO_NOTHING, verbose_name="员工名字")
    bustravel_start_time = models.TimeField(blank=True, null=True, verbose_name="出差开始时间")
    bustravel_stop_time = models.TimeField(blank=True, null=True, verbose_name="出差结束时间")
    bustravel_last_time = models.FloatField(verbose_name="出差时长(天)")
    years = models.IntegerField(blank=True, null=True)
    months = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    weeks = models.IntegerField(blank=True, null=True)
    dates = models.DateField(blank=True, null=True, verbose_name="出差日期")
    serial = models.CharField(blank=True, null=True, max_length=255, verbose_name="云之家流水号")
    go_out_type = models.IntegerField(blank=True, null=True, verbose_name="出门类型", choices=go_out_type_choice)

    class Meta:
        managed = False
        db_table = 'employee_bustravel_statistics'
        verbose_name = '出差信息统计表'


att_chioce = (
    (1, "记录考勤"),
    (2, "不统计考勤"),
)
is_job_chioce = (
    (1, "在职"),
    (2, "已离职"),
)


class EmployeeInformation(models.Model):
    bus_id = models.IntegerField(primary_key=True, verbose_name="企业工号")
    namse = models.CharField(max_length=255, verbose_name="员工姓名")
    dept = models.CharField(max_length=255, verbose_name="部门")
    positi = models.CharField(max_length=255, verbose_name="岗位")
    openid = models.CharField(max_length=255)
    time1 = models.TimeField(blank=True, null=True, verbose_name="上班打卡时间")
    time2 = models.TimeField(blank=True, null=True, verbose_name="午休开始时间")
    time3 = models.TimeField(blank=True, null=True, verbose_name="午休结束时间")
    time4 = models.TimeField(blank=True, null=True, verbose_name="下班打卡时间")
    att_type = models.IntegerField(blank=True, null=True, verbose_name="出勤类型", choices=att_chioce)
    is_job = models.IntegerField(blank=True, null=True, verbose_name="在职状态", choices=is_job_chioce)
    entry_date = models.DateField(blank=True, null=True, verbose_name="入职日期")
    leave_date = models.DateField(blank=True, null=True, verbose_name="离职日期")

    def __str__(self):
        return self.namse

    class Meta:
        managed = True
        db_table = 'employee_information'
        verbose_name = '员工信息表'


class EmployeeMonthStatistics(models.Model):
    bus = models.ForeignKey(EmployeeInformation, models.DO_NOTHING, verbose_name="员工名称")
    years = models.IntegerField(blank=True, null=True, verbose_name="考勤年")
    months = models.CharField(max_length=255, verbose_name="考勤月")
    attendance_days = models.FloatField(blank=True, null=True, verbose_name="应出勤(天)")
    act_attendance_days = models.FloatField(blank=True, null=True, verbose_name="实际出勤(天)")
    sat_attendance_days = models.FloatField(blank=True, null=True, verbose_name="周六出勤(天)")
    sun_attendance_days = models.FloatField(blank=True, null=True, verbose_name="周日出勤(天)")
    holi_attendance_days = models.FloatField(blank=True, null=True, verbose_name="节假日出勤(天)")
    evection_days = models.FloatField(blank=True, null=True, verbose_name="出差(天)")
    usua_overtime = models.FloatField(blank=True, null=True, verbose_name="平常加班(时)")
    absence_time = models.FloatField(blank=True, null=True, verbose_name="缺勤时间")
    miss_chock_in_times = models.IntegerField(blank=True, null=True, verbose_name="上班缺卡次数")
    miss_chock_out_times = models.IntegerField(blank=True, null=True, verbose_name="下班缺卡次数")
    late_times = models.IntegerField(blank=True, null=True, verbose_name="迟到次数")
    late_length = models.FloatField(blank=True, null=True, verbose_name="迟到时长(分钟)")
    early_leave_times = models.IntegerField(blank=True, null=True, verbose_name="早退次数")
    early_leave_length = models.FloatField(blank=True, null=True, verbose_name="早退时长(分钟)")
    a_holi = models.FloatField(blank=True, null=True, verbose_name="调休假(天)")
    b_holi = models.FloatField(blank=True, null=True, verbose_name="事假(天)")
    c_holi = models.FloatField(blank=True, null=True, verbose_name="病假(天)")
    d_holi = models.FloatField(blank=True, null=True, verbose_name="婚假(天)")
    e_holi = models.FloatField(blank=True, null=True, verbose_name="产假(天)")
    f_holi = models.FloatField(blank=True, null=True, verbose_name="陪产假(天)")
    g_holi = models.FloatField(blank=True, null=True, verbose_name="哺乳假(天)")
    h_holi = models.FloatField(blank=True, null=True, verbose_name="节育假(天)")
    i_holi = models.FloatField(blank=True, null=True, verbose_name="工伤假(天)")
    j_holi = models.FloatField(blank=True, null=True, verbose_name="看护假(天)")
    k_holi = models.FloatField(blank=True, null=True, verbose_name="丧假(天)")
    l_holi = models.FloatField(blank=True, null=True, verbose_name="产检假(天)")
    act_holi_days = models.FloatField(blank=True, null=True, verbose_name="实际请假(天)")
    overtime_surplus = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_month_statistics'
        verbose_name = '月度信息汇总表'


over_choice = (
    ("1", "工作日加班"),
    ("2", "假日加班"),
    ("3", "节日加班"),
)


class EmployeeOvertimeStatistics(models.Model):
    bus = models.ForeignKey('EmployeeInformation', models.DO_NOTHING, verbose_name="员工名字")
    overtime_type = models.CharField(max_length=255, verbose_name="加班类型", choices=over_choice)
    dates = models.DateField(blank=True, null=True, verbose_name="加班日期")
    overtime_start_time = models.DateTimeField(verbose_name="加班开始时间")
    overtime_stop_time = models.DateTimeField(verbose_name="加班结束时间")
    overtime_last_time = models.FloatField(verbose_name="加班时长(小时)")
    years = models.IntegerField(blank=True, null=True)
    months = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    weeks = models.IntegerField(blank=True, null=True, verbose_name="周几")

    class Meta:
        managed = False
        db_table = 'employee_overtime_statistics'
        verbose_name = "员工加班信息汇总表"


class SaturdayHoli(models.Model):
    bus_id = models.IntegerField()
    lasttime = models.FloatField()
    date = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'saturday_holi'
