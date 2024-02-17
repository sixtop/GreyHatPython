from ctypes import *


class BarleyAmount(Union):
    _fields_ = [
        ("barley_long", c_long),
        ("barley_int", c_int),
        ("barley_char", c_char * 8),
    ]


value = input("enter amount:")
my_barley = BarleyAmount(int (value))

print("Barley amount as a long: %ld" % my_barley.barley_long)
print("Barley amount as an int: %d" % my_barley.barley_long)
print("Barley amount as a char: %s" % my_barley.barley_char)