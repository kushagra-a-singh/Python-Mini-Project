#This file acts as a configuration File for Python Script named generate_puzzles.py , it defines various parameters used by the script to generate Word Puzzles.

#!/usr/bin/env python3

import os

#Defines the number of puzzles to Generate 
PUZZLE_COUNT = 1000

#Maximum Number of attempts to generate a valid puzzle before giving up
MAX_PUZZLE_TRIES = 100000

#(This step is important for file merging , it basically specifies the locatio of the word file used for puzzle Gen)
WORD_LIST_PATH = 'word_lists' + os.sep + 'scowl.txt'
PUZZLE_DATA_PATH = 'data'

#multithreading
THREADS = 1

# This sets minimum word length and total letters used
MIN_WORD_LENGTH = 4
TOTAL_LETTER_COUNT = 7

VOWEL_LIST = ('A','E','I','O','U')

#a sentence that contains every letter of the alphabet, if possible with each letter only being used once
COUNT_PANGRAMS = 1

MIN_WORD_COUNT = 25
MAX_WORD_COUNT = 50

# Reject games with too many plural pairs (Ending with -S)
CAP_PLURALS = True
MAX_PLURALS = 3

# Reject games with too many gerund pairs (Ending with -ING)
CAP_GERUNDS = True
MAX_GERUNDS = 5

# total score limits
MIN_TOTAL_SCORE = 60
MAX_TOTAL_SCORE = 240

# Show rejected games as well as valid ones.
# True, False, or "dots", or "why".
PRINT_INVALID = "dots"        # "dots" simply prints a dot per invalid game.
PRINT_INVALID = "why"         # "why" prints % stats for invalid games.
