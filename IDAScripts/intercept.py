import idaapi, idc 
import binascii as ba

'''
	open TODO
'''

mainfunc = 0x400C7D

# set breakpoints
print "setup breakpoints..."
idc.AddBpt(mainfunc)

# start debugger
#print "starting debugger..."
#idc.RunTo(mainfunc)

def delAllBpts():
	while(True):
		bp = idc.GetBptEA(0)
		if bp == 0xffffffffffffffff:
			break
		idc.DelBpt(bp)

	
def singleStep(segfault_addr):

	# add breakpoint on segfault addr
	idc.AddBpt(segfault_addr)
	
	# move debugger	
	idc.GetDebuggerEvent(idc.WFNE_SUSP|idc.WFNE_CONT, -1)
	rip = idc.GetRegValue("RIP")
		
	# now single step through segfault code
	while True:

		# print instruction
		addr = idc.GetRegValue("RIP")	
		disasm = idc.GetDisasm(addr)
		msg = "{}: {}".format(hex(addr), disasm)
	
		# step through loaded code
		idc.StepInto()
		idc.GetDebuggerEvent(idc.WFNE_SUSP, -1)
		
		addr = idc.GetRegValue("RIP")
		if addr < begin or addr > (begin+size):
			break
	
	idc.DelBpt(segfault_addr)
	
	
def modeCode():

	# delete all breakpoints, can cause trouble
	delAllBpts()
	idc.RunTo(mainfunc)
	idc.AddBpt(addr)
