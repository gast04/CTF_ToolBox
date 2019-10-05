import idc
import idaapi

def reg(name):
    return idc.get_reg_value(name)

def px_w(addr):
    w = idaapi.get_bytes(addr, 2)[::-1]
    w_int = ord(w[0])<<8 | ord(w[1])
    print(hex(w_int))
    return w_int

def px_dw(addr, p=True):
    dw = idaapi.get_bytes(addr, 4)[::-1]
    dw_int = ord(dw[0]) << 24 | ord(dw[1])<< 16 | ord(dw[2])<<8 | ord(dw[3])
    if p:
        print(hex(dw_int))
    return dw_int

def px_qw(addr):
    dw = idaapi.get_bytes(addr, 8)[::-1]
    dq_int =  ord(dw[0]) << 56 | ord(dw[1]) << 48 | ord(dw[2]) << 40 | ord(dw[3]) << 32 | ord(dw[4]) << 24 | ord(dw[5])<< 16 | ord(dw[6])<<8 | ord(dw[7])
    print(hex(dq_int))
    return dq_int


# TODO: better printing
def hexdump_raw(addr, src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % x for x in chars])
        printable = ''.join(["%s" % ((x <= 127 and FILTER[x]) or '.') for x in chars])
        print("%08x | %-*s | %s" % (addr+c, length*3, hex, printable))

def hexdump(addr, size):
    print_bytes = idaapi.get_bytes(addr, size)
    
    dump = []
    for b in print_bytes:
        dump.append(ord(b))

    hexdump_raw(addr, dump)


