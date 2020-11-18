#include <cs50.h>
#include <stdio.h>

int get_positive_int(string prompt);
void dots(int n);

int main(void)
{
    int h = get_positive_int("Height: ");
    for (int i = 0; i < h; i++)
    {
        dots(h-i);
        for (int j = h-i-1; j < h; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}

// Prompt user for integer between 1 and 8 inclusive
int get_positive_int(string prompt)
{
    int h;
    do
    {
        do
        {
            h = get_int("%s", prompt);            
        }
        while (h > 8);
    }
    while (h < 1);
    return h;
}

// Dots a number of times
void dots(int n)
{
    for (int i = 1; i < n; i++)
    {
        printf(" ");
    }
}
