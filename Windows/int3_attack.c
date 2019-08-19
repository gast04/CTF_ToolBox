#include <stdio.h>
#include <inttypes.h>

#include<windows.h>
#include<winternl.h>

/*
    cl /c int3_attack.c
    link int3_attack.obj /SAFESEH:NO
*/

int main(int argc, char** argv) {
    printf("\nMain Start\n");
	
    int checker = 1;

    // fill thread environment block using inline assembly
    __asm{
        nop
        push offset cont
        push fs:[0]
        mov fs:[0], esp   
        int 3
        xor ebx, ebx
        jmp offset end
        cont:
        mov eax, ss:[ebp-4]
        mov eax, 0x1234
        mov ss:[ebp-4], eax
        jmp offset end
        end:
        nop
    };

    printf("checker: 0x%x\n", checker);

    printf("Return From Main\n");
    exit(0); // if not, takes ages to exit the program, 
    // I guess its because of the unsafe SEH handler
	return 0;
}
