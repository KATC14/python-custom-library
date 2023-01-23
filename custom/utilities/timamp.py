import datetime

def time_stamp(timefmt:str='%I:%M:%S %p') -> str:
	"""returns current time. default 12 hour format

	can have optional timefmt described in
	https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
	"""
	return datetime.datetime.now().strftime(timefmt)