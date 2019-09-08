#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {

  char* b0 = malloc(100);
  char* b1 = malloc(101);
  char* b2 = malloc(102);
  char* b3 = malloc(103);

  free(b0);
  free(b1);
  free(b2);
  free(b3);

  return 0;
}

