""" play puzzles based on params.py PUZZLE_PATH_READ value"""

import params
import utils

import os
import sys
import random


def play(puzl):
    print("Type !help or !h for help")

    letters = puzl.get("letters")
    print("Playing puzzle index:", letters)

    print("Your letters are:", draw_letters_honeycomb(letters))

    word_list = puzl.get("word_list")
    pangram_list = puzl.get("pangram_list")
    total_score = puzl.get("total_score") + 7 * int(puzl.get("pangram_count"))
    word_count = puzl.get("word_count")

    print("Max score:", total_score)
    print("Total words:", word_count)

    player_score = 0
    player_words = 0
    guess_list = []
    player_pangram = False

    valid_combinations = []

    word_lists_by_length = {length: [] for length in range(4, 8)} 
    for word_entry in word_list:
        word = word_entry["word"]
        length = len(word)
        if length in word_lists_by_length:
            word_lists_by_length[length].append(word)

    for length, words in word_lists_by_length.items():
        if words:
            print(f"\nWords with {length} letters:")
            for word in words:
                print(word)

    while True:
        guess = ask_user()

        if guess.startswith("!"):
            if guess.lower() == "!a":
                # Display all possible word combinations stored in the word_list
                print("\nAll possible word combinations:")
                for word_entry in word_list:
                    print(word_entry["word"])
                continue
            else:
                help(
                    guess,
                    letters,
                    guess_list,
                    player_score,
                    player_words,
                    player_pangram,
                    total_score,
                    word_count,
                    word_list,
                )
                continue

def is_word_possible(word, letters):
    """
    Check if a word can be formed from the given letters.
    Args:
        word (str): The word to check.
        letters (str): The available letters.
    Returns:
        bool: True if the word can be formed, False otherwise.
    """
    # Check if each letter in the word is available in the given letters
    for letter in word:
        if letter not in letters:
            return False

    return True

def calculate_score(word, letters):
    """
    Calculate the score of a word based on the given letters.
    """
    score = 0  # Initialize score to 0
    word_length = len(word)
    
    # Award points based on word length
    if word_length == 4:
        score = 1
    elif word_length > 4:
        score = word_length - 3  # Additional points for each letter beyond 4
    
    # Check if the word is a pangram and award additional points
    if set(word) == set(letters):
        score += 7

    return score


def calculate_score(word, letters):
    """
    Calculate the score of a word based on the given letters.
    """
    score = 1  # Initialize score to 1
    for letter in word:
        if letter in letters:
            score += 1  # Increment score by 1 for each valid letter
    return score

def get_instructions():
    instructions = """
    Welcome to the Spelling Bee Puzzle Game!
    
    Here are the rules:
    1. Try to make as many words as you can using the given letters.
    2. Each word must contain the central letter at least once.
    3. Each word must be at least 4 letters long.
    4. Each word must be unique and valid.
    5. The player's score is based on the total number of valid words found.
    
    Have fun playing!
    """
    return instructions

def get_show_answers(word_list):
    """
    Display all possible word combinations stored in the word_list.
    
    Args:
        word_list (list): A list of dictionaries containing word entries.
            Each dictionary should have a key named "word" containing the word.
    """
    print("\nAll possible word combinations:")
    for word_entry in word_list:
        print(word_entry["word"])

def shuffle_letters(letters):
    other_letters = list(letters[1:])
    random.shuffle(other_letters)
    return letters[0] + "".join(other_letters)

def draw_letters_honeycomb(letters):
    if len(letters) != 7:
        return letters[0] + " " + "".join(letters[1:])

    hex_string = r"""
            _____
           /     \
          /       \
    ,----(    {2}    )----.
   /      \       /      \
  /        \_____/        \
  \   {1}    /     \    {3}   /
   \      /       \      /
    )----(    {0}'   )----(
   /      \       /      \
  /        \_____/        \
  \   {4}    /     \    {5}   /
   \      /       \      /
    `----(    {6}    )----'
          \       /
           \_____/
    """.format(
        *letters
    )

    return hex_string

def ask_user():
    text = input("Your guess: ")
    text = text.strip().upper()

    return text


def help(
    msg,
    letters,
    guess_list,
    player_score,
    player_words,
    player_pangram,
    total_score,
    word_count,
    word_list,
):

    clean_msg = msg.replace("!", "")
    if clean_msg:
        clean_msg = clean_msg[0].lower()
    else:
        clean_msg = "i"

    if clean_msg == "q":
        print("\nAll possible word combinations:")
        for word_entry in word_list:
            print(word_entry["word"])
        print("\nTotal words:", word_count)
        print("Number of words you guessed correctly:", player_words)

        choice = input("\nDo you want to play another puzzle? (Y/N): ").strip().upper()
        if choice == "Y":
            main()
        else:
            print("\nQuitting...")
            exit(0)

    help_msg = (
        "!i : instructions\n!g : show letters\n!f : shuffle letters\n!s : player stats\n!h : help\n!a : show all possible word combinations\n!q : quit"
    )
    instruction_msg = (
        """
    Welcome to Spelling Bee puzzle!
    To play, build minimum """
        + str(params.MIN_WORD_LENGTH)
        + """-letter words.
    Each word must include the center letter at least once.
    Letters may be used as many times as you'd like.

    Scoring: 1 point for a 4 letter word, and 1 more point for each word longer than 4 letters.
                Example:  WORD - 1 point
                          WORDS - 2 points
                          SPELLING - 5 points

    Each puzzle has """
        + str(params.COUNT_PANGRAMS)
        + """ pangram(s) that uses each of the """
        + str(params.TOTAL_LETTER_COUNT)
        + """ letters.
    The pangram is worth 7 extra points.

    Have fun!
    """
    )

    msg_dict = {
        "h": help_msg,
        "i": instruction_msg,
        "g": draw_letters_honeycomb(letters),
        "f": draw_letters_honeycomb(shuffle_letters(letters)),
        "s": "guessed: "
        + ", ".join(guess_list[::-1])
        + "\n"
        "player words: "
        + str(player_words)
        + " / "
        + str(word_count)
        + " ("
        + str(round(player_words * 100.0 / word_count, 1))
        + "%)"
        + "\n"
        "player score: "
        + str(player_score)
        + " / "
        + str(total_score)
        + " ("
        + str(round(player_score * 100.0 / total_score, 1))
        + "%)"
        + "\n"
        "pangram found: "
        + str(player_pangram),
    }

    print(msg_dict.get(clean_msg, "Unknown selection"))
    return


def main():
    try:
        puzzle_idx = sys.argv[1].strip().upper()
    except:
        puzzle_idx = None

    if puzzle_idx is not None:
        utils.check_letters(puzzle_idx)
        puzzle_idx = utils.sort_letters(puzzle_idx)

    puzl_path = utils.select_puzzle(puzzle_idx)

    puzl = utils.read_puzzle(puzl_path)

    play(puzl)


if __name__ == "__main__":

    main()
