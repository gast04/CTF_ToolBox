#!/usr/bin/python2.7

from triton     import *
from triton.ast import *

# content of the check function
# got from r2: pdf @ sym.check

# I changed some memory locations and instructions

function = {
   #sym.check (int arg_8h)#
       # var int local_4h @ ebp-0x4
       # arg int arg_8h @ ebp+0x8
    0x0804840b:      "\x55",                            # push ebp
    0x0804840c:      "\x89\xe5",                        # ebp = esp
    0x0804840e:      "\x83\xec\x10",                    # esp -= 0x10
    0x08048411:      "\xc7\x45\xfc\x00\x00\x00\x00",    # dword [ebp - local_4h] = 0
    0x08048418:      "\xeb\x36",                        # goto 0x8048450
    0x0804841a:      "\x8b\x55\xfc",                    # edx = dword [ebp - local_4h] # ebx
    0x0804841d:      "\x8b\x45\x08",                    # eax = dword [ebp + arg_8h]   # [0x8:4]=0 # ebx
    0x08048420:      "\x01\xd0",                        # eax += edx
    0x08048422:      "\x0f\xb6\x00",                    # eax = byte [eax]
    0x08048425:      "\x0f\xbe\xc0",                    # eax = al
    0x08048428:      "\x83\xe8\x01",                    # eax -= 1
    0x0804842b:      "\x83\xf0\x55",                    # eax ^= 0x55
    0x0804842e:      "\x89\xc1",                        # ecx = eax
    0x08048430:      "\x8b\x15\x1c\xa0\x04\x08",        # edx = dword [obj.serial]    # [0x804a01c:4]=0x8048540 edx
                                                        # LEA obj.serial
                                                        # "@...GCC: (GNU) 6.1.1 20160802" @ 0x804a01c # "1>=&1" edx
                                                        # mov edx, dword ptr [0x804a01c]
    0x08048436:      "\x8b\x45\xfc",                    # eax = dword [ebp - local_4h] # ebx
    0x08048439:      "\x01\xd0",                        # eax += edx
    0x0804843b:      "\x0f\xb6\x00",                    # eax = byte [eax]
    0x0804843e:      "\x0f\xbe\xc0",                    # eax = al
    0x08048441:      "\x39\xc1",                        # if (ecx == eax
    0x08048443:      "\x74\x07",                        # isZero 0x804844c)          # unlikely#
    0x08048445:      "\xb8\x01\x00\x00\x00",            # eax = 1
    0x0804844a:      "\xeb\x0f",                        # goto 0x804845b
    0x0804844c:      "\x83\x45\xfc\x01",                # dword [ebp - local_4h] += 1
    # JMP XREF from 0x08048418 (sym.check)
    0x08048450:      "\x83\x7d\xfc\x04",                # if (dword [ebp - local_4h] == 4 # [0x4:4]=0x10101
    0x08048454:      "\x7e\xc4",                        # isLessOrEqual 0x804841a)   # unlikely
    0x08048456:      "\xb8\x00\x00\x00\x00",            # eax = 0
    # JMP XREF from 0x0804844a (sym.check)
    0x0804845b:      "\x5d",                            # ebx # esp
    0x0804845c:      "\xc3",                            # ebx
}

def initContext():
    # set serial pointer to memory location
    setConcreteMemoryValue(0x0804a01c, 0x00)
    setConcreteMemoryValue(0x0804a01d, 0x00)
    setConcreteMemoryValue(0x0804a01e, 0x90)

    # fill memory location with data
    setConcreteMemoryValue(0x900000, 0x31)
    setConcreteMemoryValue(0x900001, 0x3e)
    setConcreteMemoryValue(0x900002, 0x3d)
    setConcreteMemoryValue(0x900003, 0x26)
    setConcreteMemoryValue(0x900004, 0x31)

    # set stack parameter, the pointer we can control
    # we can only set one byte at the time so we need 4 writes for one paramter
    # (note: we have a push so we only need to add 4 to the base pointer from beyond!)
    setConcreteMemoryValue(0x7ffff103, 0x00)
    setConcreteMemoryValue(0x7ffff104, 0x10)
    setConcreteMemoryValue(0x7ffff105, 0x00)
    setConcreteMemoryValue(0x7ffff106, 0x00)

    # same as above
    #setConcreteMemoryAreaValue(0x7ffff103, [0x00,0x10])

    # Setup stack on an abitrary address.
    setConcreteRegisterValue(Register(REG.ESP, 0x7ffff0ff))
    setConcreteRegisterValue(Register(REG.EBP, 0x7ffff0ff))


