import time

check_times1 = ["2021-09-10 07:56:01", "2021-09-10 18:05:01", "2021-09-10 18:05:03"]
# for i in check_times:
#     for j in check_times:
#         time1 = time.mktime(time.strptime(str(i), "%Y-%m-%d %H:%M:%S"))
#         time2 = time.mktime(time.strptime(str(j), "%Y-%m-%d %H:%M:%S"))
#         print(i)
#         print(j)
#         print(abs(time1 - time2))
#         if abs(time1 - time2) < 300:
#             check_times.remove(i)
# print(check_times)
cut_list = []

for data1 in check_times1:
    for data2 in check_times1:
        time1 = time.mktime(time.strptime(str(data1), "%Y-%m-%d %H:%M:%S"))
        time2 = time.mktime(time.strptime(str(data2), "%Y-%m-%d %H:%M:%S"))
        noon_time = time.mktime(time.strptime(data1[:10] + " 13:00:00", "%Y-%m-%d %H:%M:%S"))
        if abs(time1 - time2) < 300 and time1 != time2:
            if time1 < noon_time:
                if time1 > time2:
                    if data1 not in cut_list:
                        cut_list.append(data1)
                if time1 < time2:
                    if data1 not in cut_list:
                        cut_list.append(data2)
            else:
                if time1 > time2:
                    if data2 not in cut_list:
                        cut_list.append(data2)
                else:
                    if data2 not in cut_list:
                        cut_list.append(data1)
# list去重
list_data = list(set(cut_list))
print(cut_list)
print(list(set(cut_list)))
for data in list_data:
    check_times1.remove(data)
print(check_times1)
