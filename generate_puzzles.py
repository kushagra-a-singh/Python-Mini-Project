import params
import utils
import os
import sys
import string
import random
from multiprocessing import Pool as ThreadPool
import itertools
import json
import glob

def get_existing_puzzles():
    existing_puzzles = glob.glob(params.PUZZLE_DATA_PATH + os.sep + '*.json')
    existing_puzzles = [x.replace(params.PUZZLE_DATA_PATH + os.sep, '').replace('.json', '') for x in existing_puzzles]
    return existing_puzzles

def get_words(word_file):
    with open(params.WORD_LIST_PATH, 'r') as wp:
        words = [w.strip() for w in wp.readlines() if len(w.strip()) >= params.MIN_WORD_LENGTH]
    return words

def get_letters():
    alphabet_list = list(string.ascii_uppercase)
    random_list = random.sample(alphabet_list, params.TOTAL_LETTER_COUNT)
    if any(letter in params.VOWEL_LIST for letter in random_list):
        return utils.sort_letters(''.join(random_list))

def get_letters_from(letters_list):
    letters = random.choice(letters_list)
    return utils.sort_letters(''.join(random.sample(letters, len(letters))))

def check_words(letters, word):
    letters = list(letters)
    if all(x in set(letters) for x in word) and letters[0] in word:
        score = len(word) - params.MIN_WORD_LENGTH + 1
        pangram = all(x in set(word) for x in letters)
        return {'word': word, 'score': score, 'pangram': pangram}
    else:
        return None

def get_score(word):
    return len(word) - params.MIN_WORD_LENGTH + 1

def make_puzzles(word_list, pool, existing_puzzles, letters=None):
    is_valid = True
    why_invalid = {}
    global valid_count

    if letters is not None:
        manual_puzzle = True
    else:
        manual_puzzle = False
        letters = get_letters_from(pool)

    if letters in existing_puzzles:
        is_valid = False
        why_invalid['Already found'] = 1
        return 0

    results = ThreadPool(params.THREADS).starmap(check_words, zip(itertools.repeat(letters), word_list)) \
        if params.THREADS > 1 else [check_words(letters, word) for word in word_list]

    results = list(filter(None.__ne__, results))
    total_score = sum(x.get('score') for x in results)
    pangram_list = [x.get('word') for x in filter(lambda x: x.get('pangram'), results)]

    if not manual_puzzle:
        if len(pangram_list) < params.COUNT_PANGRAMS or len(pangram_list) > params.COUNT_PANGRAMS \
                or total_score < params.MIN_TOTAL_SCORE or total_score > params.MAX_TOTAL_SCORE \
                or len(results) < params.MIN_WORD_COUNT or len(results) > params.MAX_WORD_COUNT \
                or (params.CAP_PLURALS and 'S' in letters and count_plurals(results) > params.MAX_PLURALS) \
                or (params.CAP_GERUNDS and all(x in letters for x in ('I', 'N', 'G')) and count_gerunds(results) > params.MAX_GERUNDS):
            is_valid = False
            why_invalid['Invalid'] = 1
            if params.PRINT_INVALID == "dots":
                print('.', end='', flush=True)
            elif params.PRINT_INVALID == "why":
                print_cumulative_why(why_invalid)
            elif params.PRINT_INVALID:
                print('\t'.join((letters, str(len(results)), str(total_score), str(len(pangram_list)), str(0))))
            return 0

    elif params.PRINT_INVALID == "dots":
        print('')

    print('\t'.join((letters, str(len(results)), str(total_score), str(len(pangram_list)), str(1))))

    if not manual_puzzle:
        valid_count += 1

    pangram_list = [x.get('word') for x in pangram_list]

    generation_info = {
        'path': params.WORD_LIST_PATH,
        'min_word_length': params.MIN_WORD_LENGTH,
        'total_letter_count': params.TOTAL_LETTER_COUNT,
        'min_word_count': params.MIN_WORD_COUNT,
        'max_word_count': params.MAX_WORD_COUNT,
        'min_total_score': params.MIN_TOTAL_SCORE,
        'max_total_score': params.MAX_TOTAL_SCORE,
        'cap_plurals': params.CAP_PLURALS,
        'max_plurals': params.MAX_PLURALS,
        'cap_gerunds': params.CAP_GERUNDS,
        'max_gerunds': params.MAX_GERUNDS,
        'count_pangrams': params.COUNT_PANGRAMS,
        'manual_puzzle': manual_puzzle,
    }

    tmp = {
        'letters': letters,
        'generation_info': generation_info,
        'total_score': total_score,
        'word_count': len(results),
        'pangram_count': len(pangram_list),
        'pangram_list': pangram_list,
        'word_list': results,
    }

    file_path = params.PUZZLE_DATA_PATH + os.sep + letters + '.json'
    with open(file_path, 'w') as json_file:
        json.dump(tmp, json_file, indent=4)

    return 1

def count_plurals(results):
    words = [x['word'] for x in results]
    count = 0
    for word in words:
        if word.endswith('S') and (word[0:-1] in words or (word.endswith('ES') and word[0:-2] in words)):
            count += 1
    return count

def count_gerunds(results):
    words = [x['word'] for x in results]
    count = 0
    for word in words:
        if word.endswith('ING') and (word[0:-3] in words or word[0:-3] + 'E' in words or \
                                     (len(word) >= 5 and word[-4] == word[-5] and word[0:-4] in words)):
            count += 1
    return count

def print_cumulative_why(why):
    global why_cumulative
    print()
    print("Reasons why generated games were rejected:")
    for k in why:
        why_cumulative[k] += why[k] / len(why)
    total = sum(why_cumulative[k] for k in why_cumulative)
    for k in why_cumulative:
        print('%24s: %5.2f%%' % (k, 100 * why_cumulative[k] / total))
    print()
    print('%24s: %d' % ('Valid games found', valid_count), flush=True)

def main(puzzle_input=None):
    if not os.path.isdir(params.PUZZLE_DATA_PATH):
        os.makedirs(params.PUZZLE_DATA_PATH)

    existing_puzzles = get_existing_puzzles()
    words = get_words(params.WORD_LIST_PATH)
    pool = get_pangramable_letter_pool(words)

    print('\t'.join(('letters', 'word_count', 'total_score', 'pangram_count', 'is_valid')))

    puzzle_input = sys.argv[1].strip().upper() if len(sys.argv) > 1 else None

    if puzzle_input is not None:
        utils.check_letters(puzzle_input)
        puzzle_input = utils.sort_letters(puzzle_input)
        make_puzzles(words, pool, existing_puzzles, puzzle_input)
    else:
        idx_valid = 0
        for _ in range(params.MAX_PUZZLE_TRIES):
            idx_valid += make_puzzles(words, pool, existing_puzzles, None)
            if idx_valid >= params.PUZZLE_COUNT:
                exit(0)

if __name__ == "__main__":
    main()

