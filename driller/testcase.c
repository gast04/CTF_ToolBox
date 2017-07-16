#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv)
{

  if(argc != 2)
  {
    printf("usage: %s <secret>\n",argv[0]);
    return 1;
  }
  
  // create bufferoverflow on stack
  char arg1[10] = "";
  strncpy(arg1, argv[1],10);
  arg1[9] = '\0';

  printf("argv[1]: %s\n", arg1);
  if (strcmp(arg1, "abcdefghi") == 0)
  {
    fgets(arg1, 100, stdin); // hmmm??
  }       
  else
    printf("nope, try harder");
  
  return 0;
}

