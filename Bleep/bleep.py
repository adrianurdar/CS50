"""
Implement a program that censors messages that contain words that appear on a list of supplied "banned words."

$ python bleep.py banned.txt
What message would you like to censor?
What the heck
What the ****
$ python bleep.py banned.txt
What message would you like to censor?
gosh darn it
**** **** it
"""

from cs50 import get_string
from sys import argv


def main():
    # Accept 1 command line
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # Remember dictionary
    infile = argv[1]

    # Open dictionary
    dictionary = open(infile, 'r')
    if not dictionary:
        print(f"Could not load {dictionary}")
        exit(1)
    words = []

    # Read all the words and append to a list
    for line in dictionary:
        word = dictionary.readline()
        words.append(line[:-1])
        words.append(word[:-1])

    # Get string from user
    message = get_string("What message would you like to censor?\n")
    message.lower()

    messageList = message.split()
    messageListCopy = message.lower().split()

    # Iterating over banned words
    for i in range(len(words)):

        # Iterating over words in message
        for j in range(len(messageListCopy)):

            # Find if word is in dictionary
            if words[i] == messageListCopy[j]:

                # Making a censored word
                copy = messageList[j]
                copyLength = len(copy)
                copy = ""

                # Replace word with *
                for i in range(copyLength):
                    copy = copy + "*"

                messageList[j] = copy

    # Print back the censored string
    messageCensored = " ".join(map(str, messageList))
    print(messageCensored)


if __name__ == "__main__":
    main()
