import sys
from pwn import *

context.terminal = ["xfce4-terminal", "--disable-server", "-e"] 
context.arch = "amd64"

if len(sys.argv) > 1 and sys.argv[1] == "REM":
  p = remote("ip", 1234)
else:
  p = process(["sample", "some_arg"])


# set breakpoints (depending on pie or not)
# addr = 0x04006b2
offset = 0x805
#gdb.attach(p, r2cmd="db {}".format(hex(addr)))
gdb.attach(p, r2cmd=".(reldb {})".format(hex(offset)))

# read banner
p.readuntil(b"template\n")

# send payload
print("sending payload")
payload = b"A"*10 + p64(offset)
p.sendline(payload)

# dont close 
p.interactive()
