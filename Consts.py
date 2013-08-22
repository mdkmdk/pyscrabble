
import re, os, sys, itertools, random
import numpy as np
import pdb
from pandas import DataFrame, Series, isnull, notnull
from numpy import nan

if os.getcwd() == 'N:\\Workspace\\krausm\\Python':
    os.chdir("h:\\scr\\")

MAX_WORD_LEN = 15
MAX_LEN=0 # Set Below

# Setup words list
sep = os.linesep
with open('sowpods.txt') as f:
    temp = [w.rstrip(sep) for w in f]
    
temp.reverse()

WORDS = {}
for i in range(1,MAX_WORD_LEN+1):
    WORDS[i] = set()

while True:
    try:
        w = temp.pop()
    except IndexError:
        break
    WORDS[len(w)].add(w)

del temp

# Tuples denote a) number of tiles and b)score
TILE_DICT = {
    'a': (9, 1),
    'b': (2, 3),
    'c': (2, 3),
    'd': (4, 2),
    'e': (12, 1),
    'f': (2, 4),
    'g': (3, 2),
    'h': (2, 4),
    'i': (9, 1),
    'j': (1, 8),
    'k': (1, 5),
    'l': (4, 1),
    'm': (2, 3),
    'n': (6, 1),
    'o': (8, 1),
    'p': (2, 3),
    'q': (1, 10),
    'r': (6, 1),
    's': (4, 1),
    't': (6, 1),
    'u': (4, 1),
    'v': (2, 4),
    'w': (2, 4),
    'x': (1, 8),
    'y': (2, 4),
    'z': (1, 10),
    ' ': (2, 0)
    }
    
OWNER = set(['BAG', 'BOARD']) # Append player ids once game initiates
PLAYER_TYPE = set(['AI', 'HUMAN'])
##############################################################################
##############################################################################
##############      UTILITY FUNCTIONS            #############################
##############################################################################
