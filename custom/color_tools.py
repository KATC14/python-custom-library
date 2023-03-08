"""tools related to color converting
- can convert hsl, cmyk, hsv, hex, to rgb
- can convert rgb to hsl, cmyk, hsv, hex
- can invert given hex color
- can return random hex color
"""

import re#, os, tkinter
import random
import colorsys

from custom import utilities

reghex   = re.compile('#[0-9a-fA-f]*')
regcolor = re.compile('.*\((\d+\.\d+|\d+)%?,? ?(\d+\.\d+|\d+)%?,? ?(\d+\.\d+|\d+)%?(?:,? ?(\d+\.\d+|\d+)%?)?\)')

def colorfix(guess:str|tuple) -> tuple:
	"""turns: given color in tuple or str"(float|int, float|int, float|int, [float|int])" to tuple(float|int, float|int, float|int, [float|int])"""
	if '#'    in f'{guess}':
		return hex2rgb(reghex.findall(f'{guess}')[0])
	else:
		return tuple(utilities.is_float(i) for i in regcolor.findall(f'{guess}')[0] if i)

def invert(color:str|tuple) -> tuple:
	"""inverts given hex color"""
	r, g, b = colorfix(color)
	r, g, b = r - 255, g - 255, b - 255
	return rgb2hex((abs(r), abs(g), abs(b)))

def calccolorbg(color:str) -> str:
	"""Converts HEX to YIQ to judge what color background the color would look best on"""

	color = color[1:]
	if len(color) < 6:color = color[0] + color[0] + color[1] + color[1] + color[2] + color[2]

	r = int(color[0:2], 16)
	g = int(color[2:4], 16)
	b = int(color[4:8], 16)
	yiq = (r * 299 + g * 587 + b * 114) / 1000
	return 'dark' if yiq >= 128 else 'light'

def calccolorreplace(color:str, background:str) -> str:
	# Modified from http://www.sitepoint.com/javascript-generate-lighter-darker-color/
	# Modified further to use HSL as an intermediate format, to avoid hue-shifting
	# toward primaries when darkening and toward secondaries when lightening
	light = background == 'light'
	factor = 0.1 if light else -0.1

	color = color[1:]
	if len(color) < 6:
		color = color[0] + color[0] + color[1] + color[1] + color[2] + color[2]

	r = int(color[0:2], 16) / 255
	g = int(color[2:4], 16) / 255
	b = int(color[4:8], 16) / 255

	# Convert RGB to HSL, not ideal but it's faster than HCL or full YIQ conversion
	# based on http://axonflux.com/handy-rgb-to-hsl-and-rgb-to-hsv-color-model-c
	maxx = max(r, g, b)
	minn = min(r, g, b)
	l = min(max(0, (maxx + minn) / 2), 1)
	d = min(max(0, maxx - minn), 1)

	if d == 0:
		rgb = [d, d, l] # achromatic

	if maxx == r: h = min(max(0, (g - b) / d + (6 if g < b else 0)), 6)
	if maxx == g: h = min(max(0, (b - r) / d + 2), 6)
	if maxx == b: h = min(max(0, (r - g) / d + 4), 6)
	h /= 6

	s = d / (2 * (1 - l)) if l > 0.5 else d / (2 * l)
	s = min(max(0, s), 1)

	hsl =  [h, s, l]

	l = 1 - (1 - factor) * (1 - hsl[2]) if light else (1 + factor) * hsl[2]
	l = min(max(0, l), 1)


	if s == 0:
		rgb = round(min(max(0, 255 * l), 255)) # achromatic
		rgb = [rgb, rgb, rgb]

	q = l * (1 + s) if l < 0.5 else l + s - l * s
	p = 2 * l - q
	rgb =  [
		round(min(max(0, 255 * asdads(p, q, h + 1 / 3)), 255)),
		round(min(max(0, 255 * asdads(p, q, h)), 255)),
		round(min(max(0, 255 * asdads(p, q, h - 1 / 3)), 255)),
	]
	r = hex(rgb[0])[2:]
	g = hex(rgb[1])[2:]
	b = hex(rgb[2])[2:]

	return f'#{r}{g}{b}'

def asdads(pp:int, qq:int, t:int) -> int:
	if t < 0: t += 1
	if t > 1: t -= 1
	if t < 1 / 6:
		return pp + (qq - pp) * 6 * t
	elif t < 1 / 2:
		return qq
	elif t < 2 / 3:
		return pp + (qq - pp) * (2 / 3 - t) * 6
	else:
		return pp

def ReadableColors(color:str) -> str:
	"""returns color with a higher contrast"""
	for i in range(7):
		bgColor = calccolorbg(color)
		if bgColor == 'dark' : break
		color = calccolorreplace(color, bgColor)
		#if i == 3:break
	return color

def TCC(rgb:str|tuple) -> str:
	"""text color correction\n
	return black or white based on how dark or light given color is"""
	r, g, b = colorfix(hex2rgb(rgb) if '#' in rgb else rgb)
	o = round(((int(r) * 299) + (int(g) * 587) + (int(b) * 114)) / 1000)
	return 'black' if o > 125 else 'white'


def rgb2hsl(rgb:str) -> str:
	r, g, b = colorfix(rgb)
	r, g, b = r / 255, g / 255, b / 255

	rgbmax = max(r, g, b)
	rgbmin = min(r, g, b)

	l = (rgbmax + rgbmin) / 2#round(, 2)

	if rgbmax == rgbmin:
		s = 0
	else:
		if l <= 0.5: s = (rgbmax-rgbmin) / (rgbmax+rgbmin)
		if l > 0.5:  s = (rgbmax-rgbmin) / (2.0-rgbmax-rgbmin)

	if s != 0:
		if r == rgbmax: h = (g-b) / (rgbmax-rgbmin)
		if g == rgbmax: h = 2.0 + (b-r) / (rgbmax-rgbmin)
		if b == rgbmax: h = 4.0 + (r-g) / (rgbmax-rgbmin)
		if '-' in str(h):
			h += 360
	else:
		h = 0
	return round(h*60), round(s*100), round(l*100)

def hsl2rgb(hsl:str|tuple) -> tuple:#, hwb=False
	h, s, l = colorfix(hsl)
	r = hueToRgb(h, s, l/100, 0)
	g = hueToRgb(h, s, l/100, 8)
	b = hueToRgb(h, s, l/100, 4)
	return (r, g, b)

def hueToRgb(h:int, s:int, l:int, n:int) -> int:
	k = (n + h / 30) % 12
	color = l - s * min(l, 1 - l) / 100 * max(min(k - 3, 9 - k, 1), -1)
	return int(255 * color)

def hwb2hsv(hwb:str|tuple) -> tuple:
	h, w, b = colorfix(hwb)
	s = 0 if b == 100 else 100 - w / (100 - b) * 100
	v = 100 - b
	return (h, s, v)

