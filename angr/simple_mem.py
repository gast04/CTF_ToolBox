
import angr

proj = angr.Project("testcases/mycrack")

start_state = proj.factory.blank_state()

# setup ip, where we want to start
start_state.ip = 0x0804848f

# create 8 bit symbolic value
sym_8bit = angr.claripy.BVS("eax", 8)

# set the al (low eax) to symbolic value
start_state.regs.al = sym_8bit

sym_16byte = angr.claripy.BVS("input", 16*8)
start_state.mem.set(0xff830512, sym_16byte)

pg = proj.factory.path_group(start_state)

# just a small explore trace through the jmp
pg.explore(find=0x08048493, avoid=0x80484f2)

state_found = pg.found[0].state

# get value of al
concrete_al = state_found.se.any_int(sym_8bit)
print "al:",hex(concrete_al)
