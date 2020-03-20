import binascii as ba
import fuckpy3

class FunctionData():
    def __init__(self, raw: bytes):
        tmp = raw.split(b"\t")

        if len(tmp) != 5:
            return None
        try:
            self.methodID = int(tmp[-5],16)
            self.classname = tmp[-4]
            self.functionname = tmp[-3]
            self.signature = tmp[-2]
            self.sourcefile = tmp[-1]
        except:
            print("FunctionData: Could not parse: {}".format(raw))
            return None

    def __str__(self):
        return "{}: {} -> {}".format(hex(self.methodID), self.classname.decode("UTF-8"), self.functionname.decode("UTF-8"))

class ThreadData():
    def __init__(self, raw: bytes):
        tmp = raw.split(b"\t")

        if len(tmp) != 2:
            return None

        self.threadID = int(tmp[-2])
        self.threadname = tmp[-1].strip()
        
    def __str__(self):
        return "{}: {}".format(hex(self.threadID), self.threadname.decode("UTF-8"))

class EventData():
    def __init__(self, raw: bytes):
        
        if len(raw) != 14:
            return None

        # Structure
        # 2 byte thread ID
        # 4 byte method ID
        # 4 byte time delta
        # 4 byte wall clock delta
       
        self.threadID = int(ba.hexlify(raw[:2][::-1]),16)
        self.methodID = int(ba.hexlify(raw[2:6][::-1]),16)
        self.timedelta = int(ba.hexlify(raw[6:10][::-1]),16)
        self.wallclockdelta = int(ba.hexlify(raw[10:14][::-1]),16)
        
        # 0x0 method enter
        # 0x1 method exit
        # 0x2 unwind
        self.action = self.methodID & 0x3
        self.methodID = self.methodID & 0xFFFFFFFC

    def __str__(self):
        if self.action == 0x0:
            return "{} -> {} : Enter".format(hex(self.threadID), hex(self.methodID))
        elif self.action == 0x1:
            return "{} -> {} : Leave".format(hex(self.threadID), hex(self.methodID))
        else:
            return "{} -> {} : {}".format(hex(self.threadID), hex(self.methodID), self.action)


# single call
FILENAME = "cpu-art-20200320T160541.trace"

# double call
FILENAME = "cpu-art-20200320T160945.trace"

# 8 times
FILENAME = "cpu-art-20200320T144656.trace"

# 14 times
FILENAME = "cpu-art-20200320T152020.trace"



f1 = open(FILENAME, "rb")
content = f1.readlines()
f1.close()


# rudimentary parsing of functions
print("parse functions")
all_funcs = []
for line in content:
    if b'\x000x' in line:
        tmp = b'0x' + line.split(b'\x000x')[-1]
        func_data = FunctionData(tmp)
        if func_data is not None:
            all_funcs.append(func_data)


# verify functions (some have errors, TODO: check)
funcs = {}
for f in all_funcs:
    try:
        funcs[f.methodID] = f
    except:
        pass


# parse of thread numbers (assume at most 100 threads)
print("parse threads")
threads = []
collect = False
for line in content[-100:]:
    if b"*methods" in line:
        collect = False

    if collect:
        threads.append(ThreadData(line))
    
    if b"*threads" in line:
        collect = True


# parse timing data
print("parse timing events")
for t in threads:
    if b"main" == t.threadname:
        main_tid = t.threadID
        break

main_bytes = (chr(main_tid & 0xff) + chr(main_tid >> 8 & 0xff)).bytes()

# read file new, since readlines migth have destroyed data
f1 = open(FILENAME, "rb")
content = f1.read()
f1.close()

events = []
i = 0
while True:
    if main_bytes == content[i:i+2]:

        event = EventData(content[i:i+14])
        if event is None:
            i += 1
            continue

        # check if function ID matches a found function
        if event.methodID not in funcs.keys():
            i += 1
            continue

        # parsing succeeded
        events.append(event)
        i += 14
    else:
        i += 1

    if i > len(content):
        break


# extract intressting functions
watch_funcs = []
for f in funcs: 
    if b"nativedebugging" in funcs[f].classname: 
        watch_funcs.append(funcs[f])


wf_counts = {}
for wf in watch_funcs:
    for e in events:
        if e.methodID == wf.methodID:
            print("{}: {}".format(wf.functionname.decode("UTF-8"), e))

            if e.action == 0:
                try:
                    wf_counts[wf] += 1
                except:
                    wf_counts[wf] = 1

