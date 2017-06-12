
#include <stdio.h>
#include <string.h>

void call_me(){
  system("/bin/sh");
}

int func_call(char* name){
  char buf[20];
  strcpy(buf, name);
  printf(buf);
}

int main(int argc, char** argv){

  func_call(argv[1]);

  return 0;
}
