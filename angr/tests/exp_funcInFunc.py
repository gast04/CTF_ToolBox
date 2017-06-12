#!/usr/bin/python2.7

import angr

proj = angr.Project('./funcInFunc', load_options={"auto_load_libs":False})

argv1 = angr.claripy.BVS("argv1", 8*16)
argv2 = angr.claripy.BVS("argv2", 8*16)
argv3 = angr.claripy.BVS("argv3", 8*4)

# works if we start from the main function
# now start directly from the function 'func'
# initial_state = proj.factory.entry_state(args=["./func_2", argv1, argv2])

# start by func
initial_state = proj.factory.call_state( 0x0804843c , argv1, argv3, argv2)

pg = proj.factory.path_group(initial_state)

pg.explore(find=0x0804841a)

print pg

fon = pg.found[0]
print "Input1:",fon.state.se.any_str(argv1)
print "Input2:",fon.state.se.any_str(argv2)
print "Input3:",fon.state.se.any_int(argv3)
