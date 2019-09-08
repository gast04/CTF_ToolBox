
from pwn import *

messash = "Hello World"

# creating a binary using pwntools
context.clear(arch='i386')
assembly =  'read:'      + shellcraft.read(constants.STDIN_FILENO, 'esp', 1024)
assembly += 'sigreturn:' + shellcraft.sigreturn()
assembly += 'int3:'      + shellcraft.trap()
assembly += 'syscall: '  + shellcraft.syscall()
assembly += 'exit: '     + 'xor ebx, ebx; mov eax, 1; int 0x80;'
assembly += 'messash:'  + ('.asciz "%s"' % messash)
binary = ELF.from_assembly(assembly)

print "binary created:"
print binary.path

