def more_than_one(amount:int, plural:str="s", zero="s") -> str:
	"""returns plural (default s) if amount above 1 or equal to 0"""
	return zero if amount == 0 else plural if amount > 1 else ""
	#return plural if amount > 1 or amount == 0 else ""