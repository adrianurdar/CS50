#include <cs50.h>
#include <stdio.h>

int get_between_int(string prompt);
void dots(int n);
void spaces(int n);

int main(void)
{
    int h = get_between_int("Height: ");
    for (int i = 0; i < h; i++)
    {
        dots(h-i);
        for (int j = h-i-1; j < h; j++)
        {
            printf("#");
        }
        spaces(2);
        for (int j = h-i-1; j < h; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}

// Prompt user for int between 1 and 8
int get_between_int(string prompt)
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

// Some dots
void dots(int n)
{
    for (int i = 1; i < n; i++)
    {
        printf(" ");
    }
}

// Spaces between the stairs
void spaces(int n)
{
    printf("  ");
}
