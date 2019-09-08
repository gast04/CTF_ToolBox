#include <stdio.h>
#include <inttypes.h>

#include<windows.h>
#include<winternl.h>

int main(int argc, char** argv) {
    printf("\nMain Start\n");
	
    TEB* teb;// = NtCurrentTeb ();

    // fill thread environment block using inline assembly
    __asm{
        nop
        mov eax, fs:[24]    // fs segment points to Thread Environment Block
        mov ss:[ebp-12], eax   
        nop
    };

    PPEB peb = teb->ProcessEnvironmentBlock;
    
    // to fetch peb is also possible using
    // mov eax, fs:[0x30] 
    
    uint8_t isdbg = peb->BeingDebugged;
    printf("isdbg: %d\n", isdbg);

    /*
    peb->BeingDebugged = 1;
    isdbg = peb->BeingDebugged;
    printf("isdbg: %d\n", isdbg);
    */

    // same Effect as reading the value directly
    if( IsDebuggerPresent())
        printf("Please remove, Debugger\n");

	return 0;
}
