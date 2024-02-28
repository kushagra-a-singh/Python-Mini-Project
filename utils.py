import params
import generate_puzzles

import os
import random
import json
import glob
import sys

def check_letters(pzl):
	if len(pzl) != len(list(set(pzl))):
		print('Invalid number of letters!', file=sys.stderr)
		print('Exiting...', file=sys.stderr)
		exit(1)

	elif len(pzl) != params.TOTAL_LETTER_COUNT:
		print('Invalid number of letters!', file=sys.stderr)
		print('Exiting...', file=sys.stderr)
		exit(1)
	else:
		return

def sort_letters(pzl):
	return pzl[0] + ''.join(sorted(pzl[1:]))

def select_puzzle(puzl_idx=None):
    puzzles = glob.glob(params.PUZZLE_DATA_PATH + os.sep + '*.json')
    puzl_idx_list = [x.split(os.sep)[-1].split('.')[0] for x in puzzles]

    if puzl_idx is None:
        puzl_path = random.choice(puzzles)
        return puzl_path
    if len(puzl_idx) != params.TOTAL_LETTER_COUNT:
        print ('Puzzles must be ',str(params.TOTAL_LETTER_COUNT),'letters long.', file=sys.stderr)
        exit(1)
    if puzl_idx in puzl_idx_list:
        print('Existing puzzle will be played:',puzl_idx)
        puzl_path = params.PUZZLE_DATA_PATH + os.sep + puzl_idx + '.json'
    else:
        puzl_idx = generate_puzzles.main(puzl_idx)
        print ('You created a new puzzle:',puzl_idx)
        puzl_path = params.PUZZLE_DATA_PATH + os.sep + puzl_idx + '.json'
    return puzl_path

def read_puzzle(puzl_path):
    with open(puzl_path,'r') as fp:
        puzzles = json.load(fp)
    print(len(puzzles.get('letters')),'total puzzle(s) were loaded')
    return puzzles

def print_table(data, cols, wide):
    n, r = divmod(len(data), cols)
    pat = '{{:{}}}'.format(wide)
    line = '\n'.join(pat * cols for _ in range(n))
    sys.stdout.reconfigure(encoding="utf-8")
    print(line.format(*data))
    last_line = pat * r
    print(last_line.format(*data[n*cols:]))