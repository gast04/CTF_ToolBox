#include<stdio.h>
#include<stdlib.h>

#include <sys/ptrace.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <unistd.h>

#include "hexdump.h"

int main(int argc, char** argv) {

	if(argc < 4) {
		printf("usage: ./prog <pid> <addr> <len>\n");
		return 1;
	}

	// parse args
	off_t addr;
	int pid = atoi(argv[1]);
	int len = atoi(argv[3]);
	sscanf(argv[2], "%lx", &addr);

	if (len >= 4096) {
		printf("max length: 4096\n");
		len = 4096;
	}

	// open memory file from the process where we want to read
	char file[64];
	sprintf(file, "/proc/%ld/mem", (long)pid);
	int fd = open(file, O_RDWR);

	// attach to process using ptrace
	// sends a SIGSTOP to the target process
	ptrace(PTRACE_ATTACH, pid, 0, 0);
	waitpid(pid, NULL, 0);

	char mem[4096];
	// read process Heap
	pread(fd, &mem, sizeof(mem), addr);
	//pwrite(fd, &value, sizeof(value), addr);

	// detach from the target
	ptrace(PTRACE_DETACH, pid, 0, 0);	
	close(fd);	

	hexdump(&mem,len);

	return 0;
}

