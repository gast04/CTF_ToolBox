/*
  a simple crackme to play with triton
  (based on the triton example)
*/

#include <stdio.h>

char *serial = "\x31\x3e\x3d\x26\x31";

int check(char *ptr)
{
  int i = 0;
  while (i < 5){
    if (((ptr[i] - 1) ^ 0x55) != serial[i])
      return 1;
    i++;
  }
  return 0;
}

int main( int argc, char** argv) {

  if( check(argv[1]) == 0)
    printf("you win!\n");
  else
    printf("nope, not today\n");

  return 0;
}
