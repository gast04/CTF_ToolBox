#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <unistd.h>

int main(int argc, char** argv) {

  if (argc < 2) {
		printf("usage: ./prog <secret text>\n");
		return 1;
	}

	// allocate memory and copy
	char* buffer = (char*)malloc(strlen(argv[1]));
	memcpy(buffer, argv[1], strlen(argv[1]));
	printf("%s\n", buffer);
	
  // keep the program alive
  while(1){
    sleep(1);
  }

  return 0;         
}

