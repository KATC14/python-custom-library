def is_int(value:int|str) -> (int|str):
	"""returns value as a integer if value is a digit else value"""
	if not isinstance(value, bool) and isinstance(value, str) and value.isdigit():
		return int(value) 
	else:
		return value
	#try: return int(Value)
	#except Exception: return Value