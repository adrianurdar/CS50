# Mario half pyramid in py
from cs50 import get_int


def main():
    h = get_positive_int("Positive integer: ")

    # Draw the half pyramid
    # For every row
    for i in range(h):
        # Print spaces
        print(" " * (h-i-1), end="")
        # Print hashes
        print("#" * (i + 1), end="")
        # Print a new line
        print()

# Define a positive integer between 1 and 8


def get_positive_int(prompt):
    while True:
        n = get_int(prompt)
        if n >= 1 and n <= 8:
            return n


main()
