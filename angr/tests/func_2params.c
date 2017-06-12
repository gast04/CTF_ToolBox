#include <stdio.h>

int func(char* arg1, char* arg2){
  if(arg1[0] == 'a')
  if(arg1[1] == 'b')
  if(arg1[2] == 'c')
  if(arg2[0] == 'c')
  if(arg2[1] == 'b')
  if(arg2[2] == 'a')
    return 1;
  return 0;
}

int main( int argc, char** argv) {

  if(func(argv[1], argv[2]) ){
    printf("success\n");
    return 1;
  }

  printf("nope, sry\n");
  return 0;
}
