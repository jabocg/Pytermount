#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""(Py)thon (Term)inal emulator from Fall(out) written with (n)curses."""


# import curses
import pathlib
import random

# used temporarily for args
import sys

MAX_SIZE = 408
REGION_WIDTH = 12
REGION_HEIGHT = 34


def main():
    """Start playing the game."""
    initWords()

    difficulty = 0

    if len(sys.argv) > 1:
        difficulty = int(sys.argv[1])

    password, guessable = chooseWords(difficulty=difficulty)

    initTerm(guessable)
    printTerm(mode=1)

    maxguesses = 4
    guesses = 0

    guess = input('>')
    correctness = checkCorrectness(password, guess)
    guesses += 1
    print('>Entry denied.\n>{}/{} correct.'.format(correctness, len(password)))
    correct = False
    while correctness < len(password) and guesses < maxguesses:
        guess = input('>')
        correctness = checkCorrectness(password, guess)
        guesses += 1
        if correctness == len(password):
            correct = True
            break
        print('>Entry denied.\n>{}/{} correct.'.format(correctness,
              len(password)))
    if correct:
        print('>Entry accepted.\n>Access granted.')
    else:
        print('>TOO MANY WRONG ATTEMPTS.\n>ACCESS DENIED.')


def initTerm(words,
             fillers=['`', '-', '=', '[', ']', '\\', ';', '\'', ',', '.', '/',
                      '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
                      '+', '{', '}', '|', ':', '"', '<', '>', '?']):
    """Set up terminal for dispalying."""
    global passwordRegion
    passwordRegion = [''] * MAX_SIZE

    for w in words:
        index = random.randrange(MAX_SIZE)
        isValid = validWordPosition(index, len(w))
        while not isValid:
            index = random.randrange(MAX_SIZE)
            isValid = validWordPosition(index, len(w))
        passwordRegion[index:index + len(w)] = w

    for i, c in enumerate(passwordRegion):
        if c == '':
            passwordRegion[i] = random.choice(fillers)


def printTerm(mode=0):
    """Print password region.

    Keyword arguments:
    mode -- how the terminal is displayed
            0 : single block
            1 : double block
    """
    if mode == 0:
        sectionSize = MAX_SIZE // REGION_WIDTH
        for i in range(sectionSize):
            line = passwordRegion[i * REGION_WIDTH:
                                  i * REGION_WIDTH + REGION_WIDTH]
            print(''.join(line))
    elif mode == 1:
        lines = MAX_SIZE // REGION_WIDTH
        blockSize = lines // 2
        block = [''] * blockSize
        for i in range(lines):
            line = passwordRegion[i * REGION_WIDTH:
                                  i * REGION_WIDTH + REGION_WIDTH]
            if block[i % blockSize] == '':
                block[i % blockSize] = []
            block[i % blockSize].append(''.join(line))
        for l in block:
            print('    '.join(l))


def validWordPosition(index, wordlength):
    """Return whether a position is valid to start a new word.

    Given the global list, a starting index, and the length of the word, return
    whether the given index is valid to start a new word in.
    """
    slice = passwordRegion[clamp(index - wordlength - 1):
                           clamp(index + wordlength) + wordlength]
    return index < MAX_SIZE - wordlength and ''.join(slice) == ''


def clamp(value, minv=0, maxv=MAX_SIZE):
    """Clamp value between min and max."""
    return max(minv, min(value, maxv))


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
    |     4      |    13-14    |
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
        maxwords = 40
    elif difficulty == 1:
        wordlength = random.randrange(6, 9)
        maxwords = 22
    elif difficulty == 2:
        wordlength = random.randrange(9, 11)
        maxwords = 18
    elif difficulty == 3:
        wordlength = random.randrange(11, 13)
        maxwords = 15
    elif difficulty == 4:
        wordlength = random.randrange(13, 15)
        maxwords = 12

    if numwords == 0:
        numwords = random.randint(minwords, maxwords)

    guessable = random.sample(wordlist[wordlength], numwords)
    password = guessable[random.randrange(len(guessable))]

    return password, guessable


def checkCorrectness(password, guess):
    """Return number of correct characters in guess.

    Arguments:
    password -- password to check against
    guess -- word to compare to password
    """
    if not len(password) == len(guess):
        raise ValueError("password and guess cannot be different lengths")

    correcteness = 0

    for i, _ in enumerate(guess):
        if guess[i] == password[i]:
            correcteness += 1

    return correcteness


if __name__ == "__main__":
    main()
