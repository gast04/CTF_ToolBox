#include <stdio.h>
#include <inttypes.h>

#include<windows.h>
#include<winternl.h>

int main(int argc, char** argv) {
    printf("\nMain Start\n");
    void* somemalloc = malloc(1234);
	
    uint32_t someval;

    // fill variable using inline assembly
    __asm{
        nop
        mov eax, fs:[48]
        mov eax, [eax+24]
        mov eax, [eax+16]
        mov ss:[ebp-16], eax
        nop
    };
    
    printf("isdbg: %d\n", someval);


    // we have to extract the ForceFlags field from the ProcessHeap struct
    TEB* teb = NtCurrentTeb ();
    uint32_t* peb = teb->ProcessEnvironmentBlock;
    uint32_t* procheap = *(peb+0x18);
    printf("procheap: %d\n", *(procheap+0x44));

    // I tried several things but, none of them really seemed to work...
    // assuming this is not a thing anymore

	return 0;
}
