
import re, os, sys, itertools, random
import numpy as np
import pdb
from pandas import DataFrame, Series, isnull, notnull
from numpy import nan

if os.getcwd() == 'N:\\Workspace\\krausm\\Python':
    os.chdir("h:\\scr\\")

MAX_WORD_LEN = 15
MAX_LEN=0 # Set Below
OWNER = set(['BAG', 'BOARD']) # Append player ids once game initiates
PLAYER_TYPE = set(['AI', 'HUMAN'])
MULTIPLIERS = ['TRIP_WORD', 'DOUB_WORD', 'TRIP_LET', 'DOUB_LET']

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

# 8 x trip_words
# 17 x double_words
# 12 x triple_let
# 24 x double_lets

MULT_DF = DataFrame()

trip_words = [(a,b) for a in [0,8,14] for b in [0,8,14]]
trip_words.remove((8,8))
MULT_DF = MULT_DF.append( DataFrame([(a,b,'TRIP_WORD') for a,b in trip_words], columns=['Row','Column','Multiplier']) )

double_words = [(a,a) for a in [1,2,3,4,10,11,12,13]]
double_words.extend( [(a,b) for a,b in  zip([13, 12, 11, 10, 4, 3, 2, 1],[1,2,3,4,10,11,12,13])] )
double_words.append((7,7))
MULT_DF = MULT_DF.append( DataFrame([(a,b,'DOUB_WORD') for a,b in double_words], columns=['Row','Column','Multiplier']) , ignore_index=True)

triple_let = [(a,b) for a in [5,9] for b in [1,13]]
triple_let.extend( [(a,b) for a in [1,13] for b in [5,9]] )
triple_let.extend( [(a,b) for a in [5,9] for b in [5,9]] )
MULT_DF = MULT_DF.append( DataFrame([(a,b,'TRIP_LET') for a,b in triple_let], columns=['Row','Column','Multiplier']) , ignore_index=True)

double_let = [(a,b) for a in [3,11] for b in [0,14]]
double_let.extend( [(a,b) for a in [0,14] for b in [3,11]] )#
double_let.extend( [(a,b) for a in [6,8] for b in [2, 12]] )
double_let.extend( [(a,b) for a in [2, 12] for b in [6,8]] )#
double_let.extend( [(7,2), (2,7), (11,7), (7,11)] )
double_let.extend( [(a,b) for a in [6,8] for b in [6,8] ])#
MULT_DF = MULT_DF.append( DataFrame([(a,b,'DOUB_LET') for a,b in double_let], columns=['Row','Column','Multiplier']) , ignore_index=True)    

MULT_DF = MULT_DF.sort('Row')
MULT_DF.set_index(['Row','Column'], drop=False, inplace=True)
del trip_words, double_words, triple_let, double_let

##############################################################################
##############################################################################
##############      UTILITY FUNCTIONS            #############################
##############################################################################
