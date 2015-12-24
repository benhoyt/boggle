"""Find all words on an NxN Boggle-like grid.

Usage:

boggle.py                     # solve random 5x5 grid
boggle.py N                   # solve random NxN grid
boggle.py row1 row2 ... rowN  # solve MxN grid with given rows, eg: abc def ghi
"""

import bisect
import random
import string
import sys
import time

# load wordlist as sorted list
with open('word-list.txt') as f:
    WORDLIST = sorted(line.strip() for line in f if len(line.strip()) >= 3)

# (delta_x, delta_y) for 8 directions including diagonals
DIRS = [
    ( 1,  0), # right
    ( 1,  1), # down-right
    ( 0,  1), # down
    (-1,  1), # down-left
    (-1,  0), # left
    (-1, -1), # left-up
    ( 0, -1), # up
    ( 1, -1), # up-right
]

# populated below from command line arguments
GRID = []


clock = time.clock if sys.platform == 'win32' else time.time


def find_words(x0, y0, prefix, used):
    """Find words from (x0, y0) starting with given "prefix" string, but
    not including grid positions in "used" tuple.
    """
    words = set()
    for dir in DIRS:
        x = x0 + dir[0]
        y = y0 + dir[1]
        if x < 0 or y < 0 or x >= len(GRID[0]) or y >= len(GRID):
            continue  # done if we go off the grid
        if (x, y) in used:
            continue  # done if this position has already been used
        word = prefix + GRID[y][x]

        # binary search to find index of word or word prefix
        index = bisect.bisect_left(WORDLIST, word)
        if index >= len(WORDLIST):
            continue
        found = WORDLIST[index]

        if found == word:
            # found an exact match, add it to list
            words.add(word)

        if found.startswith(word):
            # found a word prefix, recursively find words from here with this
            # prefix and add them to list
            words.update(find_words(x, y, word, used + ((x, y),)))
    
    return words


def solve():
    """Solve the GRID and return set of all words found."""
    words = set()
    for y0 in range(len(GRID)):
        for x0 in range(len(GRID[0])):
            words.update(find_words(x0, y0, GRID[y0][x0], ((x0, y0),)))
    return words


if __name__ == '__main__':
    # parse command line arguments
    if len(sys.argv) > 1 and not sys.argv[1].isdigit():
        GRID = [row.lower() for row in sys.argv[1:]]
    else:
        if len(sys.argv) > 1:
            n = int(sys.argv[1])
        else:
            n = 5
        GRID = []
        for y in range(n):
            GRID.append(''.join(random.choice(string.ascii_lowercase) for x in range(n)))

    # print the grid we're solving
    for row in GRID:
        print row
    print '-----'

    # solve and print the words found and number of solutions
    start_time = clock()
    words = solve()
    elapsed_time = clock() - start_time
    print ' '.join(sorted(words))
    print '-----'
    print 'found', len(words), 'in', elapsed_time, 'seconds'
