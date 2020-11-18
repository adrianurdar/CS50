#import <math.h>
#import <cs50.h>
#import <stdio.h>

int main(void)
{
    float change;
    do
    {
        change = get_float("Change: ");
    }
    while (change < 0);
    int amount = round(change * 100);
    int coins = 0;
    while (amount >= 25)
    {
        coins++;
        amount -= 25;
    }
    while (amount >= 10)
    {
        coins++;
        amount -= 10;
    }
    while (amount >= 5)
    {
        coins++;
        amount -= 5;
    }
    while (amount >= 1)
    {
        coins++;
        amount -= 1;
    }
    printf("%i\n", coins);
}
