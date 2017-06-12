#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import curses
import pathlib

"""
Pytermount  - the Fallout Terminal password guessing game written in Python
              using ncurses
"""

def initWords(filepath='falloutdict.txt'):
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

def checkCorrectness(password, selectedWord):
    if not len(password) == len(selectedWord):
        raise ValueError("password and chosen word cannot be different lengths")

    correcteness = 0

    for i, _ in enumerate(selectedWord):
        if selectedWord[i] == password[i]:
            correcteness += 1

    return correcteness

if __name__ == "__main__":
    main()
