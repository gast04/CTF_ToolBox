
#include <iostream>
#include <Windows.h>
#include <psapi.h>
#include <tchar.h>

using namespace std;

string targetModule = "CheatOnMe.exe";

void hexdump(char* ptr, int buflen) {
    unsigned char* buf = (unsigned char*)ptr;
    int i, j;
    for (i = 0; i < buflen; i += 16) {
        printf("%06x: ", i);
        for (j = 0; j < 16; j++)
            if (i + j < buflen)
                printf("%02x ", buf[i + j]);
            else
                printf("   ");
        printf(" ");
        for (j = 0; j < 16; j++)
            if (i + j < buflen)
                printf("%c", isprint(buf[i + j]) ? buf[i + j] : '.');
        printf("\n");
    }
}

int main(int argc, char** argv) {
    cout << "Starting enumeration..." << endl;

    // open handle to remote process
    HANDLE process_hdl = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ | PROCESS_VM_WRITE, FALSE, 2336);

    // EnumProcessModules
    DWORD cbNeeded;
    HMODULE modules[1024];
    if (!EnumProcessModules(process_hdl, modules, 1024, &cbNeeded)) {
        cout << "Error during ernumeration" << endl;
        return -1;
    }

    int mod_id = 0;
    for (; mod_id < (cbNeeded / sizeof(HMODULE)); mod_id++)
    {   
        TCHAR szModName[MAX_PATH];
        if (GetModuleFileNameEx(process_hdl, modules[mod_id], szModName,
            sizeof(szModName) / sizeof(TCHAR))) {
            _tprintf(TEXT("\t%s (0x%08X)\n"), szModName, modules[mod_id]);
        }

        // only analyse if name contains "Cheater.exe" -> binary name
        wstring tmp(&szModName[0]);
        string modname(tmp.begin(), tmp.end());

        // stop after target program was found
        if (modname.find(targetModule) != -1) {
            break;
        }
    }

    MODULEINFO modinfo;
    GetModuleInformation(process_hdl, modules[mod_id], &modinfo, sizeof(modinfo));
    _tprintf(TEXT("\tBase: 0x%08X, Size: 0x%08X\n"), modinfo.lpBaseOfDll, modinfo.SizeOfImage);

    char mem_buffer[4096];
    SIZE_T readbytes;
    if (!ReadProcessMemory(process_hdl, modinfo.lpBaseOfDll, mem_buffer, sizeof(mem_buffer), &readbytes)) {
        cout << "Could not read remote memory" << endl;
        return -1;
    }
    // hexdump(mem_buffer, 4096);

    PIMAGE_NT_HEADERS nt = PIMAGE_NT_HEADERS(PCHAR(mem_buffer) + PIMAGE_DOS_HEADER(mem_buffer)->e_lfanew);
    DWORD sectionLocation = (DWORD)nt
        + sizeof(DWORD) + (DWORD)(sizeof(IMAGE_FILE_HEADER))
        + (DWORD)nt->FileHeader.SizeOfOptionalHeader;
    PIMAGE_SECTION_HEADER sectionHeader = (PIMAGE_SECTION_HEADER)sectionLocation;

    // find data section, we know that, for this simple example
    int section_count = 0;
    while (true) {

        if (sectionHeader[section_count].Name[0] == 0)
            break;

        if (strncmp((const char*)sectionHeader[section_count].Name, ".data", 5) == 0) {
            break;
        }
        // cout << section_count << " | SectionName: " << hex << sectionHeader[section_count].Name << endl;
        section_count++;
    }

    char* data_sec = (char*)((DWORD)modinfo.lpBaseOfDll + sectionHeader[section_count].VirtualAddress);

    // read bytes from data section
    memset(mem_buffer, 0, 4096);
    readbytes = 0;
    if (!ReadProcessMemory(process_hdl, data_sec, mem_buffer, 256, &readbytes)) {
        cout << "Could not read remote memory" << endl;
        return -1;
    }
    hexdump(mem_buffer, 256);

    // first byte in data section is the value we want to change
    char write_buffer[1] = { 0x31 };
    SIZE_T written_bytes;
    if (!WriteProcessMemory(process_hdl, data_sec, write_buffer, 1, &written_bytes)) {
        cout << "Could not write remote memory" << endl;
        return -1;
    }

    return 0;
}

// testing code
// start reading and printing the memory
    //HANDLE process_hdl = GetCurrentProcess();
    //hexdump((char*)modinfo.lpBaseOfDll, modinfo.SizeOfImage);
    /*
    char* binary = (char*)modinfo.lpBaseOfDll;
    PIMAGE_NT_HEADERS nt = PIMAGE_NT_HEADERS(PCHAR(binary) + PIMAGE_DOS_HEADER(binary)->e_lfanew);

    nt->OptionalHeader.SizeOfHeaders;

    DWORD codebase = nt->OptionalHeader.BaseOfCode;
    DWORD database = nt->OptionalHeader.BaseOfData;
    DWORD imagebase = nt->OptionalHeader.ImageBase;
    DWORD sectionalignment = nt->OptionalHeader.SectionAlignment;
    DWORD headerssize = nt->OptionalHeader.SizeOfHeaders;

    DWORD size = nt->OptionalHeader.DataDirectory->Size;
    IMAGE_DATA_DIRECTORY* datadir = nt->OptionalHeader.DataDirectory;

    DWORD sectionLocation = (DWORD)nt
        + sizeof(DWORD) + (DWORD)(sizeof(IMAGE_FILE_HEADER))
        + (DWORD)nt->FileHeader.SizeOfOptionalHeader;
    PIMAGE_SECTION_HEADER sectionHeader = (PIMAGE_SECTION_HEADER)sectionLocation;

    // find data section
    int section_count = 0;
    while (true) {

        if (sectionHeader[section_count].Name[0] == 0)
            break;

        if (strncmp((const char*)sectionHeader[section_count].Name, ".data", 5) == 0) {
            break;
        }
        cout << section_count << " | SectionName: " << hex << sectionHeader[section_count].Name << endl;
        section_count++;
    }

    cout << "\tVirtualAddress: " << hex << sectionHeader[section_count].VirtualAddress << endl;
    //cout << "\tSizeOfRawData : " << hex << sectionHeader[section_count].SizeOfRawData << endl;

    char* data_sec = binary + sectionHeader[section_count].VirtualAddress;

    // search virtual address space for specific value
    //hexdump((char*)sectionHeader[section_count].VirtualAddress, sectionHeader[section_count].SizeOfRawData);
    hexdump(data_sec, 256);
    data_sec[0] = 0x11;

    cout << changeme << endl;
    */