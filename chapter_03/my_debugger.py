from ctypes import *
from my_debugger_defines import *
from my_debugger_defines_amd64 import *

kernel32 = windll.kernel32

class Debugger():
    def __init__(self):
        self.h_process = None
        self.h_thread = None
        self.pid = None
        self.context = None
        self.debugger_active = None
        self.exception = None
        self.exception_address = None

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

        # https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa
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

            # Obtain a valid handle and store for future access
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            # https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror
            print(f"[*] Error: {kernel32.GetLastError()}")

    def open_process(self, pid):
        # https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)

        # attempt to attach to process
        # https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-debugactiveprocess
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
        else:
            print(f"[*] Unable to attach to the process: {kernel32.GetLastError()}")

    def run(self):
        # poll for events
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        # https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-waitfordebugevent
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):

            # Obtain thread and context info
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context = self.get_thread_context(self.h_thread)

            print(f"Event code: {debug_event.dwDebugEventCode}, thread ID: {debug_event.dwThreadId}")

            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                # Obtain exception code
                exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address = debug_event.u.Exception.ExceptionRecord.ExceptionAddress

                if exception == EXCEPTION_ACCESS_VIOLATION:
                    print("Access violation detected.")
                elif exception == EXCEPTION_BREAKPOINT:
                    # handle breakpoint
                    continue_status = self.exception_handler_breakpoint()

                elif exception == EXCEPTION_GUARD_PAGE:
                    print("Guard page access detected.")
                elif exception == EXCEPTION_SINGLE_STEP:
                    print("Single stepping.")

            # input("Press a key to continue...")
            # self.debugger_active = False

            # https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent
            kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, continue_status)

    def exception_handler_breakpoint(self):
        print(f"[*] Inside the breakpoint handler. Exception address: {hex(self.exception_address)}")
        return DBG_CONTINUE

    def detach(self):

        # https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-debugactiveprocessstop
        if kernel32.DebugActiveProcessStop(self.pid):
            print(f"[*] Finished debugging. Exiting...")
            return True
        else:
            print(f"[*] There was an error")
            return False

    def open_thread(self, thread_id):
        # https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openthread
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)

        if h_thread is not None:
            return h_thread
        else:
            print("[*] Could not obtain a valid thread handle.")
            return False

    def enumerate_threads(self):
        thread_entry = THREADENTRY32()

        thread_list = []

        # https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if snapshot is not None:
            # set size of struct otherwise it'll fail
            thread_entry.dwSize = sizeof(thread_entry)

            # https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-thread32first
            success = kernel32.Thread32First(snapshot, byref(thread_entry))
            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)

                # https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-thread32next
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))

            # https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False

    def get_thread_context(self, thread_id):
        # context = CONTEXT() # 32 bit arch
        # context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        context = CONTEXT_x64() # 64 bit arch
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        # Obtain a handle to the thread
        h_thread = self.open_thread(thread_id)

        # https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadcontext
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False