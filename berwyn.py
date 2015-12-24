""" Exhaustively play boggle by finding words from word-list.txt

This algorithm is very fast (solved in 2 milliseconds), but building the word tree is rather slow.

Note1: this solution was written in the allotted 1.5 hours except that:
 1. it had a bug that took me a further 1.5 hours to find: I forgot to strip() the input wordlist
    line endings so it never found any words since they all ended in '\n'. But all
    my testing was with inline wordlists which worked fine because they didn't contain '\n'
 2. it still re-used letters (the used_locations list had not yet been written)
 3. also after the allotted time I added the board_2d() function to make the boards more algorithmically

Note2: If I change the namedtuple to a standard tuple, the word tree build goes 55% faster

"""

import random, collections

def find_words_at(x, y, treepos, used_locations, found_words):
    """ Given board position and tree position, look for continuation of current word in every direction
        used_locations is a list of (x, y) tuples of locations that have already been used to build the word currently being found """
    if x<0 or y<0 or x>=5 or y>=5:
        return
    c = Board[y][x]
    node = treepos.get(c, None)
    if not node:
        return

    location = x, y
    if location in used_locations:
        return

    used_locations.append(location)
    #print "Found letter %s at %d,%d; used_letters are %s; tree keys at this node are: %s" % ( c, x, y, used_letters(used_locations), ''.join(sorted(treepos.keys())) )

    # is it a word?
    if node.word:
        found_words.append(node.word)

    for neighbour in locations_around(x, y):
        find_words_at(neighbour[0], neighbour[1], node.next, used_locations, found_words)

    used_locations.pop()

def solutions(tree):
    found_words = []
    for y in xrange(5):
        for x in xrange(5):
            find_words_at(x, y, tree, used_locations=[], found_words=found_words)
    found_words = set(found_words)  # remove duplicates
    return sorted(found_words)

def locations_around(x, y):
    return [
        (x-1, y-1),
        (x,   y-1),
        (x+1, y-1),

        (x-1, y  ),
        (x+1, y  ),

        (x-1, y+1),
        (x,   y+1),
        (x+1, y+1),
    ]

# ~~~~ Load wordlist tree ~~~~

def fill_tree(tree, remaining, word):
    """ Recursable function to fill tree with remaining part (ending) of word """
    c = remaining[0]
    remaining = remaining[1:]
    if c in tree:
        node = tree[c]
    else:
        node = tree[c] = Node(None if remaining else word, {})
    if remaining:
        fill_tree(node.next, remaining, word)

def build_letter_tree(words):
    """ Return tree of letters given words """
    tree = {}
    for word in words:
        fill_tree(tree, word, word)
    return tree

def read_wordlist():
    """ Read word list from word-list.txt and return it """
    words = []
    with open('word-list.txt') as f:
        for word in f:
            words.append(word.strip())
    return sorted(words)

def used_letters(used_locations):
    """ Debug function to return used letters given used_location list of (x, y) tuples """
    return ''.join(Board[loc[1]][loc[0]] for loc in used_locations)

# ~~~~ Setup board ~~~~

def rand_letter():
    """ Return a random letter """
    letter_n = random.randint(0, 25)
    letter = chr(letter_n+ord('a'))
    return letter

def board_2d(iterable, n):
    """ Convert iterable of n*n values to 2d board of n x n using zip idiom (per docs) """
    return zip(*[iter(iterable)]*n)

Node = collections.namedtuple('node', ['word', 'next'])

print "Building board: ",
#Board = board_2d([rand_letter() for _i in xrange(5*5)], 5)         # random board
Board = board_2d('abcdefghijklmnopqrstuvwxy', 5) # test board
print Board

print "Loading wordlist"
Wordlist = read_wordlist()
print "Building word tree"
Tree = build_letter_tree(Wordlist)

print "Solving"

if __name__ == '__main__':
    print solutions(Tree)

    import timeit
    print "Built word tree in %0.1f s" % timeit.timeit('build_letter_tree(Wordlist)', setup='from __main__ import build_letter_tree, Wordlist, read_wordlist', number=1)
    print "All solutions found in %0.1f ms" % (timeit.timeit('solutions(Tree)', setup='from __main__ import solutions, Tree', number=1) * 1000)
