#include <stdio.h>

int funcAdd(int a, int b){
  return a+b;
}


int main( int argc, char** argv){

  int a = atoi(argv[1]);
  int b = atoi(argv[2]);

  if( 9 == funcAdd(a, b))
    printf("success\n");
  else
    printf("fail\n");

  return 0;
}
