#include <cs50.h>
#include <stdio.h>

long get_positive_long(string prompt);
int card_length(long card);
int card_prefix(long card);
int product_sum(long card);
int sum_digits(long card);
int total_sum(long card);

int main(void)
{
    long card = get_positive_long("Number: ");
    int length = card_length(card);
    int prefix = card_prefix(card);
    int prod = product_sum(card);
    int sum = sum_digits(card);
    int total = total_sum(card);
    if (total % 10 == 0)
    {
        if (length == 13)
        {
            if ((prefix >= 40) && (prefix <= 49))
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (length == 15)
        {
            if ((prefix == 34) || (prefix == 37))
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (length == 16)
        {
            if ((prefix >= 51) && (prefix <= 55))
            {
                printf("MASTERCARD\n");
            }
            else if ((prefix >= 40) && (prefix <= 49))
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

// Prompt user for card number
long get_positive_long(string prompt)
{
    long n;
    do
    {
        n = get_long("%s", prompt);        
    }
    while (n < 0);
    return n;
}

// Find the length of the card number
int card_length(long card)
{
    int length = 0;
    while (card > 0)
    {
        card /= 10;
        length++;
    }
    return length;
}

// Find if the first 2 digits match card
int card_prefix(long card)
{
    int prefix = 0;
    while (card > 100)
    {
        card /= 10;
    }
    prefix = card;
    return prefix;
}

// Sum of the product of the digits second-to-last
int product_sum(long card)
{
    int prod = 0, check = 0;
    int length = card_length(card) - 1;
    for (int i = 0; i < length; i += 2)
    {
        check = 2 * (((card - (card % 10)) / 10) % 10);
        if (check >= 10)
        {
            check = (check % 10) + ((check - (check % 10)) / 10);
        }
        prod += check;
        card /= 100;
    }
    return prod;
}

// Sum of the digits
int sum_digits(long card)
{
    int sum = 0;
    int length = card_length(card);
    for (int i = 0; i < length; i += 2)
    {
        sum += card % 10;
        card /= 100;
    }
    return sum;
}

// Total modulo 10 is congruent to 0?
int total_sum(long card)
{
    int a = product_sum(card);
    int b = sum_digits(card);
    return a + b;
}
