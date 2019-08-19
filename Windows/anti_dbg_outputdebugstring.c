#include <stdio.h>
#include <inttypes.h>

#include<windows.h>
#include<winternl.h>


int main(int argc, char** argv) {
    printf("\nMain Start\n");
	
    uint16_t errorValue = 1234;
    SetLastError(errorValue);

    OutputDebugStringA("Debugger Test\x00");

    printf("%d\n", GetLastError());

    if( GetLastError() == errorValue)
        printf("Debugger Detected\n");
    else
        printf("no debugger\n");

	return 0;
}
