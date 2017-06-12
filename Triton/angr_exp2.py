#!/usr/bin/python2.7

import angr

# load binary
# auto_load_libs: False (to avoid state explotions)
# static loads the binary
proj = angr.Project('./crackme_simple', load_options={"auto_load_libs":False})

# setup a parameter cause we know we need one, and this is the Flag
argv1 = angr.claripy.BVS("argv1", 0xA*8)

# setup initial state for path exploration
initial_state = proj.factory.entry_state(args=["./crackme_simple", argv1])
initial_path = proj.factory.path(initial_state)

# setup path group
pg = proj.factory.path_group(initial_state)

# explore paths
#pg.explore(find=lambda p: "you win!" in p.state.posix.dumps(1))
# maybe its better to look for an address instead of a output, cause I do not
# know in which dump the output will occur. 0x08048488 from r2
pg.explore(find=0x08048488)

if len(pg.found) == 0:
    print "no matching input found"
    exit(0)

fon = pg.found[0]
print "Input:",fon.state.se.any_str(argv1)
