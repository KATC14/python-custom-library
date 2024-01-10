# python-custom-library
python library intended to live in install of python for easy importing

# color_tools
- randcolor
  - returns random color in hex
- ReadableColors
  - returns color with a higher contrast
- TCC (text color correction)
  - returns black or white based on how dark or light given color is
- invert
  - returns inverted hex color from given hex
- hex2rgb
  - returns rgb color coverted from given hex
- rgb2hex
  - returns hex color coverted from given rgb
- rgb2hsv
  - returns hsv color coverted from given rgb
- hsv2rgb
  - returns rgb color coverted from given hsv
- rgb2cmyk
  - returns rgb color coverted from given cmyk
- cmyk2rgb
  - returns rgb color coverted from given cmyk
- rgb2hsl
  - returns hsl color coverted from given rgb
- hsl2rgb
  - returns rgb color coverted from given hsl
- hsv2hwb
  - returns hwb color coverted from given hsv
- hwb2hsv
  - returns hsv color coverted from given hwb

# twitch irc parser
[python port](https://github.com/KATC14/twitch_irc_parser) of [dev.twitch example message parser](https://dev.twitch.tv/docs/irc/example-parser/#example-message-parser) and heavy modification

# utilities
- ascii_change
  - can change a-z A-Z 0-9 and a bunch of symbols
- cut_convert
  - converts time from given datetime object to default Eastern Standard Time
- dict_replace
  - replace multiple items in a string
- genaric_header
  - returns dict based on input dict
- is_int
  - returns int or input
- is_float
  - returns float, int or input
- base42
  - encode or decode strings in base 64
- more_than_one
  - returns plural (defaults to s) if amount above 1 or equal to 0
- ordinal
  - ordinal_suffix
    - return ordinal suffix of given integer (st, nd, rd, th)
  - to_ordinal
    - return an integer n (+ve or -ve) to ordinal version.
  - from_ordinal
    - return an a ordinal version of a number back to a integer
- pi
  - returns x decimals of pi
- time_stamp
  - returns current time. default 12 hour format
- time_amount
  - return string with 'Weekday, Month, Day & ordinal, Year, 12-hour, Minute, Second'
- time_since
  - return amount of time since given datetime object to end_time defaults to current time returned by datetime.now()
- unicode_replace
  - makes translation table usable for str.translate(TranslateTable). and returns the translated input
- url_request
  - Open the given url with given headers(dict), data(must be encoded), method and SSL context
