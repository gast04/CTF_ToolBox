#include <stdio.h>
#include <inttypes.h>

#include<windows.h>
#include<winternl.h>

int main(int argc, char** argv) {
    printf("\nMain Start\n");
	
    __asm{
        nop
        
        nop
    };

    printf("Please remove, Debugger\n");
	return 0;
}