# This function emulates the code.
def run(ip):
    while ip in function:

        # Build an instruction - template
        inst = Instruction()

        # Setup opcodes, in instruction template
        inst.setOpcodes(function[ip])

        # Setup Address
        inst.setAddress(ip)

        # Process everything
        processing(inst)

        # print assembler instruction
        #print inst

        # Next instruction
        ip = buildSymbolicRegister(REG.EIP).evaluate()

    return

# This function returns a set of new inputs based on the last trace.
def getNewInput():
    # Set of new inputs
    inputs = list()

    # Get path constraints from the last execution
    pco = getPathConstraints()

    # We start with any input. T (Top)
    previousConstraints = equal(bvtrue(), bvtrue())

    # Go through the path constraints
    for pc in pco:
        # If there is a condition
        if pc.isMultipleBranches():
            # Get all branches
            branches = pc.getBranchConstraints()
            for branch in branches:
                # Get the constraint of the branch which has been not taken
                if branch['isTaken'] == False:
                    # Ask for a model
                    models = getModel(assert_(land(previousConstraints, branch['constraint'])))
                    seed   = dict()
                    for k, v in models.items():
                        # Get the symbolic variable assigned to the model
                        symVar = getSymbolicVariableFromId(k)
                        # Save the new input as seed.
                        seed.update({symVar.getKindValue(): v.getValue()})
                    if seed:
                        inputs.append(seed)

        # Update the previous constraints with true branch to keep a good path.
        previousConstraints = land(previousConstraints, pc.getTakenPathConstraintAst())

    # Clear the path constraints to be clean at the next execution.
    clearPathConstraints()

    return inputs

def symbolizeInputs(seed):
    # Clean symbolic state
    concretizeAllRegister()
    concretizeAllMemory()
    for address, value in seed.items():
        convertMemoryToSymbolicVariable(MemoryAccess(address, CPUSIZE.BYTE, value))
        convertMemoryToSymbolicVariable(MemoryAccess(address+1, CPUSIZE.BYTE))
    return


if __name__ == '__main__':

    # Set the architecture
    setArchitecture(ARCH.X86)

    # Symbolic optimization
    #triton.enableMode(triton.MODE.ALIGNED_MEMORY, True)


    # Define entry point
    ENTRY = 0x0804840b

    # We start the execution with a random value located at 0x1000.
    lastInput = list()
    worklist  = list([{0x1000:1}])

    savelist = worklist
    inj_seed = 1
    while worklist:
        # Take the first seed
        seed = worklist[0]

        if inj_seed % 2 == 0:
            savelist = list(worklist)

        inj_seed += 1

        #print 'Seed injected:', seed

        # Symbolize inputs
        symbolizeInputs(seed)

        # Init context memory
        initContext()

        # Emulate
        run(ENTRY)

        lastInput += [dict(seed)]
        del worklist[0]

        #print "get new Input: "
        newInputs = getNewInput()
        for inputs in newInputs:
            if inputs not in lastInput and inputs not in worklist:
                worklist += [dict(inputs)]


    print "finished analyzing"


    # print worklist as hex characters

    print "Found Solution:"
    for i in range(len(savelist[0])):
        # weird print cause it is a dictionary in a list...
        print "",hex(dict(savelist[0])[0x1000+i]),"",chr(dict(savelist[0])[0x1000+i])
