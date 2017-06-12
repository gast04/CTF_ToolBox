
import angr
import simuvex

def hook_func(state, testvar):
    print "function called: {0}".format(testvar)
    print "current state informations"
    print "{0}".format(state.regs.eax.args)

def hook_call(state, testvar):
    print "call instruction: {0}".format(testvar)

def hook_ret(state):
    print "{0}".format(state.regs.eax.args)

binary = "hookme"
proj = angr.Project(binary)

init_state = proj.factory.entry_state(args=[binary])


def make_hook(run):

    def hook(state):

        for item in run:
            print item
            print "run = something else: {0}".format(item)

    return hook

tmp_list = [1,2,3,4,5]

proj.hook(0x0804840b, hook_func, length=0)  # hook at function call of func_a, overwrite nothing
proj.hook(0x08048441, make_hook(tmp_list), length=0)  # hook at call instruction, patch it out
proj.hook(0x08048446, hook_ret, length=0)

pg = proj.factory.path_group(init_state)
pg.explore()
print pg
