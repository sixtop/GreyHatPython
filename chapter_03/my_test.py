import my_debugger

debugger = my_debugger.Debugger()
#pid = input("Enter the PID of the process to attach to:")
#debugger.attach(int(pid))

printf_address = debugger.func_resolve(b'msvcrt.dll', b'printf')

print(f"[*] Address of printf: {printf_address}")

debugger.bp_set(printf_address)
#debugger.run()

#debugger.detach()

