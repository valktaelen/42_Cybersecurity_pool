#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>

void ___syscall_malloc(void)
{
    puts("Nope.");
    exit(1);
}

void ____syscall_malloc(void)
{
  puts("Good job.");
  return;
}


long main(void)

{
    int char_value;
    size_t len;
    u_int8_t end_loop;
    char atoi_str [4];
    char input [31];
    char buf [9];
    size_t i_input;
    int cmp_ret;
    int i_buf;

    printf("Please enter key: ");
    if (scanf("%23s", input) != 1) {
        ___syscall_malloc();
    }
    if (input[1] != '2') {
        ___syscall_malloc();
    }
    if (input[0] != '4') {
        ___syscall_malloc();
    }
    fflush(stdin);
    memset(buf,0,9);
    buf[0] = '*';
    atoi_str[3] = '\0';
    i_input = 2;
    i_buf = 1;
    while( 1 ) {
        len = strlen(buf);
        end_loop = 0;
        if (len < 8) {
            len = strlen(input);
            end_loop = i_input < len;
        }
        if (!end_loop) break;
        atoi_str[0] = input[i_input];
        atoi_str[1] = input[i_input + 1];
        atoi_str[2] = input[i_input + 2];
        char_value = atoi(atoi_str);
        buf[i_buf] = (char)char_value;
        i_input = i_input + 3;
        i_buf = i_buf + 1;
    }
    buf[i_buf] = '\0';
    cmp_ret = strcmp(buf,"********");
    if (cmp_ret == -2) {
        ___syscall_malloc();
    }
    else if (cmp_ret == -1) {
        ___syscall_malloc();
    }
    else if (cmp_ret == 0) {
        ____syscall_malloc();
    }
    else if (cmp_ret == 1) {
        ___syscall_malloc();
    }
    else if (cmp_ret == 2) {
        ___syscall_malloc();
    }
    else if (cmp_ret == 3) {
        ___syscall_malloc();
    }
    else if (cmp_ret == 4) {
        ___syscall_malloc();
    }
    else if (cmp_ret == 5) {
        ___syscall_malloc();
    }
    else if (cmp_ret == 0x73) {
        ___syscall_malloc();
    }
    else {
        ___syscall_malloc();
    }
    return 0;
}
