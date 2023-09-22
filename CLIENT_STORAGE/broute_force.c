#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int isFinish(char *str)
{
    return '\0' == str[strspn(str, "Z")];
}

void inc_str(char *str)
{
    int index, carry;
    for (index = strlen(str) - 1; index >= 0; --index)
    {
        if (str[index] == 'Z')
        {
            carry = 1;
            str[index] = 'a';
        }
        else if (str[index] == 'z')
        {
            carry = 0;
            str[index] = 'A';
        }
        else
        {
            carry = 0;
            str[index] += 1;
        }
        if (carry == 0)
            break;
    }
}

int main()
{
    int n;
    char *str;
    char pass[] = "asg";

    n = 3; // length
    str = (char *)malloc(sizeof(char) * (n + 1));
    // initialize
    memset(str, 'a', n); //"aa..aa"
    str[n] = '\0';

    while (1)
    {
        printf("%s\n", str);
        if (isFinish(str) || strcmp(pass, str) == 0)
            break;
        inc_str(str);
    }
    free(str);
    return 0;
}