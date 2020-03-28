#include <windows.h>
#include <winternl.h>
#include <vector>
#include <iostream>
#include <cstring>

#define DEREF_32( name )*(DWORD *)(name)

#define BUFFERSIZE 20000

char ReadBuffer[BUFFERSIZE] = { 0 };
uint8_t* buffer;
uint32_t* code;

int openFile(uint32_t* filesize) {

	HANDLE hFile;
	DWORD  dwBytesRead = 0;
	OVERLAPPED ol = { 0 };

	hFile = CreateFile("C:\\Users\\kurtn\\Desktop\\HelloWorld.exe",               // file to open
		GENERIC_READ,          // open for reading
		FILE_SHARE_READ,       // share for reading
		NULL,                  // default security
		OPEN_EXISTING,         // existing file only
		FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, // normal file
		NULL);                 // no attr. template

	if (hFile == INVALID_HANDLE_VALUE) {
		printf("unable to open file\n"); return -1;
	}

	if (FALSE == ReadFileEx(hFile, ReadBuffer, BUFFERSIZE - 1, &ol, NULL)) {
		printf("Terminal failure: Unable to read from file.\n GetLastError=%08x\n", GetLastError());
		CloseHandle(hFile); return -1;
	}

	// get filesize
 	*filesize = GetFileSize(hFile, NULL);

	printf("DONE reading\n");
	return 0;
}

int main(int argc, char** argv) {
	std::cout << "nyPack Version 1.0\n\n";

	uint32_t filesize = 9216;
	//if (openFile(&filesize) != 0)
	//	return -1;

	/*
	std::vector<unsigned char> const code = {
		0xb8,                   // move the following value to EAX:
		0x05, 0x00, 0x00, 0x00, // 5
		0xc3                    // return what's currently in EAX
	};*/

	// prepare the memory in which the machine code will be put (it's not executable yet):
	buffer = (uint8_t*)VirtualAlloc(nullptr, filesize, MEM_COMMIT, PAGE_READWRITE);
	printf("Buffer Pointer: %p\n", buffer);
	printf("Filesize: %d\n", filesize);

	// assembly code
	//uint32_t code[3] = {0x34120000, 0x35120000, 0x36120000};
	uint8_t* start_buffer = (buffer + filesize);
	//code = (uint32_t*)ReadBuffer;
	//printf("Code Pointer: %p\n", code);

	// no reference to stack variables are allowed here, we moved the stack pointer
  

	// get NT header start
	PIMAGE_NT_HEADERS nt = PIMAGE_NT_HEADERS(PCHAR(buffer) + PIMAGE_DOS_HEADER(buffer)->e_lfanew);
    printf("NT-header-start: %x\n", nt);
	HANDLE handle = GetCurrentProcess();

	// get VA of entry point
	DWORD EntryAddr = nt->OptionalHeader.ImageBase + nt->OptionalHeader.AddressOfEntryPoint;

	// Allocate the space with Imagebase as a desired address allocation request
	PVOID memalloc = VirtualAllocEx(
		handle,
		PVOID(nt->OptionalHeader.ImageBase),
		nt->OptionalHeader.SizeOfImage,
		MEM_RESERVE | MEM_COMMIT,
		PAGE_EXECUTE_READWRITE
	);
	
	// Write headers on the allocated space
	WriteProcessMemory(handle,
		memalloc,
		buffer,
		nt->OptionalHeader.SizeOfHeaders,
		0
	);

	// write sections on the allocated space
	PIMAGE_SECTION_HEADER section = IMAGE_FIRST_SECTION(nt);
	for (ULONG i = 0; i < nt->FileHeader.NumberOfSections; i++) {
		WriteProcessMemory(
			handle,
			PCHAR(memalloc) + section[i].VirtualAddress,
			PCHAR(buffer) + section[i].PointerToRawData,
			section[i].SizeOfRawData,
			0 );
	}

	// read import directory    
	DWORD dwValueB = (DWORD) & (nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]);

	// get the VA 
	DWORD dwValueC = (DWORD)(nt->OptionalHeader.ImageBase) +
		((PIMAGE_DATA_DIRECTORY)dwValueB)->VirtualAddress;

	while (((PIMAGE_IMPORT_DESCRIPTOR)dwValueC)->Name)
	{
		// get DLL name
		LPSTR libname = (LPSTR)(nt->OptionalHeader.ImageBase +
			((PIMAGE_IMPORT_DESCRIPTOR)dwValueC)->Name);

		// Load dll
		HINSTANCE laddress = LoadLibrary(libname);

		// get first thunk, it will become our IAT
		DWORD dwValueA = nt->OptionalHeader.ImageBase +
			((PIMAGE_IMPORT_DESCRIPTOR)dwValueC)->FirstThunk;

		// resolve function addresses
		while (DEREF_32(dwValueA))
		{
			DWORD dwValueD = nt->OptionalHeader.ImageBase + DEREF_32(dwValueA);
			// get function name 
			LPSTR Fname = (LPSTR)((PIMAGE_IMPORT_BY_NAME)dwValueD)->Name;
			// get function addresses
			DEREF_32(dwValueA) = (DWORD)GetProcAddress(laddress, Fname);
			dwValueA += 4;
		}

		dwValueC += sizeof(IMAGE_IMPORT_DESCRIPTOR);
	}

	// call the entry point :: here we assume that everything is ok.
	((void(*)(void))EntryAddr)();
	
	return 0;
}
