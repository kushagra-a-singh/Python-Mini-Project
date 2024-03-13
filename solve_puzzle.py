#!/usr/bin/env python3

import params
import utils
import os
import sys


def solve(p):
    print('letters:', p.get('letters', None))
    print('total_score:', p.get('total_score', ''))
    print('word_count:', p.get('word_count', ''))
    print('pangram(s):', ', '.join(p.get('pangram_list', [])))
    print()

    for x in p.get('word_list', []):
        score = x.get('score')

        if x.get('word') in p.get('pangram_list', []):
            score += +7
        utils.print_table((x.get('word'), score), 2, 10)


def main():
    try:
        puzzle_idx = sys.argv[1].strip().upper()
    except:
        print('Please enter a puzzle. Exiting...')
        exit(0)

    if puzzle_idx is not None:
        utils.check_letters(puzzle_idx)
        puzzle_idx = utils.sort_letters(puzzle_idx)

    puzl_path = utils.select_puzzle(puzzle_idx)

    puzl = utils.read_puzzle(puzl_path)

    solve(puzl)


if __name__ == "__main__":
    main()
