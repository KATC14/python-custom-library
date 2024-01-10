import csv


def csv_pprint(fieldnames, data:dict):
	"""saves to cvs file with white sapces
	>>> fieldnames = 'id|user_name|display_name'
	>>> a = {"a":{"id":1111, "user_name":"name", "display_name":"Name"},
	... "b":{"id":2222, "user_name":"name2", "display_name":"nAme2"}}
	>>> csv_pprint(fieldnames, a)
	['id  |user_name|display_name', '1111|name     |Name', '2222|name2    |nAme2']
	"""
	values = ['|'.join([str(i) for i in list(data[i].values())]) for i in data]
	values.insert(0, fieldnames)
	csv_data = list(csv.reader(values, delimiter='|'))

	col_widths = [max(len(row[i]) for row in csv_data) for i in range(len(csv_data[0]))]

	return ['|'.join(val.ljust(width) for val, width in zip(row, col_widths)).strip() for row in csv_data]