#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int shift(char c);

int main(int argc, string argv[])
{
    // Check if argv exists
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    
    string key = argv[1];
    int key_len = strlen(argv[1]);
    
    // Check if argv[1] is valid
    for (int i = 0; i < key_len; i++)
    {
        if (isdigit(key[i]))
        {
            printf("Usage: ./vigenere keyword\n");
            return 1;
        }
    }

    int i, j;    
    string plaintext = get_string("plaintext: ");
    int plaintext_len = strlen(plaintext);
    
    // Encrypt
    printf("ciphertext: ");
    for (i = 0, j = 0; i < plaintext_len; i++, j++)
    {
        // Loop key
        if (j >= key_len)
        {
            j = 0;
        }
        
        // Skip key if char doesn't need to be encrypted
        if (!isalpha(plaintext[i]))
        {
            j = j-1;
        }
        
        // Print encrypted char
        if (islower(plaintext[i]))
        {
            int c = ((((int) plaintext[i] + shift(key[j]) - 97) % 26) + 97);
            printf("%c", c);
        }
        else if (isupper(plaintext[i]))
        {
            int c = ((((int) plaintext[i] + shift(key[j]) - 65) % 26) + 65);
            printf("%c", c);
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}

// Getting the shift value
int shift(char c)
{
    int k = 0;
    if (isupper(c))
    {
        k = (int) c - 65;
    }
    else if (islower(c))
    {
        k = (int) c - 97;
    }
    return k;
}
