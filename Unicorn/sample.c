
#include <stdlib.h>
#include <stdio.h>


int main(int argc, char** argv) 
{
  
  int a = atoi(argv[1]);
  int b = atoi(argv[2]);

  int c = a*1234;
  int d = b*4321;
  
  d = a+d;
  c = b+c;

  d = d+c;

  printf("%d\n", d);

  return 0;
}

