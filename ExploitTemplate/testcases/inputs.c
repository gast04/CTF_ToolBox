#include<stdio.h>

void callme(){
  system("/bin/sh");
}

int main(int argc, char** argv) {
  char buffer[64];

  printf("Hello to my template\n");

  if (argc < 2) {
    printf("usage: %s <name>\n", argv[0]);
    return -1;
  }

  gets(buffer);
  return 0;
}

