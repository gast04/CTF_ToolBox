
import z3

a = z3.Int("a")
b = z3.Int("b")

s = z3.Solver()
s.add(a + b > 5, a > 0, b < -5)

# check for satisfiability
print(s.check())
print(s.model())

