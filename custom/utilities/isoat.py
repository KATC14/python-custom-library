def is_float(num:str) -> (float|int|str):
	try:
		if num.isdigit():
			return int(num)
		return float(num)
	except Exception:
		return num