def hsv2hwb(hsv:str|tuple) -> tuple:
	h, s, v = colorfix(hsv)
	w = round((100 - s) * v / 100)
	b = 100 - v
	return (h, w, b)

def rgb2cmyk(rgb:str|tuple) -> tuple:
	r, g, b = colorfix(rgb)
	if (r, g, b) == (0, 0, 0):
		return (0, 0, 0, 100)# black

	# rgb [0,255] -> cmy [0,1]
	c, m, y= 1 - r / 255, 1 - g / 255, 1 - b / 255

	# extract out k [0, 1]
	min_cmy = min(c, m, y)
	c = (c - min_cmy) / (1 - min_cmy)
	m = (m - min_cmy) / (1 - min_cmy)
	y = (y - min_cmy) / (1 - min_cmy)
	k = min_cmy

	# rescale to the range [0,CMYK_SCALE]
	return (round(c * 100), round(m * 100), round(y * 100), round(k * 100))

def cmyk2rgb(cmyk:str|tuple) -> tuple:
	c, m, y, k = colorfix(cmyk)
	r = 255 * (1.0 - c / float(100)) * (1.0 - k / float(100))
	g = 255 * (1.0 - m / float(100)) * (1.0 - k / float(100))
	b = 255 * (1.0 - y / float(100)) * (1.0 - k / float(100))
	return (round(r), round(g), round(b))

#def rgb2yiq(rgb):
#	r, g, b = colorfix(rgb)
#	return colorsys.rgb_to_yiq(r, g, b)
#def yiq2rgb(yiq):
#	y, i, q = colorfix(yiq)
#	r = y + (0.27*q + 0.41*i) / (0.74*0.41 + 0.27*0.48)
#	b = y + (0.74*q - 0.48*i) / (0.74*0.41 + 0.27*0.48)
#	g = y - (0.30*(r-y) + 0.11*(b-y)) / 0.59
#	return (int(r), int(g), round(b))

#def rgb2hls(rgb):
#	r, g, b = colorfix(rgb)
#	return colorsys.rgb_to_hls(r, g, b)
#def hls2rgb(hls):
#	h, l, s = colorfix(hls)
#	return colorsys.hls_to_rgb(h, l, s)

def rgb2hsv(rgb:str|tuple) -> tuple:
	r, g, b = colorfix(rgb)
	r /= 255
	g /= 255
	b /= 255
	v = max(r, g, b)
	diff = v - min(r, g, b)
	if (diff == 0):h = s = 0
	else:
		s = diff / v
		rr = (v - r) / 6 / diff + 1 / 2
		gg = (v - g) / 6 / diff + 1 / 2
		bb = (v - b) / 6 / diff + 1 / 2

		if r == v:h = bb - gg
		elif g == v:h = (1 / 3) + rr - bb
		elif b == v:h = (2 / 3) + gg - rr
		if h < 0:h += 1
		elif h > 1:h -= 1
	return (round(h * 360), int(round(s * 100 * 100) / 100), int(round(v * 100 * 100) / 100))

def hsv2rgb(hsv:str|tuple) -> tuple:
	h, s, v = colorfix(hsv)
	#r, g, b = colorsys.hsv_to_rgb(h/360, s/100, v/100)
	#return (round(r * 255), round(g * 255), round(b * 255))
	r, g, b = [round(i * 255) for i in colorsys.hsv_to_rgb(h/360,s/100,v/100)]
	return (r, g, b)

def randcolor() -> str:
	"""returns random color in hex"""
	r = lambda: random.randint(0,255)
	return rgb2hex((r(), r(), r()))

