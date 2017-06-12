

#Create a 32-bit symbolic bitvector "x": `claripy.BVS('x', 32)`

# we could also set constraints for bytes or for argv1
argv1 = angr.claripy.BVS("argv1", input_size * 8)

# restrict bytes
for byte in argv1.chop(8):
    initial_state.add_constraints(byte != '\x00') # null
    initial_state.add_constraints(byte >= ' ') # '\x20'
    initial_state.add_constraints(byte <= '~') # '\x7e'


# set first letters to know Flag start
initial_state.add_constraints(argv1.chop(8)[0] == 'C')
initial_state.add_constraints(argv1.chop(8)[1] == 'T')
initial_state.add_constraints(argv1.chop(8)[2] == 'F')
initial_state.add_constraints(argv1.chop(8)[3] == '{')


state.add_constraints(argv[1].get_byte(0) >= argv[1].get_byte(1))
state.add_constraints(argv[1].get_byte(0) ^ argv[1].get_byte(1) == 0x1f)
state.add_constraints(argv[1].get_byte(4) <= argv[1].get_byte(5))
state.add_constraints(argv[1].get_byte(4) ^ argv[1].get_byte(5) == 0x67)
state.add_constraints(argv[1].get_byte(8) >= argv[1].get_byte(9))

# If you want to prevent appending the ID and size to the name, you can, instead, do:
v = s.se.BVS("some_name", 32, explicit_name=True)


def memory_store_str(st, addr, s, size=None, *args, **kwargs):
    """store "string" BV in memory, getting endianess right"""
    if 'endness' in kwargs:
        del kwargs['endness']
    st.memory.store(addr, s, size=size, endness='Iend_BE',
                    *args, **kwargs)

def memory_store_int(st, addr, i, size=None, *args, **kwargs):
    """store integer in memory, getting endianess right"""
    if 'endness' in kwargs:
        del kwargs['endness']
    st.memory.store(addr, i, size=size, endness=st.arch.memory_endness,
                    *args, **kwargs)


# with .concrete you can check if the memory address in angr
# is symbolic or not
# if you do not setu up a memory region, and angr access it
# it will automatically define it as symbolic, and if it is
# handled as a pointer, it will define an arbitrary pointer

print start_state.memory.load(0xffc65040, 4, endness='Iend_LE')
print start_state.memory.load(0xffc65040+4, 4, endness='Iend_LE')
print start_state.memory.load(0xffc65040+8, 4, endness='Iend_LE')

print start_state.memory.load(0xffc65040, 4, endness='Iend_LE').concrete
print start_state.memory.load(0xffc65040+4, 4, endness='Iend_LE').concrete
print start_state.memory.load(0xffc65040+8, 4, endness='Iend_LE').concrete


print start_state.memory.load(0xffc650d4, 4, endness='Iend_LE') # [ebx+4]
print start_state.memory.load(0xffc650e0, 4, endness='Iend_LE') # [ebx+8]

print start_state.memory.load(0xffc650d4, 4, endness='Iend_LE').concrete # [ebx+4]
print start_state.memory.load(0xffc650e0, 4, endness='Iend_LE').concrete # [ebx+8]



argv = angr.claripy.BVS("argv", 32)
proj = angr.Project("mycrack")
entry_state = proj.factory.entry_state()

entry_state.regs.eax = argv
entry_state.regs.eax.concrete

eax_symbolic = entry_state.regs.eax.get_bytes(0,3)
entry_state.add_constraints(eax_symbolic > 0x1234)


#!/usr/bin/env python
import angr, simuvex

def main():
    b = angr.Project("very_success", load_options={"auto_load_libs":False})
    # create a state at the checking function
    # Since this is a windows binary we have to start after the windows library calls
    # remove lazy solves since we don't want to explore unsatisfiable paths
    s = b.factory.blank_state(addr=0x401084, remove_options={simuvex.o.LAZY_SOLVES})
    # set up the arguments on the stack
    s.memory.store(s.regs.esp+12, s.se.BVV(40, s.arch.bits))
    s.mem[s.regs.esp+8:].dword = 0x402159
    s.mem[s.regs.esp+4:].dword = 0x4010e4
    s.mem[s.regs.esp:].dword = 0x401064
    # store a symbolic string for the input
    s.memory.store(0x402159, s.se.BVS("ans", 8*40))
    # explore for success state, avoiding failure
    pg = b.factory.path_group(s, immutable=False)
    pg.explore(find=0x40106b, avoid=0x401072)
    # print the string
    found_state = pg.found[0].state
    return found_state.se.any_str(found_state.memory.load(0x402159, 40)).strip('\0')

def test():
    assert main() == 'a_Little_b1t_harder_plez@flare-on.com'

if __name__ == '__main__':
    print main()
