import my_debugger

debugger = my_debugger.Debugger()
pid = input ("Enter the PID of the process to attach to:")
debugger.attach(int(pid))

t_list = debugger.enumerate_threads()

for thread in t_list:
    thread_context = debugger.get_thread_context(thread)
    print(f"[*] Dumping registers for thread ID {thread}")
    print (f"[**] Rip: {hex(thread_context.Rip)}")

debugger.detach()

