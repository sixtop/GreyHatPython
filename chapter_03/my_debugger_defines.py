from ctypes import *

# mapping MS types to ctypes for clarity
# https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types
BYTE = c_ubyte
WORD = c_ushort
DWORD = c_ulong
LONG = c_long
LPBYTE = POINTER(c_ubyte)
LPSTR = POINTER(c_char)
HANDLE = c_void_p
PVOID = c_void_p
UINT_PTR = c_ulong

#x64
DWORD64 = c_ulonglong  # A 64-bit unsigned integer.
ULONGLONG = c_ulonglong

# constants
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010
PROCESS_ALL_ACCESS = 0x001F0FFF # https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights
INFINITE = 0xFFFFFFFF
DBG_CONTINUE = 0x00010002

# Debug event constants

# Thread constants for CreateToolhelp32Snapshot()
#TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPTHREAD = 0x00000004
THREAD_ALL_ACCESS = 0x001F03FF

# Context flags for GetThreadContext()
#CONTEXT_FULL                   = 0x00010007
#CONTEXT_DEBUG_REGISTERS        = 0x00010010

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

# Describes an exception.
# https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-exception_record
class EXCEPTION_RECORD(Structure):
    pass

EXCEPTION_RECORD._fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     PVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", UINT_PTR * 15),
    ]

# Describes an exception.
# https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-exception_record
class _EXCEPTION_RECORD(Structure):
    _fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     PVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", UINT_PTR * 15),
    ]

# Contains exception information that can be used by a debugger.
# https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-exception_debug_info
class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord",    EXCEPTION_RECORD),
        ("dwFirstChance",      DWORD),
    ]

class DEBUG_EVENT_UNION(Union):
    _fields_ = [
        ("Exception",         EXCEPTION_DEBUG_INFO),
#        ("CreateThread",      CREATE_THREAD_DEBUG_INFO),
#        ("CreateProcessInfo", CREATE_PROCESS_DEBUG_INFO),
#        ("ExitThread",        EXIT_THREAD_DEBUG_INFO),
#        ("ExitProcess",       EXIT_PROCESS_DEBUG_INFO),
#        ("LoadDll",           LOAD_DLL_DEBUG_INFO),
#        ("UnloadDll",         UNLOAD_DLL_DEBUG_INFO),
#        ("DebugString",       OUTPUT_DEBUG_STRING_INFO),
#        ("RipInfo",           RIP_INFO),
        ]

# Describes a debugging event
# https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-debug_event
class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode", DWORD),
        ("dwProcessId",      DWORD),
        ("dwThreadId",       DWORD),
        ("u",                DEBUG_EVENT_UNION),
    ]


# Used by the CONTEXT structure
class FLOATING_SAVE_AREA(Structure):
    _fields_ = [

        ("ControlWord", DWORD),
        ("StatusWord", DWORD),
        ("TagWord", DWORD),
        ("ErrorOffset", DWORD),
        ("ErrorSelector", DWORD),
        ("DataOffset", DWORD),
        ("DataSelector", DWORD),
        ("RegisterArea", BYTE * 80),
        ("Cr0NpxState", DWORD),
    ]

# Contains processor-specific register data. The system uses CONTEXT structures to perform various internal operations.
# https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-arm64_nt_context
class CONTEXT(Structure):
    _fields_ = [

        ("ContextFlags", DWORD),
        ("Dr0", DWORD),
        ("Dr1", DWORD),
        ("Dr2", DWORD),
        ("Dr3", DWORD),
        ("Dr6", DWORD),
        ("Dr7", DWORD),
        ("FloatSave", FLOATING_SAVE_AREA),
        ("SegGs", DWORD),
        ("SegFs", DWORD),
        ("SegEs", DWORD),
        ("SegDs", DWORD),
        ("Edi", DWORD),
        ("Esi", DWORD),
        ("Ebx", DWORD),
        ("Edx", DWORD),
        ("Ecx", DWORD),
        ("Eax", DWORD),
        ("Ebp", DWORD),
        ("Eip", DWORD),
        ("SegCs", DWORD),
        ("EFlags", DWORD),
        ("Esp", DWORD),
        ("SegSs", DWORD),
        ("ExtendedRegisters", BYTE * 512),
    ]

# Describes an entry from a list of the threads executing in the system when a snapshot was taken.
# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-threadentry32
class THREADENTRY32(Structure):
    _fields_ = [
        ("dwSize",             DWORD),
        ("cntUsage",           DWORD),
        ("th32ThreadID",       DWORD),
        ("th32OwnerProcessID", DWORD),
        ("tpBasePri",          LONG),
        ("tpDeltaPri",         LONG),
        ("dwFlags",            DWORD),
    ]