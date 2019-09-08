#include <stdio.h>
#include <inttypes.h>

#include<windows.h>
#include<winternl.h>

int main(int argc, char** argv) {
    printf("Main Start\n");
	
    __asm{
        nop
        mov eax, 1
        cpuid
        nop
    };

    printf("Main End\n");
	return 0;
}
