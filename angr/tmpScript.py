#!/usr/bin/env python2.7

import angr
import json
import simuvex

def loadMemory( blank_state ):
    try:
        mem_file = open("memoryContent.txt", "r")
    except IOError:
        print "could not find memoryContent.txt..."
        exit(0)

    memory_json = json.load(mem_file)   # loads file as json object

    # load stack memory
    stack_content = memory_json['stack']
    for address in stack_content:
        blank_state.memory.store(int(address), int(stack_content[address]), endness=blank_state.arch.memory_endness)

    if len(memory_json) > 1:
        # load heap memory, if there is one used
        heap_content = memory_json['heap']
        for address in heap_content:
            blank_state.memory.store(int(address), int(stack_content[address]), endness=blank_state.arch.memory_endness)
    
def assert_checkEAX(state):
    if not state.se.any_int(state.regs.eax) >= 0x4:
        print "Assert checkEAX failed..."

# create angr project and blank_state, maybe you have to edit the path
proj = angr.Project("/home/niku/Documents/CTFs_H4XXOR/Code_Snippets/angr/mycrack", load_options={"auto_load_libs":False})
blank_state = proj.factory.blank_state(remove_options={simuvex.o.LAZY_SOLVES})

# set register values
blank_state.regs.eip=0x804844a
blank_state.regs.esp=0xffe3cbe0
blank_state.regs.ebp=0xffe3cbe8
blank_state.regs.esi=0x2
blank_state.regs.edi=0xf7697000
blank_state.regs.eax=0xf7698d9c
blank_state.regs.ebx=0x0
blank_state.regs.ecx=0xffe3cc00
blank_state.regs.edx=0xffe3cc24

# setup blank_state memory 
loadMemory( blank_state )

# set up symbolic memory
blank_state.memory.store(0xffe3e268, blank_state.se.BVS('userinput', 7*8, explicit_name=True))
'''
# in case if you want to limit the values for the bitvector
# chop(8) splits bitvector into pieces of 8 bits
for byte in symb_var.chop(8):
    blank_state.add_constraints(angr.claripy.Or(byte >= ' ', byte == 0x00)) # 0x20
    blank_state.add_constraints(byte <= '~') # 0x7e

# add hard constraints
blank_state.add_constraints(symb_var.chop(8)[0] == 'F')
blank_state.add_constraints(symb_var.chop(8)[1] == 'L')
blank_state.add_constraints(symb_var.chop(8)[2] == 'A')
blank_state.add_constraints(symb_var.chop(8)[3] == 'G')
'''

# setup hooks in project

# setup assert hooks in project
proj.hook(0x8048471, assert_checkEAX, length=0)

# setup path groups and start exploration
pg = proj.factory.path_group(blank_state)
pg.explore(find=0x80484e8, avoid=[0x80484f2])

# print soltion if we found a path
if len(pg.found) > 0:
    foundstate = pg.found[0].state
    concrete_memory = foundstate.memory.load(0xffe3e268, 7) # userinput
    print foundstate.se.any_str(concrete_memory)
