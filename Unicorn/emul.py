import r2pipe, array, unicorn, capstone

'''
r2p = r2pipe.open("sample")
addr = 0x68d
byte_len = 48 
'''

r2p = r2pipe.open("sample2")
addr = 0x68d
byte_len = 74

code = r2p.cmdj("p8j {} @ {}".format(byte_len, addr)) # get bytes from r2
cap_code = array.array('B', code).tostring()

print("Code to Simulate:")
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for i in md.disasm(cap_code, addr):
    print(hex(i.address), "".join("{:02x}".format(x) for x in i.bytes), i.mnemonic, i.op_str)
print("")

ADDRESS = 0x10000

mu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
mu.mem_map(ADDRESS, 2*1024*2014)

# setup stack base pointer
mu.reg_write(unicorn.x86_const.UC_X86_REG_RBP, ADDRESS*2)

# setup parameter
print("set both parameters")
mu.reg_write(unicorn.x86_const.UC_X86_REG_EAX, 1234) # second param

# first param (0x10 -> sample, 0x8 -> sample2)
#mu.mem_write(ADDRESS*2 - 0x10, b"\xd2\x04")
mu.mem_write(ADDRESS*2 - 0x8, b"\x0b\x0c\x00\x00") # 3083 -> 0x0C0B
#mu.mem_write(ADDRESS*2 - 0x8, b"\x63\x00") #   99 -> 0x0063

# write code
mu.mem_write(ADDRESS, cap_code)

# start emulation
mu.emu_start(ADDRESS, ADDRESS+len(cap_code))

# final result
print("Result:", mu.reg_read(unicorn.x86_const.UC_X86_REG_EAX))

