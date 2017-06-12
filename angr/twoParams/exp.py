#!/usr/bin/python2.7

import angr


# funcAdd: 0x0804843b
# goal:    0x080484ab

# load binary
# auto_load_libs: False
proj = angr.Project('./hacklet', load_options={"auto_load_libs":False})

# setup a parameter cause we know we need one, and this is the Flag
arg1 = angr.claripy.BVS("argv1", 3*8)
arg2 = angr.claripy.BVS("argv2", 3*8)

# setup initial state for path exploration
initial_state = proj.factory.entry_state( args=[ './hacklet', arg1, arg2])

# constraint input, all charackters are printable
'''
for byte in argv1.chop(8):
    initial_state.add_constraints(byte >= ' ') # '\x20'
    initial_state.add_constraints(byte <= '~') # '\x7e'

initial_state.add_constraints(argv1.chop(8)[0] == 'F')
initial_state.add_constraints(argv1.chop(8)[1] == 'u')
initial_state.add_constraints(argv1.chop(8)[2] == 'z')
initial_state.add_constraints(argv1.chop(8)[3] == '{')
'''

initial_path = proj.factory.path(initial_state)

# setup path group
pg = proj.factory.path_group(initial_state)

pg.explore(find=0x080484a3)

print "pg:", pg
