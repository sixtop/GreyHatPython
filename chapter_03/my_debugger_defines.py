from ctypes import *

# mapping MS types to ctypes for clarity
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPSTR = POINTER(c_char)
HANDLE = c_void_p

# constants
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010

# CreateProcessA function (processthreadsapi.h)
# Creates a new process and its primary thread. The new process runs in the security context of the calling process.
#
# https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa
#
# BOOL CreateProcessA(
#  [in, optional]      LPCSTR                lpApplicationName,
#  [in, out, optional] LPSTR                 lpCommandLine,
#  [in, optional]      LPSECURITY_ATTRIBUTES lpProcessAttributes,
#  [in, optional]      LPSECURITY_ATTRIBUTES lpThreadAttributes,
#  [in]                BOOL                  bInheritHandles,
#  [in]                DWORD                 dwCreationFlags,
#  [in, optional]      LPVOID                lpEnvironment,
#  [in, optional]      LPCSTR                lpCurrentDirectory,
#  [in]                LPSTARTUPINFOA        lpStartupInfo,
#  [out]               LPPROCESS_INFORMATION lpProcessInformation
#);


# STARTUPINFOA (processthreadsapi.h)
# https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfoa
class STARTUPINFO (Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPSTR),
        ("lpDesktop", LPSTR),
        ("lpTitle", LPSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", DWORD),
        ("cbReserved2", DWORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE),
    ]


# PROCESS_INFORMATION (processthreadsapi.h)
# https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information
class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
    ]
