def genaric_header(args:dict[str, str]) -> dict:
	"""
	>>> genaric_header({"ct":"a/j"})
	{"Content-Type":"application/json"}
	keys\n
		- ct       = Content-Type
		- ua       = User-Agent
		- acc      = Accept
	values\n
		- a/j      = application/json
		- a/urlenc = application/x-www-form-urlencoded
		- m5       = Mozilla/5.0
		- m5l      = Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0
	"""
	Headers = {}
	for k, v in args.items():
		if 'ct'   in k: key = 'Content-Type'
		if 'ua'   in k: key = 'User-Agent'
		if 'acc'  in k: key = 'Accept'

		if 'a/j'      in v: value = "application/json"
		if 'a/urlenc' in v: value = "application/x-www-form-urlencoded"
		if 'm5'       in v: value = "Mozilla/5.0"
		if 'longm5'   in v: value = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"

		Headers[key] = value
	return Headers