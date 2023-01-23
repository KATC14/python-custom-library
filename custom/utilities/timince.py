import datetime

from . import moane

def time_since(start_time:datetime.datetime, end_time:datetime.datetime=None, anal:bool=False):
	"""takes datetime object

	can have optional end_time defaults to current date and time if end_time none

	can have optional anal(analysis) changes return to total amount in all format

	returns:
		amount of time since given datetime object to end_time

		in format 'year(s), month(s), week(s), day(s), hour(s) minuet(s), second(s)' if amount is above 0, plural if amount above 1 or equal to 0

	>>> dts = datetime.datetime.strptime('2001-09-11 08:14:00', '%Y-%m-%d %H:%M:%S')
	>>> dte = datetime.datetime.strptime('2022-09-02 03:08:01', '%Y-%m-%d %H:%M:%S')
	>>> times_since(dts, dte)
	'20 years, 11 months, 3 weeks, 5 days, 18 hours, 54 minutes, 1 second'
	"""
	if not end_time: end_time = datetime.datetime.now()
	duration = end_time - start_time

	second = duration.total_seconds()# Total number of seconds between dates
	#minutes, seconds = divmod(second, 60)
	#hours, minutes = divmod(minutes, 60)
	#days, hours = divmod(hours, 24)
	#weeks = divmod(divmod(days, 7)[0], 4.345)[1]

	minute = second / 60
	hour   = minute / 60
	day    = hour   / 24
	week   = day    / 7
	month  = week   / 4.345
	year   = month  / 12#second // 31536000

	# isly = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
	# fy = int(ts.strftime("%Y"))
	# py = int(utcest.strftime("%Y"))
	# print('Ld', calendar.leapdays(py, fy))
	# day += calendar.leapdays(py, fy)

	# w = int((year%365)/7)
	# d = int((year%365)%7)
	# print(w, d)

	if not anal:
		second -= int(minute) * 60
		minute -= int(hour)   * 60
		hour   -= int(day)    * 24
		week   -= int(month)  * 4.345 #= int((year%365)/7) #= divmod(divmod(days, 7)[0], 4.345)[1]
		month  -= int(year)   * 12

		day     = (week - int(week)) * 7

	periods = (
		(int(year),   "year"),
		(int(month),  "month") if not anal else (0, "month"),
		(int(week),   "week")  if not anal else (0, "week"),
		(int(day),    "day"),
		(int(hour),   "hour"),
		(int(minute), "minute"),
		(int(second), "second")
	)

	#', '.join([f"{int(amount)} {timeformat}{more_than_one(amount)}{total}" for amount, timeformat in periods if int(amount) > 0])
	datelist = []
	for amount, timeformat in periods:
		if amount > 0:
			datelist.append(f"{amount} {timeformat}{moane.more_than_one(amount)}{' total' if anal else ''}")
	#if int(year)   > 0:     datelist.append(f"{int(year)} year{more_than_one(year)}{total}")
	#if int(month)  > 0:   datelist.append(f"{int(month)} month{more_than_one(month)}{total}")
	#if int(week)   > 0:     datelist.append(f"{int(week)} week{more_than_one(week)}{total}")
	#if int(day)    > 0:       datelist.append(f"{int(day)} day{more_than_one(day)}{total}")
	#if int(hour)   > 0:     datelist.append(f"{int(hour)} hour{more_than_one(hour)}{total}")
	#if int(minute) > 0: datelist.append(f"{int(minute)} minute{more_than_one(minute)}{total}")
	#if int(second) > 0: datelist.append(f"{int(second)} second{more_than_one(second)}{total}")
	#print(datelist)

	return ', '.join(datelist)