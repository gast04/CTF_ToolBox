#include <stdio.h>
#include <inttypes.h>
#include "windefines.h"

// x86_64-w64-mingw32-gcc -O1 -masm=intel -o WinSys.exe AssemblyWinSyscall_O1.c

//uint64_t* SyscallInline(uint64_t syscallnum, uint64_t param1, uint64_t param2, uint64_t param3, uint64_t param4) __attribute__((always_inline));

// #define VIRTUAL_ALLOC 0x18

//#define PAGE_READWRITE 0x4
//#define PAGE_EXECUTE_READWRITE 0x40

uint64_t* SyscallInline(uint64_t syscallnum, uint64_t param1, 
  uint64_t param2, uint64_t param3, uint64_t param4) {
  
  // Virtual Alloc in assembly
  asm(
    // rcx, arg1
    // rdx, arg2
    // r8,  arg3
    // r9,  arg4
    // [rbp+0x30], arg5

    "mov r10, [rsp + 0x28];"  // move param5 to r10
    "mov rax, rcx;"   // setup syscall number

    "sub rsp, 0x58;"

    "mov qword ptr ss:[rsp+0x48], rdx;"  // param1
    "mov qword ptr ss:[rsp+0x50], r8;"   // param2 
    "mov qword ptr ss:[rsp+0x28], r9;"   // param3
    "mov qword ptr ss:[rsp+0x30], r10;"  // param4

    "lea r9, qword ptr [rsp+0x50];"
    "xor r8d,r8d;"
    "lea rdx, qword ptr [rsp+0x48];"
    "lea rcx, qword ptr [r8-1];"
    "mov r10, rcx;"
    "syscall;"
    "mov rax, qword ptr[rsp+0x48];"         // result
    "add rsp,0x58;"
  );
}


uint64_t* VirtualAllocInline(uint64_t address, uint64_t size, uint64_t alloctype, uint64_t protect) {
  SyscallInline(NtAllocateVirtualMemory, address, size, alloctype, protect);
}

/*
uint64_t* VirtualAllocInline(uint64_t address, 
  uint64_t size, uint64_t alloctype, uint64_t protect) {
  
  // Virtual Alloc in assembly
  asm(
    // rcx, arg1
    // rdx, arg2
    // r8,  arg3
    // r9,  arg4

    "sub rsp, 0x58;"

    "mov qword ptr ss:[rsp+0x48], rcx;"  // param1
    "mov qword ptr ss:[rsp+0x50], rdx;"  // param2 
    "mov qword ptr ss:[rsp+0x28], r8;"   // param3
    "mov qword ptr ss:[rsp+0x30], r9;"   // param4

    "lea r9, qword ptr [rsp+0x50];"
    "xor r8d,r8d;"
    "lea rdx, qword ptr [rsp+0x48];"
    "lea rcx, qword ptr [r8-1];"
    "mov r10, rcx;"
    "mov eax, 0x18;"
    "syscall;"
    "mov rax, qword ptr[rsp+0x48];"         // result
    "add rsp,0x58;"
  );
}
*/

int main() {
  printf("hello windows syscalls\n");

  /*
  LPVOID address2 = VirtualAlloc((LPVOID)0x0, 1024, MEM_RESERVE |MEM_COMMIT, PAGE_READWRITE);
  printf("Address: %p\n",address2);
  */

  uint64_t* address0 = SyscallInline(NtAllocateVirtualMemory, 0x0,4096,0x3000,4);
  printf("Address: %p\n",address0);

  uint64_t* address1 = VirtualAllocInline(0x0,4096,0x3000,4);
  printf("Address: %p\n",address1);

  printf("end program\n");
  return 0;
}

