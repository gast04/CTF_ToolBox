from androguard.misc import AnalyzeAPK
import os, sys

if len(sys.argv) != 2:
    print("Usage: strings.py <APK>")
    sys.exit(-1)

print("analyzing APK...")
a,d,dx = AnalyzeAPK(sys.argv[1])
print("")

# package name
packname = a.get_package().split(".")[-1]

# filter strings, print only if occurs in application not in framework
printable = []
longest_str = 0
for string in dx.strings:
    for _, meth in dx.strings[string].get_xref_from():
        if packname in meth.class_name:
            printable.append([string, meth.class_name, meth.name])
            if len(string) > longest_str:
                longest_str = len(string)

# format output
for p in printable:
    string = p[0].ljust(longest_str, ' ')
    print("{}\t{}\t{}".format(string, p[1], p[2]))
