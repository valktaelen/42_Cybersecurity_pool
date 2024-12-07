#include <sys/types.h>
#include <stdio.h>
#include <string.h>
#define PASSWORD "__stack_check"


int main(void)
{
    int     iVar1;
    char    pass [14];
    char    input [100];

    *((int32_t*)(pass + 0)) = *((int32_t *)(PASSWORD + 0));
    *((int32_t*)(pass + 4)) = *((int32_t *)(PASSWORD + 4));
    *((int32_t*)(pass + 8)) = *((int32_t *)(PASSWORD + 8));
    *((int16_t*)(pass + 12)) = *((int16_t*)(PASSWORD + 12));
    printf("Please enter key: ");
    scanf("%s",input);
    if (strcmp(input,pass) == 0) {
        printf("Good job.\n");
    }
    else {
        printf("Nope.\n");
    }
    return 0;
}
