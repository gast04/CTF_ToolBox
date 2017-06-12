#!/usr/bin/python2.7

import angr

# load the binary
# auto_load_libs: False (to avoid state explotions)
proj = angr.Project("./crackme_simple", load_options={'auto_load_libs':False})

# create the binary pathgroup
pg = proj.factory.path_group()

# step through all paths
while len(pg.active) > 0:
    pg.step()be

# print length of all deadended paths
print "path lengths:"
i = 0
for dead in pg.deadended:
    print "path:{0} - {1}".format(i, dead.length)
    i +=1

# we know we need the longest path, it will contain the most constraints
path  = pg.deadended[0]
for dead in pg.deadended:
    if(path.length < dead.length):
        path = dead

#optional way (TODO)
#pg.explore(find=lambda p: "you win!" in p.state.posix.dumps(1))

# now analyse the constraints
print "Constraints of longest path:"
print('\n'.join('{}: {}'.format(*con) for con in enumerate(path.state.se.constraints)))

# we could now revert the constraints and look for the matching input
# via : chr((0x31^0x55)+1)  # for the first constraint

# unfortunately I couldn't find anything, because the flag is the input and not
# printed, we can print state dumps: path.state.posix.dumps(0)
# but this will only print output dumps.
# see to angr_exp2.py for a better solution
