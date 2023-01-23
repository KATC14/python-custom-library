import datetime

from . import ordinal

def time_amount(TimeStamp:datetime.datetime, fmt:str=None, ordinal_suffix=True) -> str:
	"""can have optional fmt described in
	https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
	
	defaults to %A %B %d(with ordinal suffix) %Y %I:%M:%S %p\n
	set ordinal_suffix to false to remove ordinal suffix

	returns:
	- Weekday as locale's full name.
	- Month   as locale's full name.
	- Day of the month as a zero-padded decimal number.
	- Year with century as a decimal number.
	- %I 12-hour as a zero-padded decimal number.
	- %M Minute as a zero-padded decimal number.
	- %S Second as a zero-padded decimal number.
	- %P Locale's equivalent of either AM or PM.

	>>> ts = datetime.datetime(2022, 9, 2, 17, 44, 17, 985008)
	>>> time_amount(ts)
	'Friday September 02nd 2022 05:44:17 PM'
	"""
	ordi = ''
	if ordinal_suffix: ordi = ordinal.ordinal_suffix(int(TimeStamp.strftime("%d")))
	if not fmt:        fmt     = f"%A %B %d{ordi} %Y %I:%M:%S %p"

	return TimeStamp.strftime(fmt.replace("ord", ordi))