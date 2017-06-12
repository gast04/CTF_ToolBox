#include <stdio.h>

void func2(int res){
  if(res == 1)
    printf("success\n");
  else
    printf("fail\n");
}

int func(char* arg1, int b,  char* arg2){

  int a = 0;
  if(arg1[0] == 'a' && b == 17)
  if(arg1[1] == 'b')
  if(arg1[2] == 'c')
  if(arg2[0] == 'c')
  if(arg2[1] == 'b')
  if(arg2[2] == 'a')
    a = 1;

  func2(a);
  return a;
}

int main( int argc, char** argv) {

  if(func(argv[1], argv[2], 0) ){
    //printf("success\n");
    return 1;
  }

  //printf("nope, sry\n");
  return 0;
}
