import binascii, random
from pwn import *

f = open("kdctf.exe","rb")
binf = f.read()
f.close()
f = open("push_code.txt", "w+")

prolog = """__asm {
  nop
  push eax
  push edx
  mov edx, esp
  mov esp, start_buffer	
  nop
"""

# push directly on stack
prolog = """__asm {
  nop
  nop
"""

epilog = """
  nop
  mov esp, edx
  pop edx
  pop eax
  nop
};
"""

# push directly on stack
epilog = """
  mov buffer, esp
  nop
  nop
};
"""

push_tmp = "  push {}"

add_tmp = """  push {}
  add dword ptr [esp],{}"""

xor_tmp = """  push {}
  xor dword ptr [esp],{}"""

push0_tmp = """  xor eax, eax
  head{}:
    push 0x0
    inc eax
    cmp eax,{}
    jne head{}
"""

# get PE_header_offset and start from it
# e_lfanew -> offset 60:64

tmpval = int(binascii.hexlify(binf[60:64]),16)
e_lfanew = int(binascii.hexlify(p32(tmpval)), 16)
print("e_lfanew: {}".format(hex(e_lfanew)))

push0_ops = 0
p0_enter = False
p0_cnt = 0

f.write(prolog + "\n")
for i in range(len(binf), e_lfanew,-4):
  #try:
    # convert to int
    tmpval = int(binascii.hexlify(binf[i-4:i]),16)

    # convert to little endian
    tmpval = int(binascii.hexlify(p32(tmpval)), 16)

    if p0_enter and tmpval != 0:
      # leave p0 state
      p0_enter = False

      if p0_cnt >= 6:
        # apply optimization
        f.write(push0_tmp.format(push0_ops, p0_cnt, push0_ops))
      else:
        # dont apply optimization
        for i in range(p0_cnt):
          f.write(push_tmp.format(hex(0)) + "\n")

      p0_cnt = 0
      push0_ops += 1

    if tmpval == 0:
      # enter p0 state
      p0_enter = True
      p0_cnt += 1
      continue

    add_ob = random.randint(0,1)

    rand_add = random.randint(0x10000, 0x80000000)

    # write
    if tmpval >= rand_add:
      if add_ob:
        f.write(add_tmp.format(hex(tmpval-rand_add),hex(rand_add)) + "\n")
      else:
        f.write(xor_tmp.format(hex(tmpval^rand_add),hex(rand_add)) + "\n")
    else:
      f.write(push_tmp.format(hex(tmpval)) + "\n")

  #except:
  #  print("ERROR:" + str(binf[i-4:i]))

f.write(epilog + "\n")
f.close()


'''
TODO: 
* add anti-debug stuff in the unpacker
* add block randomization
'''
