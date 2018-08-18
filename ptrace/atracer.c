#include<stdio.h>
#include<stdlib.h>

#include <sys/uio.h>
#include <bits/uio-ext.h>

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

	char mem[4096];

	// define local space
	struct iovec liov;
	liov.iov_base = mem;
	liov.iov_len = 4096;

	// define target process space
	struct iovec riov;
	riov.iov_base = (void*)addr;
	riov.iov_len = len;

	// read from target process
	process_vm_readv(pid, &liov, 1, &riov, 1, 0);
	// here we dont need to attach to a process and interrupt it
	// (still we have to deactivate yama, of course)

	hexdump(&mem,len);
	return 0;
}