def rgb2hex(rgb:str|tuple) -> str:
	hextable = [
		'00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', 
		'10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', 
		'20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', 
		'30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', 
		'40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', 
		'50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', 
		'60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', 
		'70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f', 
		'80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', 
		'90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 
		'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 
		'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 
		'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 
		'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 
		'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 
		'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
	r, g, b = colorfix(rgb)
	eh = f'#{r:02x}{g:02x}{b:02x}'
	#r = eh[:3]
	#g = eh[5:7]
	#b = eh[9:11]
	#if r == '':r = f"00"
	#if g == '':g = f"00"
	#if b == '':b = f"00"
	#if len(r) == 1:r = f"0{r}"
	#if len(g) == 1:g = f"0{g}"
	#if len(b) == 1:b = f"0{b}"
	#print(r, g, b)
	return eh#f"{r}{g}{b}"
def hex2rgb(hexx:str|tuple) -> tuple:
	hexx = hexx[1:]
	n = 2
	a = [hexx[i:i+n] for i in range(0, len(hexx), n)]
	return tuple(int(i, 16) for i in a)

class tkcolors():
	"""
	- `allcolors`    - every valid tkinter color stored in a dict{color name:hex of color name}
	- `unique_names` - every valid tkinter unique named color
	"""
	def allcolors():
		return {"snow": "#fffafa", "ghost white": "#f8f8ff", "GhostWhite": "#f8f8ff", "white smoke": "#f5f5f5", "WhiteSmoke": "#f5f5f5", "gainsboro": "#dcdcdc", "floral white": "#fffaf0", "FloralWhite": "#fffaf0", "old lace": "#fdf5e6", "OldLace": "#fdf5e6", "linen": "#faf0e6", "antique white": "#faebd7", "AntiqueWhite": "#faebd7", "papaya whip": "#ffefd5", "PapayaWhip": "#ffefd5", "blanched almond": "#ffebcd", "BlanchedAlmond": "#ffebcd", "bisque": "#ffe4c4", "peach puff": "#ffdab9", "PeachPuff": "#ffdab9", "navajo white": "#ffdead", "NavajoWhite": "#ffdead", "moccasin": "#ffe4b5", "cornsilk": "#fff8dc", "ivory": "#fffff0", "lemon chiffon": "#fffacd", "LemonChiffon": "#fffacd", "seashell": "#fff5ee", "honeydew": "#f0fff0", "mint cream": "#f5fffa", "MintCream": "#f5fffa", "azure": "#f0ffff", "alice blue": "#f0f8ff", "AliceBlue": "#f0f8ff", "lavender": "#e6e6fa", "lavender blush": "#fff0f5", "LavenderBlush": "#fff0f5", "misty rose": "#ffe4e1", "MistyRose": "#ffe4e1", "white": "#ffffff", "black": "#000000", "dark slate gray": "#2f4f4f", "DarkSlateGray": "#2f4f4f", "dark slate grey": "#2f4f4f", "DarkSlateGrey": "#2f4f4f", "dim gray": "#696969", "DimGray": "#696969", "dim grey": "#696969", "DimGrey": "#696969", "slate gray": "#708090", "SlateGray": "#708090", "slate grey": "#708090", "SlateGrey": "#708090", "light slate gray": "#778899", "LightSlateGray": "#778899", "light slate grey": "#778899", "LightSlateGrey": "#778899", "gray": "#bebebe", "grey": "#bebebe", "light grey": "#d3d3d3", "LightGrey": "#d3d3d3", "light gray": "#d3d3d3", "LightGray": "#d3d3d3", "midnight blue": "#191970", "MidnightBlue": "#191970", "navy": "#000080", "navy blue": "#000080", "NavyBlue": "#000080", "cornflower blue": "#6495ed", "CornflowerBlue": "#6495ed", "dark slate blue": "#483d8b", "DarkSlateBlue": "#483d8b", "slate blue": "#6a5acd", "SlateBlue": "#6a5acd", "medium slate blue": "#7b68ee", "MediumSlateBlue": "#7b68ee", "light slate blue": "#8470ff", "LightSlateBlue": "#8470ff", "medium blue": "#0000cd", "MediumBlue": "#0000cd", "royal blue": "#4169e1", "RoyalBlue": "#4169e1", "blue": "#0000ff", "dodger blue": "#1e90ff", "DodgerBlue": "#1e90ff", "deep sky blue": "#00bfff", "DeepSkyBlue": "#00bfff", "sky blue": "#87ceeb", "SkyBlue": "#87ceeb", "light sky blue": "#87cefa", "LightSkyBlue": "#87cefa", "steel blue": "#4682b4", "SteelBlue": "#4682b4", "light steel blue": "#b0c4de", "LightSteelBlue": "#b0c4de", "light blue": "#add8e6", "LightBlue": "#add8e6", "powder blue": "#b0e0e6", "PowderBlue": "#b0e0e6", "pale turquoise": "#afeeee", "PaleTurquoise": "#afeeee", "dark turquoise": "#00ced1", "DarkTurquoise": "#00ced1", "medium turquoise": "#48d1cc", "MediumTurquoise": "#48d1cc", "turquoise": "#40e0d0", "cyan": "#00ffff", "light cyan": "#e0ffff", "LightCyan": "#e0ffff", "cadet blue": "#5f9ea0", "CadetBlue": "#5f9ea0", "medium aquamarine": "#66cdaa", "MediumAquamarine": "#66cdaa", "aquamarine": "#7fffd4", "dark green": "#006400", "DarkGreen": "#006400", "dark olive green": "#556b2f", "DarkOliveGreen": "#556b2f", "dark sea green": "#8fbc8f", "DarkSeaGreen": "#8fbc8f", "sea green": "#2e8b57", "SeaGreen": "#2e8b57", "medium sea green": "#3cb371", "MediumSeaGreen": "#3cb371", "light sea green": "#20b2aa", "LightSeaGreen": "#20b2aa", "pale green": "#98fb98", "PaleGreen": "#98fb98", "spring green": "#00ff7f", "SpringGreen": "#00ff7f", "lawn green": "#7cfc00", "LawnGreen": "#7cfc00", "green": "#00ff00", "chartreuse": "#7fff00", "medium spring green": "#00fa9a", "MediumSpringGreen": "#00fa9a", "green yellow": "#adff2f", "GreenYellow": "#adff2f", "lime green": "#32cd32", "LimeGreen": "#32cd32", "yellow green": "#9acd32", "YellowGreen": "#9acd32", "forest green": "#228b22", "ForestGreen": "#228b22", "olive drab": "#6b8e23", "OliveDrab": "#6b8e23", "dark khaki": "#bdb76b", "DarkKhaki": "#bdb76b", "khaki": "#f0e68c", "pale goldenrod": "#eee8aa", "PaleGoldenrod": "#eee8aa", "light goldenrod yellow": "#fafad2", "LightGoldenrodYellow": "#fafad2", "light yellow": "#ffffe0", "LightYellow": "#ffffe0", "yellow": "#ffff00", "gold": "#ffd700", "light goldenrod": "#eedd82", "LightGoldenrod": "#eedd82", "goldenrod": "#daa520", "dark goldenrod": "#b8860b", "DarkGoldenrod": "#b8860b", "rosy brown": "#bc8f8f", "RosyBrown": "#bc8f8f", "indian red": "#cd5c5c", "IndianRed": "#cd5c5c", "saddle brown": "#8b4513", "SaddleBrown": "#8b4513", "sienna": "#a0522d", "peru": "#cd853f", "burlywood": "#deb887", "beige": "#f5f5dc", "wheat": "#f5deb3", "sandy brown": "#f4a460", "SandyBrown": "#f4a460", "tan": "#d2b48c", "chocolate": "#d2691e", "firebrick": "#b22222", "brown": "#a52a2a", "dark salmon": "#e9967a", "DarkSalmon": "#e9967a", "salmon": "#fa8072", "light salmon": "#ffa07a", "LightSalmon": "#ffa07a", "orange": "#ffa500", "dark orange": "#ff8c00", "DarkOrange": "#ff8c00", "coral": "#ff7f50", "light coral": "#f08080", "LightCoral": "#f08080", "tomato": "#ff6347", "orange red": "#ff4500", "OrangeRed": "#ff4500", "red": "#ff0000", "hot pink": "#ff69b4", "HotPink": "#ff69b4", "deep pink": "#ff1493", "DeepPink": "#ff1493", "pink": "#ffc0cb", "light pink": "#ffb6c1", "LightPink": "#ffb6c1", "pale violet red": "#db7093", "PaleVioletRed": "#db7093", "maroon": "#b03060", "medium violet red": "#c71585", "MediumVioletRed": "#c71585", "violet red": "#d02090", "VioletRed": "#d02090", "magenta": "#ff00ff", "violet": "#ee82ee", "plum": "#dda0dd", "orchid": "#da70d6", "medium orchid": "#ba55d3", "MediumOrchid": "#ba55d3", "dark orchid": "#9932cc", "DarkOrchid": "#9932cc", "dark violet": "#9400d3", "DarkViolet": "#9400d3", "blue violet": "#8a2be2", "BlueViolet": "#8a2be2", "purple": "#a020f0", "medium purple": "#9370db", "MediumPurple": "#9370db", "thistle": "#d8bfd8", "snow1": "#fffafa", "snow2": "#eee9e9", "snow3": "#cdc9c9", "snow4": "#8b8989", "seashell1": "#fff5ee", "seashell2": "#eee5de", "seashell3": "#cdc5bf", "seashell4": "#8b8682", "AntiqueWhite1": "#ffefdb", "AntiqueWhite2": "#eedfcc", "AntiqueWhite3": "#cdc0b0", "AntiqueWhite4": "#8b8378", "bisque1": "#ffe4c4", "bisque2": "#eed5b7", "bisque3": "#cdb79e", "bisque4": "#8b7d6b", "PeachPuff1": "#ffdab9", "PeachPuff2": "#eecbad", "PeachPuff3": "#cdaf95", "PeachPuff4": "#8b7765", "NavajoWhite1": "#ffdead", "NavajoWhite2": "#eecfa1", "NavajoWhite3": "#cdb38b", "NavajoWhite4": "#8b0c01", "LemonChiffon1": "#fffacd", "LemonChiffon2": "#eee9bf", "LemonChiffon3": "#cdc9a5", "LemonChiffon4": "#8b8970", "cornsilk1": "#fff8dc", "cornsilk2": "#eee8cd", "cornsilk3": "#cdc8b1", "cornsilk4": "#8b8878", "ivory1": "#fffff0", "ivory2": "#eeeee0", "ivory3": "#cdcdc1", "ivory4": "#8b8b83", "honeydew1": "#f0fff0", "honeydew2": "#e0eee0", "honeydew3": "#c1cdc1", "honeydew4": "#838b83", "LavenderBlush1": "#fff0f5", "LavenderBlush2": "#eee0e5", "LavenderBlush3": "#cdc1c5", "LavenderBlush4": "#8b8386", "MistyRose1": "#ffe4e1", "MistyRose2": "#eed5d2", "MistyRose3": "#cdb7b5", "MistyRose4": "#8b7d7b", "azure1": "#f0ffff", "azure2": "#e0eeee", "azure3": "#c1cdcd", "azure4": "#838b8b", "SlateBlue1": "#836fff", "SlateBlue2": "#7a67ee", "SlateBlue3": "#6959cd", "SlateBlue4": "#473c8b", "RoyalBlue1": "#4876ff", "RoyalBlue2": "#436eee", "RoyalBlue3": "#3a5fcd", "RoyalBlue4": "#27408b", "blue1": "#0000ff", "blue2": "#0000ee", "blue3": "#0000cd", "blue4": "#00008b", "DodgerBlue1": "#1e90ff", "DodgerBlue2": "#1c86ee", "DodgerBlue3": "#1874cd", "DodgerBlue4": "#104e8b", "SteelBlue1": "#63b8ff", "SteelBlue2": "#5cacee", "SteelBlue3": "#4f94cd", "SteelBlue4": "#36648b", "DeepSkyBlue1": "#00bfff", "DeepSkyBlue2": "#00b2ee", "DeepSkyBlue3": "#009acd", "DeepSkyBlue4": "#00688b", "SkyBlue1": "#87ceff", "SkyBlue2": "#7ec0ee", "SkyBlue3": "#6ca6cd", "SkyBlue4": "#4a708b", "LightSkyBlue1": "#b0e2ff", "LightSkyBlue2": "#a4d3ee", "LightSkyBlue3": "#8db6cd", "LightSkyBlue4": "#607b8b", "SlateGray1": "#c6e2ff", "SlateGray2": "#b9d3ee", "SlateGray3": "#9fb6cd", "SlateGray4": "#6c7b8b", "LightSteelBlue1": "#cae1ff", "LightSteelBlue2": "#bcd2ee", "LightSteelBlue3": "#a2b5cd", "LightSteelBlue4": "#6e7b8b", "LightBlue1": "#bfefff", "LightBlue2": "#b2dfee", "LightBlue3": "#9ac0cd", "LightBlue4": "#68838b", "LightCyan1": "#e0ffff", "LightCyan2": "#d1eeee", "LightCyan3": "#b4cdcd", "LightCyan4": "#7a8b8b", "PaleTurquoise1": "#bbffff", "PaleTurquoise2": "#aeeeee", "PaleTurquoise3": "#96cdcd", "PaleTurquoise4": "#668b8b", "CadetBlue1": "#98f5ff", "CadetBlue2": "#8ee5ee", "CadetBlue3": "#7ac5cd", "CadetBlue4": "#53868b", "turquoise1": "#00f5ff", "turquoise2": "#00e5ee", "turquoise3": "#00c5cd", "turquoise4": "#00868b", "cyan1": "#00ffff", "cyan2": "#00eeee", "cyan3": "#00cdcd", "cyan4": "#008b8b", "DarkSlateGray1": "#97ffff", "DarkSlateGray2": "#8deeee", "DarkSlateGray3": "#79cdcd", "DarkSlateGray4": "#528b8b", "aquamarine1": "#7fffd4", "aquamarine2": "#76eec6", "aquamarine3": "#66cdaa", "aquamarine4": "#458b74", "DarkSeaGreen1": "#c1ffc1", "DarkSeaGreen2": "#b4eeb4", "DarkSeaGreen3": "#9bcd9b", "DarkSeaGreen4": "#698b69", "SeaGreen1": "#54ff9f", "SeaGreen2": "#4eee94", "SeaGreen3": "#43cd80", "SeaGreen4": "#2e0d09", "PaleGreen1": "#9aff9a", "PaleGreen2": "#90ee90", "PaleGreen3": "#7ccd7c", "PaleGreen4": "#540d09", "SpringGreen1": "#00ff7f", "SpringGreen2": "#00ee76", "SpringGreen3": "#00cd66", "SpringGreen4": "#000d09", "green1": "#001905", "green2": "#001708", "green3": "#001405", "green4": "#000d09", "chartreuse1": "#7f1905", "chartreuse2": "#761708", "chartreuse3": "#661405", "chartreuse4": "#450d09", "OliveDrab1": "#c01905", "OliveDrab2": "#b31708", "OliveDrab3": "#9a1405", "OliveDrab4": "#690d09", "DarkOliveGreen1": "#caff70", "DarkOliveGreen2": "#bcee68", "DarkOliveGreen3": "#a21405", "DarkOliveGreen4": "#6e0d09", "khaki1": "#fff68f", "khaki2": "#eee685", "khaki3": "#cdc673", "khaki4": "#8b0d04", "LightGoldenrod1": "#ffec8b", "LightGoldenrod2": "#eedc82", "LightGoldenrod3": "#cdbe70", "LightGoldenrod4": "#8b0c09", "LightYellow1": "#ffffe0", "LightYellow2": "#eeeed1", "LightYellow3": "#cdcdb4", "LightYellow4": "#8b8b7a", "yellow1": "#ff1905", "yellow2": "#ee1708", "yellow3": "#cd1405", "yellow4": "#8b0d09", "gold1": "#ff1505", "gold2": "#ee1401", "gold3": "#cd1103", "gold4": "#8b0b07", "goldenrod1": "#ff1303", "goldenrod2": "#ee1200", "goldenrod3": "#cd0f05", "goldenrod4": "#8b0a05", "DarkGoldenrod1": "#ff1205", "DarkGoldenrod2": "#ee1103", "DarkGoldenrod3": "#cd0e09", "DarkGoldenrod4": "#8b0a01", "RosyBrown1": "#ffc1c1", "RosyBrown2": "#eeb4b4", "RosyBrown3": "#cd9b9b", "RosyBrown4": "#8b6969", "IndianRed1": "#ff6a6a", "IndianRed2": "#ee0909", "IndianRed3": "#cd0805", "IndianRed4": "#8b0508", "sienna1": "#ff0d00", "sienna2": "#ee0c01", "sienna3": "#cd0a04", "sienna4": "#8b0701", "burlywood1": "#ffd39b", "burlywood2": "#eec591", "burlywood3": "#cdaa7d", "burlywood4": "#8b0b05", "wheat1": "#ffe7ba", "wheat2": "#eed8ae", "wheat3": "#cdba96", "wheat4": "#8b7e66", "tan1": "#ff1005", "tan2": "#ee0f04", "tan3": "#cd0d03", "tan4": "#8b0900", "chocolate1": "#ff0c07", "chocolate2": "#ee0b08", "chocolate3": "#cd0a02", "chocolate4": "#8b0609", "firebrick1": "#ff0408", "firebrick2": "#ee0404", "firebrick3": "#cd0308", "firebrick4": "#8b0206", "brown1": "#ff0604", "brown2": "#ee0509", "brown3": "#cd0501", "brown4": "#8b0305", "salmon1": "#ff8c69", "salmon2": "#ee0d00", "salmon3": "#cd0b02", "salmon4": "#8b0706", "LightSalmon1": "#ffa07a", "LightSalmon2": "#ee9572", "LightSalmon3": "#cd0c09", "LightSalmon4": "#8b0807", "orange1": "#ff1005", "orange2": "#ee0f04", "orange3": "#cd0d03", "orange4": "#8b0900", "DarkOrange1": "#ff0c07", "DarkOrange2": "#ee0b08", "DarkOrange3": "#cd0a02", "DarkOrange4": "#8b0609", "coral1": "#ff0b04", "coral2": "#ee0a06", "coral3": "#cd0901", "coral4": "#8b0602", "tomato1": "#ff0909", "tomato2": "#ee0902", "tomato3": "#cd0709", "tomato4": "#8b0504", "OrangeRed1": "#ff0609", "OrangeRed2": "#ee0604", "OrangeRed3": "#cd0505", "OrangeRed4": "#8b0307", "red1": "#190500", "red2": "#170800", "red3": "#140500", "red4": "#0d0900", "DeepPink1": "#ff1493", "DeepPink2": "#ee1289", "DeepPink3": "#cd1076", "DeepPink4": "#8b0100", "HotPink1": "#ff6eb4", "HotPink2": "#ee6aa7", "HotPink3": "#cd6090", "HotPink4": "#8b3a62", "pink1": "#ffb5c5", "pink2": "#eea9b8", "pink3": "#cd919e", "pink4": "#8b636c", "LightPink1": "#ffaeb9", "LightPink2": "#eea2ad", "LightPink3": "#cd8c95", "LightPink4": "#8b5f65", "PaleVioletRed1": "#ff82ab", "PaleVioletRed2": "#ee799f", "PaleVioletRed3": "#cd6889", "PaleVioletRed4": "#8b0701", "maroon1": "#ff34b3", "maroon2": "#ee30a7", "maroon3": "#cd2990", "maroon4": "#8b0208", "VioletRed1": "#ff3e96", "VioletRed2": "#ee3a8c", "VioletRed3": "#cd3278", "VioletRed4": "#8b0304", "magenta1": "#ff00ff", "magenta2": "#ee00ee", "magenta3": "#cd00cd", "magenta4": "#8b008b", "orchid1": "#ff83fa", "orchid2": "#ee7ae9", "orchid3": "#cd69c9", "orchid4": "#8b4789", "plum1": "#ffbbff", "plum2": "#eeaeee", "plum3": "#cd96cd", "plum4": "#8b668b", "MediumOrchid1": "#e066ff", "MediumOrchid2": "#d15fee", "MediumOrchid3": "#b452cd", "MediumOrchid4": "#7a378b", "DarkOrchid1": "#bf3eff", "DarkOrchid2": "#b23aee", "DarkOrchid3": "#9a32cd", "DarkOrchid4": "#68228b", "purple1": "#9b30ff", "purple2": "#912cee", "purple3": "#7d26cd", "purple4": "#551a8b", "MediumPurple1": "#ab82ff", "MediumPurple2": "#9f79ee", "MediumPurple3": "#8968cd", "MediumPurple4": "#5d478b", "thistle1": "#ffe1ff", "thistle2": "#eed2ee", "thistle3": "#cdb5cd", "thistle4": "#8b7b8b", "gray0": "#000000", "grey0": "#000000", "gray1": "#030303", "grey1": "#030303", "gray2": "#050505", "grey2": "#050505", "gray3": "#080808", "grey3": "#080808", "gray4": "#0a0a0a", "grey4": "#0a0a0a", "gray5": "#0d0d0d", "grey5": "#0d0d0d", "gray6": "#0f0f0f", "grey6": "#0f0f0f", "gray7": "#121212", "grey7": "#121212", "gray8": "#141414", "grey8": "#141414", "gray9": "#171717", "grey9": "#171717", "gray10": "#1a1a1a", "grey10": "#1a1a1a", "gray11": "#1c1c1c", "grey11": "#1c1c1c", "gray12": "#1f1f1f", "grey12": "#1f1f1f", "gray13": "#212121", "grey13": "#212121", "gray14": "#242424", "grey14": "#242424", "gray15": "#262626", "grey15": "#262626", "gray16": "#292929", "grey16": "#292929", "gray17": "#2b2b2b", "grey17": "#2b2b2b", "gray18": "#2e2e2e", "grey18": "#2e2e2e", "gray19": "#303030", "grey19": "#303030", "gray20": "#333333", "grey20": "#333333", "gray21": "#363636", "grey21": "#363636", "gray22": "#383838", "grey22": "#383838", "gray23": "#3b3b3b", "grey23": "#3b3b3b", "gray24": "#3d3d3d", "grey24": "#3d3d3d", "gray25": "#404040", "grey25": "#404040", "gray26": "#424242", "grey26": "#424242", "gray27": "#454545", "grey27": "#454545", "gray28": "#474747", "grey28": "#474747", "gray29": "#4a4a4a", "grey29": "#4a4a4a", "gray30": "#4d4d4d", "grey30": "#4d4d4d", "gray31": "#4f4f4f", "grey31": "#4f4f4f", "gray32": "#525252", "grey32": "#525252", "gray33": "#545454", "grey33": "#545454", "gray34": "#575757", "grey34": "#575757", "gray35": "#595959", "grey35": "#595959", "gray36": "#5c5c5c", "grey36": "#5c5c5c", "gray37": "#5e5e5e", "grey37": "#5e5e5e", "gray38": "#616161", "grey38": "#616161", "gray39": "#636363", "grey39": "#636363", "gray40": "#666666", "grey40": "#666666", "gray41": "#696969", "grey41": "#696969", "gray42": "#6b6b6b", "grey42": "#6b6b6b", "gray43": "#6e6e6e", "grey43": "#6e6e6e", "gray44": "#707070", "grey44": "#707070", "gray45": "#737373", "grey45": "#737373", "gray46": "#757575", "grey46": "#757575", "gray47": "#787878", "grey47": "#787878", "gray48": "#7a7a7a", "grey48": "#7a7a7a", "gray49": "#7d7d7d", "grey49": "#7d7d7d", "gray50": "#7f7f7f", "grey50": "#7f7f7f", "gray51": "#828282", "grey51": "#828282", "gray52": "#858585", "grey52": "#858585", "gray53": "#878787", "grey53": "#878787", "gray54": "#8a8a8a", "grey54": "#8a8a8a", "gray55": "#8c8c8c", "grey55": "#8c8c8c", "gray56": "#8f8f8f", "grey56": "#8f8f8f", "gray57": "#919191", "grey57": "#919191", "gray58": "#949494", "grey58": "#949494", "gray59": "#969696", "grey59": "#969696", "gray60": "#999999", "grey60": "#999999", "gray61": "#9c9c9c", "grey61": "#9c9c9c", "gray62": "#9e9e9e", "grey62": "#9e9e9e", "gray63": "#a1a1a1", "grey63": "#a1a1a1", "gray64": "#a3a3a3", "grey64": "#a3a3a3", "gray65": "#a6a6a6", "grey65": "#a6a6a6", "gray66": "#a8a8a8", "grey66": "#a8a8a8", "gray67": "#ababab", "grey67": "#ababab", "gray68": "#adadad", "grey68": "#adadad", "gray69": "#b0b0b0", "grey69": "#b0b0b0", "gray70": "#b3b3b3", "grey70": "#b3b3b3", "gray71": "#b5b5b5", "grey71": "#b5b5b5", "gray72": "#b8b8b8", "grey72": "#b8b8b8", "gray73": "#bababa", "grey73": "#bababa", "gray74": "#bdbdbd", "grey74": "#bdbdbd", "gray75": "#bfbfbf", "grey75": "#bfbfbf", "gray76": "#c2c2c2", "grey76": "#c2c2c2", "gray77": "#c4c4c4", "grey77": "#c4c4c4", "gray78": "#c7c7c7", "grey78": "#c7c7c7", "gray79": "#c9c9c9", "grey79": "#c9c9c9", "gray80": "#cccccc", "grey80": "#cccccc", "gray81": "#cfcfcf", "grey81": "#cfcfcf", "gray82": "#d1d1d1", "grey82": "#d1d1d1", "gray83": "#d4d4d4", "grey83": "#d4d4d4", "gray84": "#d6d6d6", "grey84": "#d6d6d6", "gray85": "#d9d9d9", "grey85": "#d9d9d9", "gray86": "#dbdbdb", "grey86": "#dbdbdb", "gray87": "#dedede", "grey87": "#dedede", "gray88": "#e0e0e0", "grey88": "#e0e0e0", "gray89": "#e3e3e3", "grey89": "#e3e3e3", "gray90": "#e5e5e5", "grey90": "#e5e5e5", "gray91": "#e8e8e8", "grey91": "#e8e8e8", "gray92": "#ebebeb", "grey92": "#ebebeb", "gray93": "#ededed", "grey93": "#ededed", "gray94": "#f0f0f0", "grey94": "#f0f0f0", "gray95": "#f2f2f2", "grey95": "#f2f2f2", "gray96": "#f5f5f5", "grey96": "#f5f5f5", "gray97": "#f7f7f7", "grey97": "#f7f7f7", "gray98": "#fafafa", "grey98": "#fafafa", "gray99": "#fcfcfc", "grey99": "#fcfcfc", "gray100": "#ffffff", "grey100": "#ffffff", "dark grey": "#a9a9a9", "DarkGrey": "#a9a9a9", "dark gray": "#a9a9a9", "DarkGray": "#a9a9a9", "dark blue": "#00008b", "DarkBlue": "#00008b", "dark cyan": "#008b8b", "DarkCyan": "#008b8b", "dark magenta": "#8b008b", "DarkMagenta": "#8b008b", "dark red": "#8b0000", "DarkRed": "#8b0000", "light green": "#90ee90", "LightGreen": "#90ee90"}
	def unique_names():
		return ['alice blue', 'antique white', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'black', 'BlanchedAlmond', 'blue violet', 'cadet blue', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'cornflower blue', 'dark blue', 'dark cyan', 'dark goldenrod', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'dark gray', 'dark green', 'dark khaki', 'dark magenta', 'dark olive green', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'dark orange', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'dark orchid', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'dark red', 'dark salmon', 'dark sea green', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'dark slate blue', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4', 'dark slate gray', 'dark turquoise', 'dark violet', 'DeepPink1', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'DeepSkyBlue1', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'DodgerBlue1', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'floral white', 'forest green', 'ghost white', 'green yellow', 'hot pink', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'indian red', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'LavenderBlush1', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'lawn green', 'LemonChiffon1', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'light blue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'light coral', 'LightCyan1', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'light goldenrod', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'light goldenrod yellow', 'light gray', 'light green', 'light pink', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'LightSalmon1', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'light sea green', 'light sky blue', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'light slate blue', 'light slate gray', 'light steel blue', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightYellow1', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'lime green', 'medium orchid', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'medium purple', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'medium sea green', 'medium slate blue', 'medium spring green', 'medium turquoise', 'medium violet red', 'midnight blue', 'mint cream', 'MistyRose1', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'navajo white', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'navy blue', 'old lace', 'olive drab', 'OliveDrab1', 'OliveDrab2', 'OliveDrab3', 'OliveDrab4', 'orange red', 'OrangeRed1', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'pale goldenrod', 'pale green', 'PaleGreen1', 'PaleGreen3', 'PaleGreen4', 'pale turquoise', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'pale violet red', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'papaya whip', 'PeachPuff1', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'powder blue', 'rosy brown', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'royal blue', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'saddle brown', 'sandy brown', 'sea green', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'SeaGreen4', 'sky blue', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'slate blue', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3', 'SlateGray4', 'slate gray', 'SpringGreen1', 'SpringGreen2', 'SpringGreen3', 'steel blue', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'violet red', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'yellow green', 'aquamarine1', 'aquamarine2', 'aquamarine3', 'aquamarine4', 'azure1', 'azure2', 'azure3', 'azure4', 'beige', 'bisque1', 'bisque2', 'bisque3', 'bisque4', 'blue1', 'blue2', 'blue3', 'brown', 'brown1', 'brown2', 'brown3', 'brown4', 'burlywood', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'chartreuse', 'chartreuse1', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'chocolate', 'coral', 'coral1', 'coral2', 'coral3', 'coral4', 'cornsilk1', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'cyan1', 'cyan2', 'cyan3', 'firebrick', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'gainsboro', 'gold', 'gold1', 'gold2', 'gold3', 'gold4', 'goldenrod', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'green', 'green1', 'green2', 'green3', 'green4', 'grey', 'grey0', 'grey1', 'grey10', 'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19', 'grey2', 'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28', 'grey29', 'grey3', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37', 'grey38', 'grey39', 'grey4', 'grey40', 'grey41', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47', 'grey48', 'grey49', 'grey5', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56', 'grey57', 'grey58', 'grey59', 'grey6', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65', 'grey66', 'grey67', 'grey68', 'grey69', 'grey7', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74', 'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey8', 'grey80', 'grey81', 'grey82', 'grey83', 'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey9', 'grey90', 'grey91', 'grey92', 'grey93', 'grey94', 'grey95', 'grey96', 'grey97', 'grey98', 'grey99', 'honeydew1', 'honeydew2', 'honeydew3', 'honeydew4', 'ivory1', 'ivory2', 'ivory3', 'ivory4', 'khaki', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'lavender', 'linen', 'magenta1', 'magenta2', 'magenta3', 'maroon', 'maroon1', 'maroon2', 'maroon3', 'maroon4', 'moccasin', 'orange', 'orange1', 'orange2', 'orange3', 'orange4', 'orchid', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'peru', 'pink', 'pink1', 'pink2', 'pink3', 'pink4', 'plum', 'plum1', 'plum2', 'plum3', 'plum4', 'purple', 'purple1', 'purple2', 'purple3', 'purple4', 'red', 'red1', 'red2', 'red3', 'red4', 'salmon', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'seashell1', 'seashell2', 'seashell3', 'seashell4', 'sienna', 'sienna1', 'sienna2', 'sienna3', 'snow1', 'snow2', 'snow3', 'snow4', 'tan', 'thistle', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'tomato', 'tomato1', 'tomato2', 'tomato3', 'tomato4', 'turquoise', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'violet', 'wheat', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'white', 'yellow', 'yellow1', 'yellow2', 'yellow3', 'yellow4']

class Example():
	def __init__(self):
		self.root = tkinter.Tk()
		self.root.geometry("290x260")
		# binds the menubar the the root
		menubar = tkinter.Menu(self.root)
		menubar.add_command(label="open list of all named tkinter colors", command=self.colorlist)
		self.root.config(menu=menubar)

		self.colorlabel = Label(self.root, text="               ", background="#000000", foreground=TCC("#000000"))
		self.hex_r = Label(self.root, text="00")
		self.hex_g = Label(self.root, text="00")
		self.hex_b = Label(self.root, text="00")
		self.scale = tkinter.Scale(self.root, orient='horizontal', length=250, from_=0, to=255, command=self.sacale)
		self.scale1 = tkinter.Scale(self.root, orient='horizontal', length=250, from_=0, to=255, command=self.sacale)
		self.scale2 = tkinter.Scale(self.root, orient='horizontal', length=250, from_=0, to=255, command=self.sacale)
		# hex
		self.hexxl = Label(self.root, text="hex")
		self.hexx = Entry(self.root, width=40)
		self.hexx.insert('end','#000000')
		self.hexx.config(state='disabled')
		# rgb
		self.rgbl = Label(self.root, text="rgb")
		self.rgb = Entry(self.root, width=40)
		self.rgb.insert('end','0, 0, 0')
		self.rgb.config(state='disabled')
		# hsv
		self.hsvl = Label(self.root, text="hsv")
		self.hsv = Entry(self.root, width=40)
		self.hsv.insert('end','0, 0%, 0%')
		self.hsv.config(state='disabled')
		# hsl
		self.hsll = Label(self.root, text="hsl")
		self.hsl = Entry(self.root, width=40)
		self.hsl.insert('end','0, 0%, 0%')
		self.hsl.config(state='disabled')
		# cmyk
		self.cmykl = Label(self.root, text="cmyk")
		self.cmyk = Entry(self.root, width=40)
		self.cmyk.insert('end','0%, 0%, 0%, 0%')
		self.cmyk.config(state='disabled')

		self.colorlabel.grid(column=1, row=1)
		self.hex_r.grid(column=0, row=2)
		self.scale.grid(column=1, row=2, columnspan=2)
		self.hex_g.grid(column=0, row=3)
		self.scale1.grid(column=1, row=3, columnspan=2)
		self.hex_b.grid(column=0, row=4)
		self.scale2.grid(column=1, row=4, columnspan=2)

		self.hexxl.grid(column=0, row=5)
		self.hexx.grid( column=1, row=5)
		self.rgbl.grid( column=0, row=6)
		self.rgb.grid(  column=1, row=6)
		self.hsvl.grid( column=0, row=7)
		self.hsv.grid(  column=1, row=7)
		self.hsll.grid( column=0, row=8)
		self.hsl.grid(  column=1, row=8)
		self.cmykl.grid(column=0, row=9)
		self.cmyk.grid( column=1, row=9)

		#self.root.bind('<Configure>', self.test)
		self.root.mainloop()

	def test(self, event):
		self.scale.config(length=self.root.winfo_width())
		self.scale1.config(length=self.root.winfo_width())
		self.scale2.config(length=self.root.winfo_width())
	def sacale(self, event):
		r = self.scale.get()
		g = self.scale1.get()
		b = self.scale2.get()
		interloper = (r, g, b)
		hex = rgb2hex(interloper)
		hsv = rgb2hsv(interloper)
		hsl = rgb2hsl(interloper)
		cmyk = rgb2cmyk(interloper)
		self.colorlabel.config(background=hex)#, text=hex, foreground=TCC(hex)
		#self.root.config(background=f'#{h}{e}{x}')
		self.hex_r.config(text=hex[1:3])
		self.hex_g.config(text=hex[3:5])
		self.hex_b.config(text=hex[5:7])
		self.hsl.config(state='normal')
		self.hsv.config(state='normal')
		self.rgb.config(state='normal')
		self.hexx.config(state='normal')
		self.cmyk.config(state='normal')
		self.hexx.delete(0,'end')
		self.hexx.insert('end', hex)
		self.rgb.delete(0,'end')
		self.rgb.insert('end', interloper)
		self.hsv.delete(0,'end')
		self.hsv.insert('end', hsv)
		self.hsl.delete(0,'end')
		self.hsl.insert('end', hsl)
		self.cmyk.delete(0,'end')
		self.cmyk.insert('end', cmyk)
		self.hexx.config(state='disabled')
		self.rgb.config(state='disabled')
		self.hsv.config(state='disabled')
		self.hsl.config(state='disabled')
		self.cmyk.config(state='disabled')

	def colorlist(self):
		self.lastbox = None
		self.dontcenter = 0
		# GUI
		toplevel = tkinter.Toplevel()
		toplevel.grid_rowconfigure(0, weight=1)
		toplevel.grid_columnconfigure(0, weight=1)
		toplevel.title('Pynche Color List')
		toplevel.iconname('Pynche Color List')
		#
		# create the canvas which holds everything, and its scrollbar
		#
		self.canvas = tkinter.Text(toplevel, state='normal', width=38, height=40, wrap='word')

		self.canvas = tkinter.Canvas(toplevel, width=160, height=300, borderwidth=2, relief='sunken')
		self.canvas.bind('<MouseWheel>', self.scroll)
		scrollbar = Scrollbar(toplevel, command=self.canvas.yview)
		self.canvas.config(yscrollcommand=scrollbar.set)

		scrollbar.grid(sticky='NS', column=1, row=0)
		self.canvas.grid(sticky='NSEW', column=0, row=0)
		self.populate()

		# alias list
		self.alabel = Label(toplevel, text='Aliases:')
		self.alabel.grid(column=0, row=1)
		self.aliases = tkinter.Listbox(toplevel, height=5, selectmode='browse')
		self.aliases.grid(sticky='NSEW', column=0, row=2)
	def scroll(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/20)), "units")

	def populate(self):
		#
		# create all the buttons
		row = 0
		widest = 0
		bboxes = self.__bboxes = []
		for name in tkcolors.unique_names():
			exactcolor = tkcolors.allcolors()[name]
			self.canvas.create_rectangle(5, row*20 + 5, 20, row*20 + 20, fill=exactcolor)
			textid = self.canvas.create_text(25, row*20 + 13,text=name,anchor='w')
			x1, y1, textend, y2 = self.canvas.bbox(textid)
			boxid = self.canvas.create_rectangle(3, row*20+3,textend+3, row*20 + 23,outline='',tags=(name, exactcolor, 'all'))
			self.canvas.bind('<ButtonRelease>', self.onrelease)
			bboxes.append(boxid)
			if textend+3 > widest:
				widest = textend+3
			row += 1
		canvheight = (row-1)*20 + 25
		self.canvas.config(scrollregion=(0, 0, 150, canvheight))
		for box in bboxes:
			x1, y1, _, y2 = self.canvas.coords(box)
			self.canvas.coords(box, x1, y1, widest, y2)

	def onrelease(self, event=None):
		# find the current box
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		ids = self.canvas.find_overlapping(x, y, x, y)
		for boxid in ids:
			if boxid in self.__bboxes:
				break
		else:
			##print('No box found!')
			return
		tags = self.canvas.gettags(boxid)
		taglist = []
		for t in tags:
			taglist.append(t)
			if t[0] == '#':
				break
		else:
			##print('No color tag found!')
			return
		self.dontcenter = 1
		self.update_yourself(taglist)

	def update_yourself(self, t):#red, green, blue
		# turn off the last box
		if self.lastbox:
			self.canvas.itemconfigure(self.lastbox, outline='')
		# turn on the current box
		self.canvas.itemconfigure(t[1], outline='black')
		self.lastbox = t[1]
		# fill the aliases
		self.aliases.delete(0, 'end')
		#self.aliases.insert('end', '<no aliases>')

		#try:
		unaliased = tkcolors.allcolors()
		aliased = {}
		for i, x in unaliased.items():
			if aliased.get(x):
				aliased[x].append(i)
			else:
				aliased[x] = [i]
		#except Exception:
		#	pass

		# t is (#hex, name)
		a = aliased[t[1]]
		# removes its own name so if list has length of 1 its own name is removed meaning it has no aliases
		a.remove(t[0])
		# if list is empty there is no aliases
		if not a:
			self.aliases.insert('end', '<no aliases>')
		else:
			print(t[1], a)
			# if list is not empty loop what is there
			for i in a:
				self.aliases.insert('end', i)

		# maybe scroll the canvas so that the item is visible
		if self.dontcenter:
			self.dontcenter = 0
		else:
			_, _, _, y1 = self.canvas.coords(t[1])
			_, _, _, y2 = self.canvas.coords(self.__bboxes[-1])
			h = int(self.canvas['height']) * 0.5
			self.canvas.yview('moveto', (y1-h) / y2)

