import urllib.parse

def url_format(url:str, path:str) -> str:
	if   path == 'encode':
		return urllib.parse.quote(url)
	elif path == 'decode':
		return urllib.parse.unquote(url)