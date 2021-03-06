# Generated by Django 3.2.7 on 2021-09-26 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttsystemTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'attsystem_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.DateField(blank=True, null=True, verbose_name='??????')),
                ('years', models.IntegerField(blank=True, null=True, verbose_name='???')),
                ('months', models.IntegerField(blank=True, null=True, verbose_name='???')),
                ('days', models.IntegerField(blank=True, null=True, verbose_name='???')),
                ('weeks', models.IntegerField(blank=True, null=True, verbose_name='??????')),
                ('kinds', models.IntegerField(blank=True, choices=[(1, '???????????????'), (2, '???????????????'), (3, '??????'), (4, '?????????')], null=True, verbose_name='??????')),
            ],
            options={
                'verbose_name': '????????????',
                'db_table': 'cal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CheckInDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_date', models.DateField(verbose_name='????????????')),
                ('checkin_time', models.TimeField(verbose_name='????????????')),
                ('weeks', models.IntegerField(verbose_name='??????')),
                ('years', models.IntegerField(blank=True, null=True)),
                ('months', models.IntegerField(blank=True, null=True)),
                ('days', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '???????????????',
                'db_table': 'check_in_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeBustravelStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bustravel_start_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('bustravel_stop_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('bustravel_last_time', models.FloatField(verbose_name='????????????(???)')),
                ('years', models.IntegerField(blank=True, null=True)),
                ('months', models.IntegerField(blank=True, null=True)),
                ('days', models.IntegerField(blank=True, null=True)),
                ('weeks', models.IntegerField(blank=True, null=True)),
                ('dates', models.DateField(blank=True, null=True, verbose_name='????????????')),
                ('serial', models.CharField(blank=True, max_length=255, null=True, verbose_name='??????????????????')),
                ('go_out_type', models.IntegerField(blank=True, choices=[(1, '??????'), (2, '??????')], null=True, verbose_name='????????????')),
            ],
            options={
                'verbose_name': '?????????????????????',
                'db_table': 'employee_bustravel_statistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeDaysStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('out_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('judge_in_time', models.TimeField(blank=True, null=True, verbose_name='????????????????????????')),
                ('judge_out_time', models.TimeField(blank=True, null=True, verbose_name='????????????????????????')),
                ('act_times', models.FloatField(blank=True, null=True, verbose_name='????????????(???)')),
                ('holi_in_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('holi_out_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('hoil_last_time', models.FloatField(blank=True, null=True, verbose_name='??????????????????(???)')),
                ('over_in_time', models.DateTimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('over_out_time', models.DateTimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('over_last_time', models.FloatField(blank=True, null=True, verbose_name='??????????????????(??????)')),
                ('bustravel_start_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('bustravel_stop_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('bustravel_last_time', models.FloatField(blank=True, null=True, verbose_name='??????????????????(???)')),
                ('check_in_result', models.IntegerField(blank=True, choices=[(1, '??????'), (2, '??????'), (3, '??????')], null=True, verbose_name='??????????????????')),
                ('check_out_result', models.IntegerField(blank=True, choices=[(1, '??????'), (2, '??????'), (3, '??????')], null=True, verbose_name='??????????????????')),
                ('late_time', models.IntegerField(blank=True, null=True, verbose_name='????????????')),
                ('leaveearly_time', models.IntegerField(blank=True, null=True, verbose_name='????????????')),
                ('absence_times', models.IntegerField(blank=True, null=True, verbose_name='????????????')),
            ],
            options={
                'verbose_name': '?????????????????????',
                'db_table': 'employee_days_statistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeHoildayStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoilday_type', models.CharField(choices=[('a', '?????????'), ('b', '??????'), ('c', '??????'), ('d', '??????'), ('e', '??????'), ('f', '?????????'), ('g', '?????????'), ('h', '?????????'), ('i', '?????????'), ('j', '?????????'), ('k', '??????'), ('l', '?????????')], max_length=255, verbose_name='????????????')),
                ('hoilday_day_type', models.CharField(choices=[(1, '?????????????????????'), (2, '?????????????????????'), (3, '????????????'), (4, '???????????????')], max_length=255, verbose_name='???????????????')),
                ('hoilday_start_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('hoilday_stop_time', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('hoilday_last_time', models.FloatField(verbose_name='????????????(???)')),
                ('years', models.IntegerField(blank=True, null=True)),
                ('months', models.IntegerField(blank=True, null=True)),
                ('days', models.IntegerField(blank=True, null=True)),
                ('weeks', models.IntegerField(blank=True, null=True)),
                ('dates', models.DateField(blank=True, null=True, verbose_name='????????????')),
                ('serial', models.CharField(blank=True, max_length=255, null=True, verbose_name='??????????????????')),
            ],
            options={
                'verbose_name': '?????????????????????',
                'db_table': 'employee_hoilday_statistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeMonthStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years', models.IntegerField(blank=True, null=True, verbose_name='?????????')),
                ('months', models.CharField(max_length=255, verbose_name='?????????')),
                ('attendance_days', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('act_attendance_days', models.FloatField(blank=True, null=True, verbose_name='????????????(???)')),
                ('sat_attendance_days', models.FloatField(blank=True, null=True, verbose_name='????????????(???)')),
                ('sun_attendance_days', models.FloatField(blank=True, null=True, verbose_name='????????????(???)')),
                ('holi_attendance_days', models.FloatField(blank=True, null=True, verbose_name='???????????????(???)')),
                ('evection_days', models.FloatField(blank=True, null=True, verbose_name='??????(???)')),
                ('usua_overtime', models.FloatField(blank=True, null=True, verbose_name='????????????(???)')),
                ('absence_time', models.FloatField(blank=True, null=True, verbose_name='????????????')),
                ('miss_chock_in_times', models.IntegerField(blank=True, null=True, verbose_name='??????????????????')),
                ('miss_chock_out_times', models.IntegerField(blank=True, null=True, verbose_name='??????????????????')),
                ('late_times', models.IntegerField(blank=True, null=True, verbose_name='????????????')),
                ('late_length', models.FloatField(blank=True, null=True, verbose_name='????????????(??????)')),
                ('early_leave_times', models.IntegerField(blank=True, null=True, verbose_name='????????????')),
                ('early_leave_length', models.FloatField(blank=True, null=True, verbose_name='????????????(??????)')),
                ('a_holi', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('b_holi', models.FloatField(blank=True, null=True, verbose_name='??????(???)')),
                ('c_holi', models.FloatField(blank=True, null=True, verbose_name='??????(???)')),
                ('d_holi', models.FloatField(blank=True, null=True, verbose_name='??????(???)')),
                ('e_holi', models.FloatField(blank=True, null=True, verbose_name='??????(???)')),
                ('f_holi', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('g_holi', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('h_holi', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('i_holi', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('j_holi', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('k_holi', models.FloatField(blank=True, null=True, verbose_name='??????(???)')),
                ('l_holi', models.FloatField(blank=True, null=True, verbose_name='?????????(???)')),
                ('act_holi_days', models.FloatField(blank=True, null=True, verbose_name='????????????(???)')),
                ('overtime_surplus', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '?????????????????????',
                'db_table': 'employee_month_statistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeOvertimeStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overtime_type', models.CharField(choices=[('1', '???????????????'), ('2', '????????????'), ('3', '????????????')], max_length=255, verbose_name='????????????')),
                ('dates', models.DateField(blank=True, null=True, verbose_name='????????????')),
                ('overtime_start_time', models.DateTimeField(verbose_name='??????????????????')),
                ('overtime_stop_time', models.DateTimeField(verbose_name='??????????????????')),
                ('overtime_last_time', models.FloatField(verbose_name='????????????(??????)')),
                ('years', models.IntegerField(blank=True, null=True)),
                ('months', models.IntegerField(blank=True, null=True)),
                ('days', models.IntegerField(blank=True, null=True)),
                ('weeks', models.IntegerField(blank=True, null=True, verbose_name='??????')),
            ],
            options={
                'verbose_name': '???????????????????????????',
                'db_table': 'employee_overtime_statistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SaturdayHoli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_id', models.IntegerField()),
                ('lasttime', models.FloatField()),
                ('date', models.IntegerField()),
            ],
            options={
                'db_table': 'saturday_holi',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeInformation',
            fields=[
                ('bus_id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='????????????')),
                ('namse', models.CharField(max_length=255, verbose_name='????????????')),
                ('dept', models.CharField(max_length=255, verbose_name='??????')),
                ('positi', models.CharField(max_length=255, verbose_name='??????')),
                ('openid', models.CharField(max_length=255)),
                ('time1', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('time2', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('time3', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('time4', models.TimeField(blank=True, null=True, verbose_name='??????????????????')),
                ('att_type', models.IntegerField(blank=True, choices=[(1, '????????????'), (2, '???????????????')], null=True, verbose_name='????????????')),
                ('is_job', models.IntegerField(blank=True, choices=[(1, '??????'), (2, '?????????')], null=True, verbose_name='????????????')),
                ('entry_date', models.DateField(blank=True, null=True, verbose_name='????????????')),
                ('leave_date', models.DateField(blank=True, null=True, verbose_name='????????????')),
                ('is_office', models.IntegerField(blank=True, choices=[(1, '????????????'), (2, '????????????')], null=True, verbose_name='????????????')),
            ],
            options={
                'verbose_name': '???????????????',
                'db_table': 'employee_information',
                'managed': True,
            },
        ),
    ]
