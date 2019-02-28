import unicorn

X86_CODE32 = b"\x41\x4a"
ADRESS = 0x1000000

mu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)

# map 2MB on ADRESS, and write code on it
mu.mem_map(ADRESS, 2*1024*1024)
mu.mem_write(ADRESS, X86_CODE32)

# set register values
mu.reg_write(unicorn.x86_const.UC_X86_REG_ECX, 0x1234)
mu.reg_write(unicorn.x86_const.UC_X86_REG_EDX, 0x7890)

# start emulation, and emulate until code length
mu.emu_start(ADRESS, ADRESS + len(X86_CODE32))
print("Emulation done. Below is the CPU context")

# read result values
r_ecx = mu.reg_read(unicorn.x86_const.UC_X86_REG_ECX)
r_edx = mu.reg_read(unicorn.x86_const.UC_X86_REG_EDX)

print(">>> ECX = 0x%x" %r_ecx)
print(">>> EDX = 0x%x" %r_edx)

