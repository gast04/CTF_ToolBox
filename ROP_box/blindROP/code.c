// compiled with:
//	gcc -fno-pie -o code code.c

#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
int echo_service(){
    char x[100];
    read(0, x, 500);
    printf("%s", x);
    fflush(stdout);
}
int main(void) {
    while(1) {
        if (fork() == 0) {
            echo_service();
            return 0;
        }
        int status;
        wait(&status);
        if (status != 0) {
            puts("You broke the internet!");
            fflush(stdout);
        }
    }
    return 0;
}

