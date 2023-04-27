from . import dictlace

__all__ = ['ordinal_suffix', 'to_ordinal', 'from_ordinal']

def ordinal_suffix(n:int) -> str:
	#0 if int(str(n)[-1]) > 3 else int(str(n)[-1])
	return 'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]

def to_ordinal(n:int) -> str:
	"""return an integer n (+ve or -ve) to ordinal version.
	>>> to_ordinal(1234)
	'one thousand two hundred and thirty-four'
	"""
	# lookups
	ones = ["zero",    "one",     "two",      "three",     "four",     "five",    "six",     "seven",     "eight",    "nine", 
			"ten",     "eleven",  "twelve",   "thirteen",  "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]

	tens = ["zero",    "ten",     "twenty",   "thirty",    "forty",    "fifty",   "sixty",   "seventy",   "eighty",   "ninety"]
	# negative case
	if n < 0: return f"minus {to_ordinal(abs(n))}"
	# 1000+
	if n >= 1000:
		num = (
			#(1.e+1000, "Googolplex"),# 10**10**100# big number big makes python not happy
			(10**103, "Centillion"),        (10**100, "Googol"),
			(10**63,  "Vigintillion"),      (10**60, "Novemdecillion"),
			(10**57,  "Octodecillion"),     (10**54, "Septendecillion"),
			(10**51,  "Sexdecillion"),      (10**48, "Quindecillion"),
			(10**45,  "Quattuordecillion"), (10**42, "Tredecillion"),
			(10**39,  "Duodecillion"),      (10**36, "Undecillion"),
			(10**33,  "Decillion"),         (10**30, "Nonillion"),
			(10**27,  "Octillion"),         (10**24, "Septillion"),
			(10**21,  "Sextillion"),        (10**18, "Quintillion"),
			(10**15,  "quadrillion"),       (10**12, "trillion"),
			(10**9,   "billion"),           (10**6,  "million"),
			(10**3,   "thousand"))
		for order, word in num:
			if n >= order:
				return f"{to_ordinal(n // order)} {word}{f' {to_ordinal(n % order)}' if n % order else ''}"
	# 100-999
	if n >= 100 and n <= 999:
		if n % 100:
			return f"{to_ordinal(n // 100)} hundred and {to_ordinal(n % 100)}"
		else:
			return f"{to_ordinal(n // 100)} hundred"
	# 0-99
	if n >= 0 and n <= 99:
		if n < 20:
			return ones[n]
		else:
			return f"{tens[n // 10]}{f'-{to_ordinal(n % 10)}' if n % 10 else ''}"

def from_ordinal(n:str) -> int:
	"""return an a ordinal version n (+ve or -ve) back to a integer.
	>>> to_ordinal('minus one thousand two hundred and thirty-four')
	-1234
	"""
	# lookups
	ones = {"minus":"-",
			"zero":0,          "one":1,            "two":2,                "three":3,            "four":4,           
			"five":5,          "six":6,            "seven":7,              "eight":8,            "nine":9, 
			"ten":10,          "eleven":11,        "twelve":12,            "thirteen":13,        "fourteen":14,
			"fifteen":15,      "sixteen":16,       "seventeen":17,         "eighteen":18,        "nineteen":19,

			"twenty":20,       "thirty":30,        "forty":40,             "fifty":50,           "sixty":60,         "seventy":70,    "eighty":80,    "ninety":90,

			"Centillion":"",   "Googol":"",        "Vigintillion":"",      "Novemdecillion":"",  "Octodecillion":"", "Septendecillion":"",
			"Sexdecillion":"", "Quindecillion":"", "Quattuordecillion":"", "Tredecillion":"",    "Duodecillion":"",  "Undecillion":"",
			"Decillion":"",    "Nonillion":"",     "Octillion":"",         "Septillion":"",      "Sextillion":"",    "Quintillion":"",
			"quadrillion":"",  "trillion":"",      "billion":"",           "million":"",         "thousand":"",      'hundred':''}
	#a = dictlace.dict_replace(n, {'-': ' ', ' and':' '}).split()
	#b = [str(ones[y])[:-1] if x < 1 else str(ones[y]) if '-' in i else str(ones[i]) for i in n.split() for x, y in enumerate(i.split('-'))]

	b = []
	for i in n.replace(' and').split():
		if '-' in i:
			#for x, y in enumerate(i.split('-')):
			#	b.append(str(ones[y])[:-1] if x < 1 else str(ones[y]))
			x, y = i.split('-')
			b.append(f"{str(ones[x])[:-1]}{ones[y]}")
		else:
			if str(ones[i]):
				b.append(str(ones[i]))
	return int(''.join(b))
