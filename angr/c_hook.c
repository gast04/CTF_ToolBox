#include <stdio.h>

int func_a(int a){
  printf("%d\n",a);
  return 42;
}

int main(){
  func_a(10);
  return 0;
}
