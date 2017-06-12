#include <stdio.h>
#include <string.h>

int evaluate_password(char* pwd);

int func_a(int a){
  printf("func_a: %d\n", a);
  return 1;
}

int func_b(int b){
  printf("func_b: %d\n", b);
  return 2;
}

void start_here(char* pwd){
  printf("your password is: %s\n", pwd);
  if (evaluate_password(pwd) == 1){
    printf("Succes-thats was the correct pwd!\nhave fun ;)\n");
    system("/bin/sh");
  }
  else
    printf("wrong password\n");
}

int main( int argc, char** argv){

  if(1)
    printf("just wait a bit, binary is almost ready :)\n");

  while(1){}
}

int evaluate_password(char* pwd){

  // length check
  if(strlen(pwd) != 16)
    return 0;

  // super secure password check
  if( (((size_t)pwd[0]*0x556677%101010)^0x113344) == 1169306)
  if( (((size_t)pwd[1]*0x556677%101010)^0x113344) == 1055963)
  if( (((size_t)pwd[2]*0x556677%101010)^0x113344) == 1051836)
  if( (((size_t)pwd[3]*0x556677%101010)^0x113344) == 1140027)
  if( (((size_t)pwd[4]*0x556677%101010)^0x113344) == 1095347)
  if( (((size_t)pwd[5]*0x556677%101010)^0x113344) == 1133929)
  if( (((size_t)pwd[6]*0x556677%101010)^0x113344) == 1133929)
  if( (((size_t)pwd[7]*0x556677%101010)^0x113344) == 1078704)
  if( (((size_t)pwd[8]*0x556677%101010)^0x113344) == 1154963)
  if( (((size_t)pwd[9]*0x556677%101010)^0x113344) == 1133929)
  if( (((size_t)pwd[10]*0x556677%101010)^0x113344) == 1172898)
  if( (((size_t)pwd[11]*0x556677%101010)^0x113344) == 1070306)
  if( (((size_t)pwd[12]*0x556677%101010)^0x113344) == 1074185)
  if( (((size_t)pwd[13]*0x556677%101010)^0x113344) == 1070306)
  if( (((size_t)pwd[14]*0x556677%101010)^0x113344) == 1123935)
  if( (((size_t)pwd[15]*0x556677%101010)^0x113344) == 1129819)
    return 1;

  return 0;
}
