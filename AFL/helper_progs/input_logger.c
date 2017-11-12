#include<stdlib.h>
#include<stdio.h>

int main(int argc, char** argv) {

  // simple write argv[1] to afl_in.txt 
  // to see what fuzzer puts into binary
  FILE* fp;
  fp = fopen("afl_in.txt", "a");
 
  if (argc == 1){
    fprintf(fp, "argc == 1");
    fprintf(fp, "\n");
    fclose(fp);
    return 0;
  }

  fprintf(fp, argv[1]);
  fprintf(fp, "\n");
  fclose(fp);
  
  // crash if the first byte is 0x00 
  // or if the 5th is 0xff
  if(argv[1][0] == 0x00 || argv[1][4] == 0xff)
  {
    unsigned char invalid_read = *(unsigned char*)0x00000000;
  }     

  return 0;
}

