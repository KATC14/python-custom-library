import datetime
import zoneinfo

def cut_convert(TimeStamp:datetime.datetime, TimeZone:str=None) -> datetime.datetime:
	"""converts time from given datetime object to Eastern Standard Time if TimeZone is None

	TimeZone should always be string in format of 'TZ database name' from
	https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
	
	or one returned from
	>>> import zoneinfo 
	>>> zoneinfo.available_timezones()
	{...}

	Examples:
	>>> ts = datetime.datetime(2001, 9, 11, 12, 14)
	>>> cut_convert(ts)
	datetime.datetime(2001, 9, 11, 8, 14)
	>>> cut_convert(ts, 'America/Anchorage')
	datetime.datetime(2001, 9, 11, 16, 14)
	>>> cut_convert(ts, 'Asia/Tokyo')
	datetime.datetime(2001, 9, 10, 23, 14)
	"""
	#if TimeStamp[-1:] == 'Z': ts = TimeStamp[:-1]
	#else:                     ts = TimeStamp
	#cut = datetime.datetime.fromisoformat(ts)#FWISO
	#print(FWISO)
	#cut = datetime.datetime.strptime(str(FWISO), '%Y-%m-%d %H:%M:%S')
	cut = TimeStamp

	#https://en.wikipedia.org/wiki/List_of_tz_database_time_zones #zoneinfo.available_timezones()
	if TimeZone is not None:
		tz = zoneinfo.ZoneInfo(TimeZone)
	else:
		tz = datetime.timezone.utc
	cut = cut.replace(tzinfo=tz)
	new_zone = cut.astimezone()
	return datetime.datetime.strptime(new_zone.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")