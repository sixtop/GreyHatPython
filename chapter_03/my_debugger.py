from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class Debugger():
    def __init__(self):
        pass

    def load(self, path_to_exe):
        # dwCreation flag determines how to create the process
        # set creation_flags = CREATE_NEW_CONSOLE if you want
        # to see the calculator GUI
        creation_flags = DEBUG_PROCESS

        # instantiate the structs
        startupinfo         = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        # The following two options allow the started process
        # to be shown as a separate window. This also illustrates
        # how different settings in the STARTUPINFO struct can affect
        # the debuggee.
        startupinfo.dwFlags     = 0x1
        startupinfo.wShowWindow = 0x0

        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print(f"[*] successfully launched the process!")
            print(f"[*] PID {process_information.dwProcessId}")
        else:
            print(f"[*] Error: {kernel32.GetLastError()}")
