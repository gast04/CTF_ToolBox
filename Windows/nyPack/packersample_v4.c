/*
Credits:
https://stackoverflow.com/questions/40936534/how-to-alloc-a-executable-memory-buffer
https://securityxploded.com/memory-execution-of-executable.php
*/

#include <windows.h>
#include <winternl.h>
#include <vector>
#include <iostream>
#include <cstring>

#define DEREF_32(name)*(DWORD *)(name)
#define DEBUG 0

// make all variables public to avoid using the stack, since we are destroying it
uint8_t* buffer;
uint32_t i;

PIMAGE_NT_HEADERS nt;
HANDLE handle;
DWORD EntryAddr;
PVOID memalloc;
PIMAGE_SECTION_HEADER section;
HINSTANCE laddress;
DWORD dwValueA, dwValueB, dwValueC, dwValueD;
LPSTR Fname;


// TODO: get these variables by packer
#define e_lfanew 264
#define filesize 105472-e_lfanew // remove DOS header

int main(int argc, char** argv) {
	std::cout << "nyPack Version 1.0\n\n";

	// no reference to stack variables are allowed here, we moved the stack pointer
  // static ASMCODE

	// get NT header start
	//PIMAGE_NT_HEADERS nt = PIMAGE_NT_HEADERS(PCHAR(buffer) + PIMAGE_DOS_HEADER(buffer)->e_lfanew);

  // trim binary to start at NT-Header
  nt = PIMAGE_NT_HEADERS(buffer);
  handle = GetCurrentProcess();

	// get VA of entry point
	EntryAddr = nt->OptionalHeader.ImageBase + nt->OptionalHeader.AddressOfEntryPoint;
    //if (DEBUG) printf("EntryPoint:%p\n", EntryAddr);
    //if (DEBUG) printf("Imagebase: %p\n", nt->OptionalHeader.ImageBase);
    //if (DEBUG) printf("Imagesize: %p\n", nt->OptionalHeader.SizeOfImage);

	// Allocate the space with Imagebase as a desired address allocation request
	memalloc = VirtualAllocEx(handle,
		PVOID(nt->OptionalHeader.ImageBase),
		nt->OptionalHeader.SizeOfImage,
		MEM_RESERVE | MEM_COMMIT,
		PAGE_EXECUTE_READWRITE);
	
	// write sections on the allocated space
    // printf("Num Sections: %d\n", nt->FileHeader.NumberOfSections);
	section = IMAGE_FIRST_SECTION(nt);
	for (i = 0; i < nt->FileHeader.NumberOfSections; i++) {
        memcpy(PCHAR(memalloc) + section[i].VirtualAddress,
               PCHAR(buffer) - e_lfanew + section[i].PointerToRawData, // remove DOS part
               section[i].SizeOfRawData);
	}

	// read import directory
	dwValueB = (DWORD) & (nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]);

	// get the VA
    dwValueC = (DWORD)(nt->OptionalHeader.ImageBase) + ((PIMAGE_DATA_DIRECTORY)dwValueB)->VirtualAddress;

	// Load Kernel32.dll, onlyone needed for static binaries
	laddress = LoadLibrary("KERNEL32.dll");

	// get first thunk, it will become our IAT
	dwValueA = nt->OptionalHeader.ImageBase + ((PIMAGE_IMPORT_DESCRIPTOR)dwValueC)->FirstThunk;

	// resolve all function addresses from Kernel32.dll
	while (DEREF_32(dwValueA)) {
		dwValueD = nt->OptionalHeader.ImageBase + DEREF_32(dwValueA);
			
        // get function name 
		Fname = (LPSTR)((PIMAGE_IMPORT_BY_NAME)dwValueD)->Name;

		// get function addresses
		DEREF_32(dwValueA) = (DWORD)GetProcAddress(laddress, Fname);
		dwValueA += 4;
	}
	dwValueC += sizeof(IMAGE_IMPORT_DESCRIPTOR);
	
	// call entry, give execution to new Binary
	((void(*)(void))EntryAddr)();
	
	return 0;
}
