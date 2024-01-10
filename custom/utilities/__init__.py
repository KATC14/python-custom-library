"""random collection of utility like functions

- `generic_header`  - returns dict based on input dict
- `url_request`     - Open the given url, which must be a string
- `more_than_one`   - returns plural (defaults to s) if amount above 1 or equal to 0
- `is_int`          - returns int or input
- `is_float`        - returns float, int or input
- `base42`          - encode or decode strings in base 64
- `dict_replace`    - replace multiple items in a string
- `time_stamp`      - returns current time. default 12 hour format
- `cut_convert`     - converts time from given datetime object to default Eastern Standard Time
- `csv_pprint`      - returns csv with added whitespaces
- `csv_read`        - fixes csv data that is saved with csv_pprint...
- `time_amount`     - return string with 'Weekday, Month, Day & ordinal, Year, 12-hour, Minute, Second'
- `time_since`      - return amount of time since given datetime object to end_time defaults to current time returned by datetime.now()
- `ordinal_suffix`  - return ordinal suffix of given integer (st, nd, rd, th)
- `to_ordinal`      - return an integer n (+ve or -ve) to ordinal version.
- `from_ordinal`    - return an a ordinal version of a number back to a integer
- `ascii_change`    - can change a-z A-Z 0-9 and a bunch of symbols
- `unicode_replace` - makes translation table usable for str.translate(TranslateTable). and returns the translated input
- `pi`              - returns x decimals of pi
"""
#- `url_format`      - url_format('abc def', 'encode') -> 'abc%20def' url_format('abc%20def', 'decode') -> 'abc def'

from .asciige    import ascii_change
from .cutert     import cut_convert
from .dictlace   import dict_replace
from .gead       import generic_header
from .isint      import is_int
from .isoat      import is_float
from .life       import base42
from .moane      import more_than_one
from .ordinal    import *
from .pie        import pi
from .timamp     import time_stamp
from .timeount   import time_amount
from .timince    import time_since
from .uniplace   import unicode_replace
from .urlest     import url_request
from .pretty_csv import *
#from .urlmat  import url_format

__all__ = [
    'ascii_change', 
    'cut_convert', 
    'csv_pprint',
    'csv_read',
    'dict_replace', 
    'generic_header', 
    'is_int', 
    'is_float', 
    'base42', 
    'more_than_one', 
    'ordinal_suffix', 
    'to_ordinal', 
    'from_ordinal', 
    'pi', 
    'time_stamp', 
    'time_amount', 
    'time_since', 
    'unicode_replace', 
    'url_request'
    #'url_format'
]
