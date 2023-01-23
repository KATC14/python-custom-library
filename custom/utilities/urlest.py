import urllib.request

def url_request(url:str, headers:dict={}, data=None, method:str=None, context=None):# -> http.client.HTTPResponse
	"""Open the given url, which must be a string

	*data* must be an object specifying additional data to be sent to
	the server, or None if no such data is needed.

	method should be a string that indicates the HTTP request method that will be used (e.g. 'HEAD').
	If provided, its value is stored in the method attribute and is used by get_method().
	The default is 'GET' if data is None or 'POST' otherwise unless method is not None.
	"""
	try:
		request = urllib.request.Request(url, headers=headers, data=data, method=method)
		response = urllib.request.urlopen(request, context=context)
		return response
	except Exception as error:
		return error