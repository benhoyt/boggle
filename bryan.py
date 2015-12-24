#!/usr/bin/env python

import random
import string
from collections import namedtuple

Cell = namedtuple('cell', 'row col')

class Boggle(object):
    def __init__(self, words=[], words_file=None, board=None):
        self.board = board or self.generate_board(5, 5)
        self.words = set(words) or self.load_words(words_file)
        print 'loaded'

    def generate_board(self, width=5, height=5):
        """ Return width*height array of random letters """
        board = []
        for i in range(height):
            board.append([random.choice(string.lowercase) for i in range(width)])
        return board

    def load_words(self, filename):
        words = []
        with open(filename) as words_file:
            words = [line.strip() for line in words_file]
        return set(words)

    def words_with_prefix(self, prefix, from_words):
        """ Return True if there are any words that have the given prefix. """
        return set([w for w in from_words if w.startswith(prefix)])

    def is_word(self, word):
        return word in self.words and len(word) >= 3

    def print_board(self):
        for row in self.board:
            print ''.join(row)
        
    def print_trail(self, trail):
        print '-----'
        for row in range(len(self.board)):
            print ''.join(letter if Cell(row, col) in trail else ' ' for col, letter in enumerate(self.board[row]))
    
    def traverse(self):
        words = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                print row, col
                words += self.find_words(Cell(row, col))
        return words

    def find_words(self, current_cell=Cell(0, 0), trail=(), word_list=None):
        """ Return a list of words that can be found from cell, given prefix.
            Prefix doesn't include letter in cell.
        """
        word_list = word_list or self.words
        row, col = current_cell     # Save some typing.
        words = []
        trail = trail + (current_cell,)
        word_so_far = ''.join(self.board[c.row][c.col] for c in trail)
        
        word_list = self.words_with_prefix(word_so_far, word_list)
        if not word_list:
            # If no words with the current prefix, then stop this branch early
            return []
            
        if self.is_word(word_so_far):
            self.print_trail(trail)
            words.append(word_so_far)
        
        def on_board(cell):
            return (0 <= cell.row < len(self.board)) and (0 <= cell.col < len(self.board[cell.row]))
        
        try_cells = [Cell(*c) for c in [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1), (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1),
        ]]
        
        for cell in try_cells:
            if not on_board(cell): continue
            if cell in trail: continue          # Skip cells already used in this word
            words += self.find_words(cell, trail, word_list)
        
        return words
        

if __name__ == '__main__':
    boggle = Boggle(words_file='word-list.txt', board=[
        'abcde',
        'fghij',
        'klmno',
        'pqrst',
        'uvwxy',
    ])
#    boggle = Boggle(words_file='word-list.txt')
    print 'Board:\n'
    boggle.print_board()
    
    words = boggle.traverse()
    for word in sorted(set(words)):
        print word
    print 'Num words:', len(words)
