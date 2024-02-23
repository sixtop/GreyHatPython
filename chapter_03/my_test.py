import my_debugger

debugger = my_debugger.Debugger()
pid = input ("Enter the PID of the process to attach to:")
debugger.attach(int(pid))
debugger.run()

t_list = debugger.enumerate_threads()
for thread in t_list:
    thread_context = debugger.get_thread_context(thread)
    print(f"[*] Dumping registers for thread ID {thread}")
    print(f"[**] Rip: {hex(thread_context.Rip)}")
    print(f"[**] Rax: {hex(thread_context.Rax)}")
    print(f"[**] Rbx: {hex(thread_context.Rbx)}")
    print(f"[**] Rcx: {hex(thread_context.Rcx)}")
    print(f"[**] Rdx: {hex(thread_context.Rdx)}")
    print(f"[**] Rsp: {hex(thread_context.Rsp)}")
    print(f"[**] Rbp: {hex(thread_context.Rbp)}")
    print(f"[**] Rsi: {hex(thread_context.Rsi)}")
    print(f"[**] Rdi: {hex(thread_context.Rdi)}")



debugger.detach()

