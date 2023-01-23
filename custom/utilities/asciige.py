from custom.ascii_text import ascii_text

def ascii_change(numbers:str) -> str:
	"""changes text into ascii version
	>>> import datetime
	>>> print(ascii_change(datetime.datetime(2022, 9, 6, 6, 40, 49, 299197).strftime('%I:%M:%S %p')))
	\"\"\"
	  .----.     ,--.              .---.    .----.            .---.    .----.
	 /  ..  \   /  .'      .-.    / .  |   /  ..  \   .-.    / .  |   /  ,.  \                 __  __
	.  /  \  . .  / -.     `-'   / /|  |  .  /  \  .  `-'   / /|  |  |  |  \  |         /\    |  \/  |
	|  |  '  | | .-.  '         / / |  |_ |  |  '  |       / / |  |_  '  `-'  '        /  \   | \  / |
	'  \  /  ' ' \  |  |   .-. /  '-'    |'  \  /  '  .-. /  '-'    |  `- /  '        / /\ \  | |\/| |
	 \  `'  /  \  `'  /    `-' `----|  |-' \  `'  /   `-' `----|  |-'   ,'  /        / ____ \ | |  | |
	  `---''    `----'              `--'    `---''             `--'    `---'        /_/    \_\|_|  |_|\"\"\"
	"""
	ascii_num = ascii_text()

	clock = ''
	numb  = ''.join([f"{ascii_num[i]}#\n" for i in numbers])
	b = numb[:-2].split('#\n')

	for i in zip(*[i.split('\n') for i in b]):
		if [x for x in i if x]:
			for x in i:
				clock += x.replace('@', '')#.rjust(1)
			clock += "\n"# '{:>30}'.format("\n")
	return clock[:-1]