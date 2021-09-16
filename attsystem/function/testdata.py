import time

check_times = ["2021-09-10 13:02:01", "2021-09-10 13:03:01"]
# for i in check_times:
#     for j in check_times:
#         time1 = time.mktime(time.strptime(str(i), "%Y-%m-%d %H:%M:%S"))
#         time2 = time.mktime(time.strptime(str(j), "%Y-%m-%d %H:%M:%S"))
#         print(time1)
#         print(time2)
#         print(abs(time1 - time2))
#         if abs(time1 - time2) < 120:
#             check_times.remove(i)
# print(check_times)

for index1 in range(len(check_times)):
    for index2 in range(len(check_times)-1):
        print(check_times[index2])
