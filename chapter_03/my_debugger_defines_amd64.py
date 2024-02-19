#from ctypes import *
from my_debugger_defines import *

CONTEXT_AMD64 = 0x00100000
CONTEXT_CONTROL = (CONTEXT_AMD64 | 0x0001)
CONTEXT_INTEGER = (CONTEXT_AMD64 | 0x0002)
CONTEXT_SEGMENTS = (CONTEXT_AMD64 | 0x0004)
CONTEXT_FLOATING_POINT = (CONTEXT_AMD64 | 0x0008)
CONTEXT_DEBUG_REGISTERS = (CONTEXT_AMD64 | 0x0010)
CONTEXT_FULL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_FLOATING_POINT)
CONTEXT_ALL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_SEGMENTS | CONTEXT_FLOATING_POINT | CONTEXT_DEBUG_REGISTERS)

class M128A(Structure):
    _fields_ = [
        ("Low",  ULONGLONG),
        ("High", ULONGLONG),
    ]

class XMM_SAVE_AREA32(Structure):
    _fields_ = [
        ("ControlWord", WORD),
        ("StatusWord", WORD),
        ("TagWord", BYTE),
        ("Reserved1", BYTE),
        ("ErrorOpcode", WORD),
        ("ErrorOffset", DWORD),
        ("ErrorSelector", WORD),
        ("Reserved2", WORD),
        ("DataOffset", DWORD),
        ("DataSelector", WORD),
        ("Reserved3", WORD),
        ("MxCsr", DWORD),
        ("MxCsr_Mask", DWORD),
        ("FloatRegisters", M128A * 8),
        ("XmmRegisters", M128A * 16),
        ("Reserved4", BYTE * 96),
    ]

class XMM(Structure):
    _fields_ = [
        ("Header", M128A * 2),
        ("Legacy", M128A * 8),
        ("Xmm0", M128A),
        ("Xmm1", M128A),
        ("Xmm2", M128A),
        ("Xmm3", M128A),
        ("Xmm4", M128A),
        ("Xmm5", M128A),
        ("Xmm6", M128A),
        ("Xmm7", M128A),
        ("Xmm8", M128A),
        ("Xmm9", M128A),
        ("Xmm10", M128A),
        ("Xmm11", M128A),
        ("Xmm12", M128A),
        ("Xmm13", M128A),
        ("Xmm14", M128A),
        ("Xmm15", M128A),
    ]

class FLOATING_POINT(Union):
    _fields_ = [
        ("FltSave", XMM_SAVE_AREA32),
        ("XMM", XMM),
    ]


# Contains processor-specific register data. The system uses CONTEXT structures to perform various internal operations.
# Refer to the header file WinNT.h for definitions of this structure for each processor architecture.
# https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context
# https://github.com/Alexpux/mingw-w64/blob/master/mingw-w64-tools/widl/include/winnt.h#L1023
# https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/programmer-references/40332.pdf
class CONTEXT_x64(Structure):
    _fields_ = [
        ("P1Home", DWORD64),
        ("P2Home", DWORD64),
        ("P3Home", DWORD64),
        ("P4Home", DWORD64),
        ("P5Home", DWORD64),
        ("P6Home", DWORD64),

        # Control flags
        ("ContextFlags", DWORD),
        ("MxCsr", DWORD),

        # Segment
        ("SegCs", WORD),
        ("SegDs", WORD),
        ("SegEs", WORD),
        ("SegFs", WORD),
        ("SegGs", WORD),
        ("SegSs", WORD),
        ("EFlags", DWORD),

        # Debug
        ("Dr0", DWORD64),
        ("Dr1", DWORD64),
        ("Dr2", DWORD64),
        ("Dr3", DWORD64),
        ("Dr6", DWORD64),
        ("Dr7", DWORD64),

        # Integer
        ("Rax", DWORD64),
        ("Rcx", DWORD64),
        ("Rdx", DWORD64),
        ("Rbx", DWORD64),
        ("Rsp", DWORD64),
        ("Rbp", DWORD64),
        ("Rsi", DWORD64),
        ("Rdi", DWORD64),
        ("R8",  DWORD64),
        ("R9",  DWORD64),
        ("R10", DWORD64),
        ("R11", DWORD64),
        ("R12", DWORD64),
        ("R13", DWORD64),
        ("R14", DWORD64),
        ("R15", DWORD64),

        # Counter
        ("Rip", DWORD64),

        # Floating Point
        ("FloatingPoint", FLOATING_POINT),

        # Vector
        ("VectorRegister", DWORD64),
        ("VectorControl", DWORD64),

        # Debug control
        ("DebugControl",         DWORD64),
        ("LastBranchToRip",      DWORD64),
        ("LastBranchFromRip",    DWORD64),
        ("LastExceptionToRip",   DWORD64),
        ("LastExceptionFromRip", DWORD64),
    ]