if __name__ == "__main__":
	import tkinter
	from tkinter.ttk import *
	print(f"random color             {randcolor()}")
	print()
	print('#0000FF')
	print(f"Readable Colors hex      {ReadableColors('#0000FF')}")#7878ff
	print()
	print('Text Color Correction')
	print('#006AFF, \'0, 106, 255\', (0, 106, 255)')
	print(f"TCC hex           {TCC('#006AFF')}")
	print()
	print(f"hex color invert  {invert('#006AFF')}")
	print()
	print('0, 106, 255')
	print(f"hex to rgb        {hex2rgb('#006AFF')}")
	print('#006AFF')
	print(f"rgb to hex        {rgb2hex('rgb(0, 106, 255)')}")
	print()
	#print(f"rgb to yiq   {rgb2yiq('0, 106, 255')}")
	#print(f"yiq to rgb   {yiq2rgb('90.59, -111.4273, 23.924899999999994')}")
	#print()
	#print(f"rgb to hls   {rgb2hls('0, 106, 255')}")
	#print(f"hsl to rgb   {hls2rgb('0.5973856209150327, 127.5, -1.007905138339921')}")
	#print()
	print('0, 106, 255')
	print(f"rgb to hsv        {rgb2hsv('rgb(0, 106, 255)')}")
	print()
	print('215.05882352941177, 100.0, 100.0')
	print(f"hsv to rgb        {hsv2rgb('hsv(215.05882352941177, 100.0%, 100.0%)')}")
	print()
	print('0, 106, 255')
	print(f"rgb to Cmyk       {rgb2cmyk('rgb(0, 106, 255)')}")
	print()
	print('100.0, 58.4313725490196, 0.0, 0.0')
	print(f"Cmyk to rgb       {cmyk2rgb('cmyk(100.0%, 58.4313725490196%, 0.0%, 0.0%)')}")
	print()
	print('0, 106, 255')
	print(f"rgb to hsl        {rgb2hsl('rgb(0, 106, 255)')}")
	print()
	print('215.05882352941177, 100, 50')
	print(f"hsl to rgb        {hsl2rgb('hsl(215.05882352941177, 100%, 50%)')}")
	print()
	print('0, 106, 255')
	print(f"hsv to hwb        {hsv2hwb('rgb(0, 106, 255)')}")
	print()
	print('215, 0, 0')
	print(f"hwb to hsv        {hwb2hsv('hwb(215, 0%, 0%)')}")
	#os.system("pause")
	Example()