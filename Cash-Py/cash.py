# Cash - greedy algorithm

from cs50 import get_float


def main():
    change = get_positive_float("Change owed: ")
    coins = 0
    amount = round(change * 100)

    # If change >= 0.25
    while amount >= 25:
        coins += 1
        amount -= 25

    # If change >= 0.10
    while amount >= 10:
        coins += 1
        amount -= 10

    # If change >= 0.05
    while amount >= 5:
        coins += 1
        amount -= 5

    # If change >= 0.01
    while amount >= 1:
        coins += 1
        amount -= 1

    # Print the min number of coins
    print(coins)


def get_positive_float(prompt):
    while True:
        n = get_float(prompt)
        if n > 0:
            return n


main()
