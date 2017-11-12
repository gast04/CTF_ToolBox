
#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) 
{
 
  char *newargv[] = { NULL, "hello", NULL };

  if(argc < 2){
    printf("need program name\n");
    return 0;  
  }

  char* input_line; // = (char*)malloc(200);
  size_t size ;
  getline(&input_line, &size, stdin);
  //printf("line read: %s %d\n", input_line, size);

  /*
  // log readed input  
  FILE* fp; 
  fp = fopen("readed_input.txt", "a");
  fprintf(fp, input_line);
  fclose(fp);
  */

  // TODO: split at spaces here and parse it as multiple arguments

  newargv[1] = input_line;
  newargv[0] = argv[1];
  //printf("start program: %s\n", argv[1]);

  // replaces current process image with the new program
  // that's why we get the crash ;)
  execve(argv[1], newargv, NULL); 

  return 0;
}

