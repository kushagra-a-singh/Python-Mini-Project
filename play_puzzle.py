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

    # Store all valid word combinations
    valid_combinations = []

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

        if guess in guess_list:
            print("You already found:", guess, "\n")
            continue

        if len(guess) < params.MIN_WORD_LENGTH:
            print(
                "Guessed word is too short. Minimum length:",
                str(params.MIN_WORD_LENGTH),
                "\n",
            )
            continue

        if any([x for x in guess if x not in letters]):
            print("Invalid letter(s)", "\n")
            continue

        if letters[0] not in guess:
            print("Must include center letter:", letters[0], "\n")
            continue

        word_index = next(
            (index for (index, d) in enumerate(word_list) if d["word"] == guess), None
        )

        if word_index is None:
            print("Sorry,", guess, "is not a valid word", "\n")
            continue
        elif guess in guess_list:
            print("You already found", guess, "\n")
            continue
        else:
            word_dict = word_list[word_index]

            player_words += 1
            word_score = word_dict.get("score")

            if word_dict.get("word") in pangram_list:
                word_score += 7
                player_pangram = True
                print("\nPANGRAM!!!")

            player_score += word_score

            print_list = [
                "✓ " + guess,
                "word score = " + str(word_score),
                "words found = " + str(player_words) + "/" + str(word_count),
                "total score = " + str(player_score) + "/" + str(total_score),
            ]

            if word_dict.get("word") in pangram_list:
                print_list[0] += " ***"

            utils.print_table(print_list, len(print_list), 22)
            print()

            guess_list.append(guess)
            valid_combinations.append(guess)

        if player_words == word_count:
            print("Congratulations. You found them all!", "\n")
            break  # Exit the loop when all words are found

    print("\nAll possible word combinations:")
    for word_entry in word_list:
        print(word_entry["word"])

    print("\nTotal words:", word_count)
    print("Correctly guessed words:", player_words)
    print("Pangram found:", player_pangram)  # Add this line to print whether pangram was found

    # Add these lines to update the current puzzle dictionary with player stats
    puzl["player_score"] = player_score
    puzl["player_words"] = player_words
    puzl["player_pangram"] = player_pangram

    return puzl


def is_word_possible(word, letters):
    """
    Check if a word can be formed from the given letters.
    Args:
        word (str): The word to check.
        letters (str): The available letters.
    Returns:
        bool: True if the word can be formed, False otherwise.
    """
    # Count occurrences of each letter in the word and available letters
    word_count = {letter: word.count(letter) for letter in set(word)}
    letter_count = {letter: letters.count(letter) for letter in set(letters)}

    # Check if each required letter in the word is available in sufficient quantity
    for letter, count in word_count.items():
        if letter not in letter_count or count > letter_count[letter]:
            return False

    return True

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
