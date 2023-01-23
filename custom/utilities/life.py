import base64

def base42(path:str, data:str) -> str:
	if   path == 'encode':
		return base64.b64encode(data.encode("utf8")).decode()
	elif path == 'decode':
		return base64.b64decode(data).decode()
	else:
		return 'you need "encode" or "decode"'