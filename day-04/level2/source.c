#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>

void ok(void)
{
    puts("Good job.");
    return;
}

void no(void)
{
    puts("Nope.");
    exit(1);
}

int main(void)
{
    size_t      len;
    int         char_value;
    int8_t      end_loop;
    char        atoi_str [4];
    char        input [24];
    char        buf [9];
    u_int32_t   i_input;
    int         i_buf;

    printf("Please enter key: ");
    if (scanf("%23s",input) != 1) {
        no();
    }
    if (input[1] != '0') {
        no();
    }
    if (input[0] != '0') {
        no();
    }
    fflush(stdin);
    memset(buf,0,9);
    buf[0] = 'd';
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
    char_value = strcmp(buf,"delabere");
    if (char_value == 0) {
        ok();
    }
    else {
        no();
    }
    return 0;
}
