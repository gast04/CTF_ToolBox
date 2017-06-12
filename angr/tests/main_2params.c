#include <stdio.h>


int main( int argc, char** argv) {

  if(argv[1][0] == 'a')
  if(argv[1][1] == 'b')
  if(argv[1][2] == 'c')
  if(argv[2][0] == 'c')
  if(argv[2][1] == 'b')
  if(argv[2][2] == 'a')
  if(argv[3][0] == 'b')
  if(argv[3][1] == 'c')
  if(argv[3][2] == 'a'){
    printf("success\n");
    return 1;
  }

  printf("nope, sry\n");


  return 0;
}
