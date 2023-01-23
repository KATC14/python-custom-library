def dict_replace(inputt:str, dictt:dict) -> str:
	"""replace multiple items in a string
	
	>>> dict_replace('this is a_test', {' ': '-','_': '.'})
	'this-is-a.test'
	"""
	#print(inputt, dictt)
	#for key, value in dictt.items():
	#    inputt = f'{value}'.join(inputt.split(key))
	#return inputt
	for key, value in dictt.items():
		inputt = str(inputt).replace(key, value)
	return inputt