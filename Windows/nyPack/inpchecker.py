import binascii
import z3

s = z3.Solver()

arg0 = z3.BitVec("a0", 32)
arg1 = z3.BitVec("a1", 32)
arg2 = z3.BitVec("a2", 32)
arg3 = z3.BitVec("a3", 32)

s.add((arg0 ^ arg1) - 0xbca086ef == 0x58838718)
s.add((arg2 ^ arg3) + 0xfbf01328 == 0x2f1a8c58)
s.add(arg1 * arg2 == 0x6808b34a)
s.add(arg0 * arg3 == 0xc428d21)

s.check()
print(s.model())
