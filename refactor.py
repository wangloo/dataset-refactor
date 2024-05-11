import csv
from datetime import datetime, timedelta
import select


data_all = []
time_format = '%Y-%m-%d %H:%M:%S'

# 将所有文件读取到data_all
for prefix in range(1,1000):
	data_user = []
	filename = "taxi_log_2008_by_id/"+str(prefix)+".txt"

	with open(filename, newline='', mode='r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			# data_user.append(row[1:]) # 过滤掉user列
			data_user.append(row) 
	if data_user != []:
		data_all.append(data_user)

print(data_all[0][0:2])

# 计算时间线端点
time_begin, time_end = '2018-02-08 16:33:25', '1998-02-08 16:33:25'
time_begin_obj = datetime.strptime(time_begin, '%Y-%m-%d %H:%M:%S')
time_end_obj = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
for datau in data_all:
	for item in datau:
		time_cur_obj = datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S')
		if time_cur_obj < time_begin_obj:
			time_begin_obj = time_cur_obj
			time_begin = time_cur_obj.strftime(time_format)
		elif time_cur_obj > time_end_obj:
			time_end_obj = time_cur_obj
			time_end = time_cur_obj.strftime(time_format)
print(time_begin, time_end)

# 创建文件：一小时做一次划分
time_format_filename = '%Y-%m-%d_%H:%M:%S'
time_now_obj = time_begin_obj
while time_now_obj < time_end_obj:
	time_next_obj = time_now_obj + timedelta(hours=1) # gap=1 hour
	filename = time_now_obj.strftime(time_format_filename) + ".csv"

	with open(filename, mode='w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for ui,datau in enumerate(data_all):
			select_item = [] # 选择时间最后的一条，如果没有就从其他时间段选一条
			nearest_index = 10000000000 # out out index
			min_gap = timedelta(days=30)
			for i,item in enumerate(datau):
				time_item_obj = datetime.strptime(item[1], time_format)
				if time_item_obj >= time_next_obj:
					if abs(time_now_obj - time_item_obj) < min_gap:
						min_gap = abs(time_now_obj - time_item_obj)
						nearest_index = i
					break
				if time_item_obj < time_now_obj:
					if abs(time_now_obj - time_item_obj) < min_gap:
						min_gap = abs(time_now_obj - time_item_obj)
						nearest_index = i
					continue
				select_item = item
			if select_item == []:
				if nearest_index == 10000000000:
					print('err! when writing {} , user:{}'.format(filename, ui))
				select_item = datau[nearest_index]
			writer.writerow(select_item)
				
	time_now_obj = time_next_obj
	
print("Done")
			
	