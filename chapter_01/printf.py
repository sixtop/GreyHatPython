from ctypes import *

# We get access to windll, cdll
print(windll.kernel32)
print(cdll.msvcrt)

# reference to it
libc = cdll.msvcrt

message_string = b"Hello world!\n"
libc.printf(b"Testing: %s", message_string)