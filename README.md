# Pytermount

/'piːtərmaʊnt/ - **Py**thon Fall**out** **Term**inal emulator written with **n**-curses


## Overview

__Pytermount__(pronounced _pee ter mount_) is an attempt at emulating the
Fallout series' terminal password guessing game in python with the help of
`ncurses`.

The terminal window is 53 characters wide and 22 lines tall. The actual password
selection windows are 12 characters wide and 17 lines tall. This gives us 204
characters to work with. Two words will always be at least one word length apart
from the next one.

## Requirements

* Python 3.6+
* `ncurses`(or [UniCurses](https://pypi.python.org/pypi/UniCurses) if on Windows)
