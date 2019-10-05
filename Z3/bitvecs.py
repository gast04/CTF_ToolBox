
import z3

a, b = z3.BitVecs('a b', 32)
s = z3.Solver()

s.add(a > 3, b > 1)
# shifts are only possible with BVs
s.add(a == 1 << b)

print(s.check())
print(s.model())

