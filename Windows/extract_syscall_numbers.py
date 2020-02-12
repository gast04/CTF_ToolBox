import r2pipe

r2functionprefix = "sym.ntdll.dll_"

r2p = r2pipe.open("ntdll.dll")
r2p.cmd("aaa")
funcs = r2p.cmdj("aflj")

# parse Nt-functions
nt_functions = []
for f in funcs:
  if f['name'].startswith(r2functionprefix+"Nt"):
    nt_functions.append(f)

# get syscall numbers
# mov eax, sysnum ; is at offset 0x3

offsets = {}
for f in nt_functions:
  disas = r2p.cmdj("pdj 1 @ {}".format(f['offset']+0x3))
  try:
    offsets[f['name']] = disas[0]['val']
  except:
    print(f['name'])

# print C-style defines
print("\n")
for o in offsets:
  print("#define {} {}".format(o[len(r2functionprefix):], offsets[o]))


