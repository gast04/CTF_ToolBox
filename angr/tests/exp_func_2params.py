#!/usr/bin/python2.7

import angr

proj = angr.Project('./func_2', load_options={"auto_load_libs":False})

argv1 = angr.claripy.BVS("argv1", 8*16)
argv2 = angr.claripy.BVS("argv2", 8*16)

# works if we start from the main function
# now start directly from the function 'func'
# initial_state = proj.factory.entry_state(args=["./func_2", argv1, argv2])


# both will work
#initial_state = proj.factory.entry_state(addr=0x0804840b , args=[ argv1, argv2])
initial_state = proj.factory.call_state( 0x0804840b , argv1, argv2)

''' NOTE:
    the two lines from above will only work if we set the explore find parameter
    to a point inside the calling function or to a subfunction, not outside it,
    because we will never leave the outside function! (see funcInFunc)
'''

pg = proj.factory.path_group(initial_state)


pg.explore(find=0x08048456)

print pg

fon = pg.found[0]
print "Input1:",fon.state.se.any_str(argv1)
print "Input2:",fon.state.se.any_str(argv2)
