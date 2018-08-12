
#include<stdlib.h>
#include<stdio.h>
#include<unistd.h>

int loopCode(int time, char* string)
{
  printf(string);
  sleep(time);
  return time;
}

int main(int argc, char** argv) 
{

  char* string = "hello world\n";

  for(int i = 0; i < 20; i ++)
  {
    printf("%d\n", loopCode(2, string));
  }
  return 0;
}

