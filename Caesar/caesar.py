# Implement Implement a program that encrypts messages using Caesar’s cipher, per the below.

# $ python caesar.py 13
# plaintext:  HELLO
# ciphertext: URYYB


from sys import argv
from cs50 import get_string


def main():
    # Verify if input data is valid
    if len(argv) != 2:
        print("Usage: python caesar.py integer")
        exit(1)

    # Get key
    key = int(argv[1])
    print(ord('a'))

    # Get plaintext
    plaintext = get_string("plaintext: ")

    # Encipher and print the ciphertext
    z = 0
    print("ciphertext: ", end="")

    for i in range(len(plaintext)):
        if plaintext[i] >= 'a' and plaintext[i] <= 'z':
            z = chr((((ord(plaintext[i]) + key - 97) % 26) + 97))
            print(z, end="")
        elif plaintext[i] >= 'A' and plaintext[i] <= 'Z':
            z = chr((((ord(plaintext[i]) + key - 65) % 26) + 65))
            print(z, end="")
        else:
            print(plaintext[i], end="")

    # Print newline
    print()


main()
