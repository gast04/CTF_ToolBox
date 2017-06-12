#!/usr/bin/python2.7

import angr

proj = angr.Project('./main_2', load_options={"auto_load_libs":False})

argv1 = angr.claripy.BVS("argv1", 8*16)
argv2 = angr.claripy.BVS("argv2", 8*16)
argv3 = angr.claripy.BVS("argv2", 8*16)

initial_state = proj.factory.entry_state(args=["./main_2", argv1, argv2, argv3])

pg = proj.factory.path_group(initial_state)

pg.explore(find=0x080484ce)

if len(pg.found) == 0:
    print "no matching input found"
    exit(0)

fon = pg.found[0]
print "Input1:",fon.state.se.any_str(argv1)
print "Input2:",fon.state.se.any_str(argv2)
print "Input3:",fon.state.se.any_str(argv3)
