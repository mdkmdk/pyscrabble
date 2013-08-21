
import re, os, sys, itertools, random
import numpy as np
import pdb
from pandas import DataFrame, Series

if os.getcwd() == 'N:\\Workspace\\krausm\\Python':
    os.chdir("h:\\scr\\")

# Setup words list
sep = os.linesep
with open('sowpods.txt') as f:
    WORDS = [w.rstrip(sep) for w in f]

WORDS = sorted(WORDS, key=lambda x: len(x))

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
##############################################################################
##############################################################################