"""Find all words on a 5x5 Boggle-like grid using a set and trie."""

import sys
import time


WORDLIST = set()
PREFIX_TREE = {}

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

GRID = [
    'abcde',
    'fghij',
    'klmno',
    'pqrst',
    'uvwxy',
]


clock = time.clock if sys.platform == 'win32' else time.time


def find_words(x0, y0, prefix, used, node):
    """Find words from (x0, y0) starting with given "prefix" string, but
    not including grid positions in "used" tuple.
    """
    words = set()
    for dx, dy in DIRS:
        x = x0 + dx
        if x < 0 or x >= 5:
            continue  # done if we go off the grid
        y = y0 + dy
        if y < 0 or y >= 5:
            continue  # done if we go off the grid
        if (x, y) in used:
            continue  # done if this position has already been used
        char = GRID[y][x]
        word = prefix + char

        if word in WORDLIST:
            # found an exact match, add it to list
            words.add(word)

        if char in node:
            # found a word prefix, recursively find words from here with this
            # prefix and add them to list
            words.update(find_words(x, y, word, used + ((x, y),), node[char]))
    
    return words


def solve():
    """Solve the GRID and return set of all words found."""
    words = set()
    for y0 in xrange(5):
        for x0 in xrange(5):
            char = GRID[y0][x0]
            words.update(find_words(x0, y0, char, ((x0, y0),), PREFIX_TREE[char]))
    return words


def load_wordlist():
    """Load entire wordlist as set for fast full-word lookups."""
    start_time = clock()
    with open('word-list.txt') as f:
        wordlist = set(line.strip() for line in f if len(line.strip()) >= 3)
    elapsed_time = clock() - start_time
    print 'loaded wordlist in', elapsed_time, 'seconds'
    return wordlist


def build_prefix_tree(wordlist):
    """Build tree (trie) data structure for fast prefix lookups."""
    start_time = clock()
    tree = {}
    for word in wordlist:
        node = tree
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
    elapsed_time = clock() - start_time
    print 'built prefix tree in', elapsed_time, 'seconds'
    return tree


if __name__ == '__main__':
    WORDLIST = load_wordlist()
    PREFIX_TREE = build_prefix_tree(WORDLIST)
    print '-----'

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
    print 'found', len(words), 'words in', elapsed_time, 'seconds'
