#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import curses
import pathlib
import random

# used temporarily for args
import sys

"""
Pytermount  - the Fallout Terminal password guessing game written in Python
              using ncurses
"""

def initWords(filepath='falloutdict.txt'):
    """Initialize the global words list using file found at filepath.

    Keyword arguments:
    filepath -- path to the file containing all possible words, serparated by
                spaces
    """
    global wordlist
    wordlist = {}

    wordsfile = pathlib.Path(filepath)

    with wordsfile.open() as f:
        list = f.read().split()
        for w in list:
            if len(w) not in wordlist:
                wordlist[len(w)] = []
            wordlist[len(w)].append(w)


def main():
    initWords()

    difficulty = 0

    if len(sys.argv) > 1:
        difficulty = int(sys.argv[1])

    password, guessable = chooseWords(difficulty=difficulty)

    print(guessable)
    print(password)

def chooseWords(difficulty=0, numwords=0):
    """Return a password and list of guessable words(including the password).

    difficulty defines the length of the words based on the below table
    +------------+-------------+
    | difficulty | word length |
    +------------+-------------+
    |     0      |     4-5     |
    |     1      |     6-8     |
    |     2      |     9-10    |
    |     3      |    11-12    |
    |     4      |    13-15    |
    +------------+-------------+

    numwords is randomized if not specified, must be more than 1

    Keyword arguments:
    difficulty -- password difficulty, ranging from 0 to 4
    numwords -- number of words to return

    Returns:
    password -- randomly selected password
    guessable -- list of guessable words(including the password)
    """
    wordlength = 0
    minwords = 5
    maxwords = 0
    if difficulty == 0:
        wordlength = random.randrange(4, 6)
        maxwords = 17
    elif difficulty == 1:
        wordlength = random.randrange(6, 9)
        maxwords = 11
    elif difficulty == 2:
        wordlength = random.randrange(9,11)
        maxwords = 9
    elif difficulty == 3:
        wordlength = random.randrange(11, 13)
        maxwords = 7
    elif difficulty == 4:
        wordlength = random.randrange(13, 16)
        maxwords = 6

    if numwords == 0:
        numwords = random.randint(minwords, maxwords)

    guessable = random.choices(wordlist[wordlength], k=numwords)
    password = guessable[random.randrange(len(guessable))]

    return password, guessable


def checkCorrectness(password, guess):
    """Return number of correct characters in guess.

    Arguments:
    password -- password to check against
    guess -- word to compare to password
    """
    if not len(password) == len(guess):
        raise ValueError("password and chosen word cannot be different lengths")

    correcteness = 0

    for i, _ in enumerate(guess):
        if guess[i] == password[i]:
            correcteness += 1

    return correcteness

if __name__ == "__main__":
    main()
