import angr
import simuvex

symb = angr.claripy.BVS("input", 10*8)

proj = angr.Project("simple_test")
start = proj.factory.entry_state(args=["simple_test", symb], remove_options={simuvex.o.LAZY_SOLVES})

pg = proj.factory.path_group(start)
pg.explore(find=0x0040069e)

p = pg.found[0].state
print p.se.any_str(symb)

