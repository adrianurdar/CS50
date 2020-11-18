#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        string s = 0;
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (argv[1][i] >= '0' && argv[1][i] <= '9')
            {

            }
            else
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        int k = atoi(argv[1]);
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    string p = get_string("plaintext: ");
    int z = 0;
    int k = atoi(argv[1]);
    printf("ciphertext: ");    
    for (int i = 0, l = strlen(p); i < l; i++)
    {
        if (p[i] >= 'a' && p[i] <= 'z')
        {
            z = ((((int) p[i] + k - 97) % 26) + 97);
            printf("%c", z);
        }
        else if (p[i] >= 'A' && p[i] <= 'Z')
        {
            z = ((((int) p[i] + k - 65) % 26) + 65);
            printf("%c", z);
        }
        else
        {
            printf("%c", p[i]);
        }
    }
    printf("\n");
}
