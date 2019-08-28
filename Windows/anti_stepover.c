#include <stdio.h>
#include <inttypes.h>

#include<windows.h>
#include<winternl.h>

int main(int argc, char** argv) {
    printf("\nMain Start\n");
	
    uint32_t debugger_detected = 0;

    __asm{
        nop
        xor ecx, ecx
        push ecx
        add ecx, 4
        mov edi, esp
        mov esi, offset l1
        rep movsb
        l1: cmp [esp], 0xCC
        jne l2  
        add ss:[ebp-4],1
        l2:
        or ss:[ebp-4],0
        pop eax
        nop
    };

    printf("debugger_detected: %d\n", debugger_detected);
	return 0;
}
// apply the copy process in an unpacking process by copying the binary
// to a mapped region, using rep mov** we will copy breakpoints and
// can handle it when we run the copied code during unpacking

/*
    Version 1
    __asm{
        nop
        xor ecx, ecx
        push ecx
        inc ecx
        inc ecx
        mov edi, esp
        mov esi, offset l1
        rep movsb
        l1: pop eax
        cmp al, 0xCC
        jne l2  
        add ss:[ebp-4],1
        l2:
        or ss:[ebp-4],0
    };
*/
