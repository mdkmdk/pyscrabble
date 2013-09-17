"""
Created by Michael Kraus
Testing PYDOC Web Help

"""
import re, os, sys, itertools, random, pickle
from colorama import init, deinit, Fore, Back, Style # Colored terminal text
import numpy as np
import pdb
from pandas import DataFrame, Series, isnull, notnull
from numpy import nan

pydoc_cmd = r'U:/python/apps/run_local.bat "C:/local_runtimes_64/19.10/Lib/pydoc.py" -w first_tests'

#global mylog
#mylog = logging.Logger()
#fh = logging.FileHandler('scrabble.log')
#fh.setLevel(logging.DEBUG)
#mylog.addHandler(fh)

#logging.basicConfig(filename='scrabble.log', level=logging.DEBUG, filemode='w')
#logging.debug('This message should go to the log file')
#logging.INFO('So should this')
#logging.warning('And this, too')

if os.getcwd() == 'N:\\Workspace\\krausm\\Python':
    os.chdir("h:\\git\\pyscrabble\\")

""" Maximum Word Length Allowed """
COLOR_OUTPUT = True
MAX_WORD_LEN = 15
MAX_LEN=0 # Set Below
OWNER = set(['BAG', 'BOARD']) # Append player ids once game initiates
PLAYER_TYPE = set(['AI', 'HUMAN'])
MULTIPLIERS = {'TRIP_WORD':'3W', 'DOUB_WORD':'2W', 'TRIP_LET':'3L', 'DOUB_LET':'2L'}

# Setup words list
sep = os.linesep

try:
    f = file('words.pickle','rb')
    WORDS = pickle.load(f)
except IOError:
    with open('sowpods.txt') as f:
        temp = [w.rstrip(sep) for w in f]
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
    f = file('words.pickle', 'wb')
    pickle.dump(WORDS, f, protocol=2)
else:
    pass
finally:
    l = 0
    for w in WORDS.itervalues(): l+= len(w)
    f.close()
    del f
    print "Dictionary Successfully Loaded: %s Words" % l

#with open('sowpods.txt') as f:
#    temp = [w.rstrip(sep) for w in f]
    
#WORDS = {}
#for i in range(1,MAX_WORD_LEN+1):
#    WORDS[i] = set()
#
#while True:
#    try:
#        w = temp.pop()
#    except IndexError:
#        break
#    WORDS[len(w)].add(w)
#
#del temp

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

#MULT_DF = DataFrame()
MULT_LET = {}
MULT_WORD = {}


trip_words = [(a,b) for a in [0,7,14] for b in [0,7,14]]
trip_words.remove((7,7))
#MULT_DF = MULT_DF.append( DataFrame([(a,b,'TRIP_WORD') for a,b in trip_words], columns=['Row','Column','Multiplier']) )
for a in trip_words: MULT_WORD[a] = 'TRIP_WORD'

double_words = [(a,a) for a in [1,2,3,4,10,11,12,13]]
double_words.extend( [(a,b) for a,b in  zip([13, 12, 11, 10, 4, 3, 2, 1],[1,2,3,4,10,11,12,13])] )
double_words.append((7,7))
#MULT_DF = MULT_DF.append( DataFrame([(a,b,'DOUB_WORD') for a,b in double_words], columns=['Row','Column','Multiplier']) , ignore_index=True)
for a in double_words: MULT_WORD[a] = 'DOUB_WORD'

triple_let = [(a,b) for a in [5,9] for b in [1,13]]
triple_let.extend( [(a,b) for a in [1,13] for b in [5,9]] )
triple_let.extend( [(a,b) for a in [5,9] for b in [5,9]] )
#MULT_DF = MULT_DF.append( DataFrame([(a,b,'TRIP_LET') for a,b in triple_let], columns=['Row','Column','Multiplier']) , ignore_index=True)
for a in triple_let: MULT_LET[a] = 'TRIP_LET'

double_let = [(a,b) for a in [3,11] for b in [0,14]]
double_let.extend( [(a,b) for a in [0,14] for b in [3,11]] )#
double_let.extend( [(a,b) for a in [6,8] for b in [2, 12]] )
double_let.extend( [(a,b) for a in [2, 12] for b in [6,8]] )#
double_let.extend( [(7,3), (3,7), (11,7), (7,11)] )
double_let.extend( [(a,b) for a in [6,8] for b in [6,8] ])#
#MULT_DF = MULT_DF.append( DataFrame([(a,b,'DOUB_LET') for a,b in double_let], columns=['Row','Column','Multiplier']) , ignore_index=True)    
for a in double_let: MULT_LET[a] = 'DOUB_LET'

#MULT_DF = MULT_DF.sort(['Row','Column'])
#MULT_DF.set_index(['Row','Column'], drop=False, inplace=True)
del trip_words, double_words, triple_let, double_let

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class Tile:
    def __init__(self, let, scr=None, t_id=None, owner=None):
        if (len(let) == 1) and ((let.isalpha()) or let == ' '):
            self.letter = let
        else:
            # What is the more informative way to do this?
            raise
            return
        self.scr = scr
        self.owner = owner
        self.t_id = t_id
        
    def __hash__(self):
        return id(self)

    def __str__(self):
        return "%s\t%i\t%i\t%s" %(self.letter, self.scr, self.t_id, self.owner)

    # Compares t_id
    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other,Tile):
            if self.t_id == other.t_id: 
                return True
            else:
                return False

#    implement addition for easy word creation
    def __add__(self, other):
        # logic different for if owners e ('bag','rack','board')
        return self.letter + other.letter

    def isLetter(let):
        if let == self.let:
            return True
        else:
            return False

class Bag:
    def __init__(self):
        self.bag_tiles = []
        self._populateLetters()
    
    def append(self,x):
        if isinstance(x, Tile):
            if x not in self.bag_tiles:
                self.bag_tiles.append(x)
                self._populateLetters()
                return True
            else:
                return False
        if isinstance(x, Bag):
            self.bag_tiles.extend( x.bag_tiles )
            self._populateLetters()
            return True
        if isinstance(x, list) and all([isinstance(el, Tile) for el in x]):
            self.bag_tiles.extend( x )
            self._populateLetters()
            return True
        return False

    def remove(self, val):
        
        print val
#        ###pdb.set_trace()
        tle = None
#        ###pdb.set_trace()
        if isinstance(val, int):
            # remove by t_id
            for t in self.bag_tiles:
                if val == t.t_id:
                    tle = t
                    break
#                    self.remove(t)
#                    return 
        if isinstance(val,str):
            # remove by letter
            for t in self.bag_tiles:
                if val == t.letter:
                    tle = t
                    break
#                    self.remove(t)
#                    return t
#            return None 
        
        if isinstance(val, Tile):
            tle = val
            
        if tle is not None:
            # remove by tile instance
            try:
                self.bag_tiles.remove(tle)
            except ValueError:
                return None
            else:
                self._populateLetters()
                return tle
        
        return None
        
#    def pop(self, t_id=None, let=None):
#        if t_id is not None:
#            for t in self.bag_tiles:
#                if t_id == t.t_id:
#                    self.remove(t)
#                    return t
#            return None
#        elif let is not None:
#            for t in self.bag_tiles:
#                if t.letter == let:
#                    self.remove(t)
#                    return t
#            return None 
#        else:
#            return None

    def getRandomTile(self):
        rem_tile = random.randint(0, len(self.bag_tiles)-1)
        t = self.bag_tiles[rem_tile]
        self.remove(t)
        return t
    
    # To Facilitate Exchanging Tiles
    def exchange(self):
        pass
    
    def getLetterSet(self):
        return set(self.letters)
    
    def getTileFromLetters(self,lst):
        """
        lst: a list of letters
        
        Returns a list of tiles if all letters in bag
        """
        pdb.set_trace()
        if lst not in self:
            return False

        ret_lst = []
        for l in lst:
#            ret_lst.append( self.pop(let = l) )
            ret_lst.append( self.remove(l) )

        pdb.set_trace()
        
        print len(self)
        
        if None in ret_lst:
            for tle in ret_lst:
                self.append(tle)
            return False
        else:
            return ret_lst
        
        
    
    def getTileSet(self):
        return set(self.bag_tiles)
    
    def getLetterList(self):
        self._populateLetters()
        return self.letters
    
    def _populateLetters(self):
        self.letters = []
        for t in self.bag_tiles:
            self.letters.append(t.letter)
        pass

    def __contains__(self, item):
        #       ###pdb.set_trace()
       # CHECK THIS IS WORKING
       print "__contains__ called"
       if isinstance(item, Tile):
           for t in self.bag_tiles:
               if item == t:
                   return True
           return False        
       elif isinstance(item,list) and all([isinstance(a,Tile) for a in item]):
           ans = len(item) * [False]
           for i,t in enumerate(item):
               if t in self.bag_tiles:
                   ans[i] = True
           return all(ans)
       elif isinstance(item, str):
           if len(item) >1:
               item = list(item)
           ans = len(item) * [False]
           for i,ltr in enumerate(item):
               if ltr in self.letters:
                   ans[i] = True
                   self.letters.remove(ltr)
           self._populateLetters()
           return all(ans)
       elif isinstance(item, list) and all([a.isalpha() for a in item]):
           ans = len(item) * [False]
           for i,ltr in enumerate(item):
               if ltr in self.letters:
                   ans[i] = True
                   self.letters.remove(ltr)
           self._populateLetters()
           return all(ans)
       else:
            return False
            
     
    def __len__(self):
        return len(self.bag_tiles)
     
    def __iter__(self):
         for t in self.bag_tiles:
             yield t


class Player:
    def __init__(self, p_id, name, p_type):
        self.rack = Bag()
        self.name = name
        self.p_id = p_id
        self.p_type = p_type

    def addTile(self, tile):
        """
        Adds tile to player's rack.
        
        ###### Returns ###### 
        True: Valid Tile Insertion
        False: Invalid Tile Insertion
        
        ###### Usage ###### 
        No Direct Usage  
        """
        if len(self.rack) < 7:
            self.rack.append(tile)
            return True
        else:
            return False
    
    def getRandomTile(self, bag):
        if len(self.rack)<7 and len(bag)>0:
            self.rack.append( bag.getRandomTile() )
            return True
        else:
            return False    
    
    def addBag(self, bag):
        return self.rack.append(bag)

    def printRack(self):
        """
        Show's tile's in player's rack
        
        ###### Returns ###### 
        None
        
        ###### Usage ###### 
        No Direct Usage  
        """
        for t in self.rack:
            print t

    def __str__(self):
        return str(self.name)
    
    def _isValidMove(self, move_tuples):
        """
        Check's that a player has the tiles in rack to make the requested play.
        This is part 1 of 2 of logic for checking validity of a player's move. 
        The other part checks aspects of move validity related to the board
        itself (i.e. valid words formed, spaces occupied/exist, etc.)
        
        ###### Returns ###### 
        True: Valid move
        False: Invalid move
        
        ###### Usage ###### 
        No Direct Usage        
        """
        # ADD LOGIC FOR DEALING WITH BLANK TILES
        
        # Confirm tiles played are in the player's rack and that they are not used multiple times
        try:
            play_letters = [a for (a,b,c) in move_tuples]
        except ValueError:
            # return ValueError: need more than 1 value to unpack
            return False
        
        if not play_letters in self.rack:
            return False

        play_bag = self.rack.getTileFromLetters(play_letters)
        ###pdb.set_trace()
        
        return play_bag
    
class AIPlayer(Player):
    pass


#class Spot:
#    def __init__(self, r_, c_):
#        self.r = r_
#        self.c = c_
#        self.letter = " "
#        self.score = None
#
#    def __str__(self):
#        return str((self.letter, self.score))
#    
#    def insertLetter(self):
#        pass

#class Move:
#    def __init__(self, move_tuple):
#        # of format (letter, row, column)
#        pass

    
class Board:
    def __init__(self):
        self._board_bag = Bag()
        self.board_df = DataFrame()
        self.moves = {}
        self._score_board = DataFrame()
        self._move_num = 1
        self._words_df = DataFrame()

    def __str__(self):  
        ans = "    "
        if COLOR_OUTPUT: ans += Fore.YELLOW
        for i in range(15):
            if i >= 10:
                 ans += "  %s   " % i
            else:
                ans += "  %s    " % i
        ans += "\n"
        if COLOR_OUTPUT:
            ans += Fore.YELLOW
            ans += "   " + 15 * " ______" + "\n"
            for i in range(15):
                ans += "   " + 15 * "|      " + "|\n"
                ans += "   "
                for j in range(15):
                    if (i,j) in self.board_df.index:
#                        ans += ""
                        ans += Fore.YELLOW +"|  " + Fore.RESET + Style.BRIGHT + "%s   " % self.board_df.ix[i,j]['Letter']
                        ans += Fore.YELLOW + Style.NORMAL
                    elif (i,j) in MULT_WORD:
                        ans += "|  %s  " % MULTIPLIERS[MULT_WORD[(i,j)]]
                    elif (i,j) in MULT_LET:
                        ans += "|  %s  " % MULTIPLIERS[MULT_LET[(i,j)]]
                    else:
                        ans += "|      "
                ans += "|\n"
                if i >= 10:
                    ans += "%s " % i
                else:
                    ans += "%s  " % i
                for j in range(15):
                    if (i,j) in self.board_df.index:
                        spot_num = self.board_df.ix[i,j]['Points']
                        if spot_num >= 10:
                            ans += "|    %s" % spot_num
                        else:
                            ans += "|     %s" % spot_num
                    else:
                        ans += "|      "
                ans += "|\n"
                ans += "   " + 15 * "|______" + "|\n"
                ans += Fore.YELLOW
            ans += Fore.RESET + Style.RESET_ALL
        else:
            ans += "   " + 15 * " ______" + "\n"
            for i in range(15):
                ans += "   " + 15 * "|      " + "|\n"
                ans += "   "
                for j in range(15):
                    if (i,j) in self.board_df.index:
                        ans += "|  %s   " % self.board_df.ix[i,j]['Letter']
                    elif (i,j) in MULT_WORD:
                        ans += "|  %s  " % MULTIPLIERS[MULT_WORD[(i,j)]]
                    elif (i,j) in MULT_LET:
                        ans += "|  %s  " % MULTIPLIERS[MULT_LET[(i,j)]]
                    else:
                        ans += "|      "
                ans += "|\n"
                if i >= 10:
                    ans += "%s " % i
                else:
                    ans += "%s  " % i
                for j in range(15):
                    if (i,j) in self.board_df.index:
                        spot_num = self.board_df.ix[i,j]['Points']
                        if spot_num >= 10:
                            ans += "|    %s" % spot_num
                        else:
                            ans += "|     %s" % spot_num
                    else:
                        ans += "|      "
                ans += "|\n"
                ans += "   " +  15 * "|______" + "|\n"
                
        return ans
    
    @staticmethod
    def load(path):
        '''
        For testing
        '''
        try:
            import pickle
            f = open(path, 'r')
            p = pickle.Unpickler(f)
            b = Board()
            b._board = p.load()
            f.close()
            return b
        except:
            return False

    @staticmethod
    def save(inst,path):
        '''
        For testing
        '''
        try:
            import pickle
            f = open(path, 'w')
            p = pickle.Pickler(f)
            p.dump(inst._board)
            f.close()
            return True
        except:
            return False        

    def parseMove(self, move_tuples,  player=None, exchange=False):
        """
        Check's that the player's move is valid with reference to the board.
        This is part 2 of 2 of logic for checking validity of a player's move. 
        The other part checks aspects of move validity related to the player
        itself (i.e. valid tiles played, not too many tiles played, exchanges, etc.)
        
        ###### Inputs ######
        Player:  Player id
        move_tuples:  A list of tuples with elements ordered as letter, row, column
        tile_bag:  ???? What was this supposed to be?
        
        ###### Returns ###### 
        True: Valid Move
        False: Invalid Move
                
        ###### Usage ###### 
        >>> bo = Board() ; test_move = [('m',5,7),('e',6,7),('a',7,7),('t',8,7)] ; bo.parseMove(test_move) ; 
        True
        >>> test_move = [('t', 2, 8), ('r', 3, 8), ('e', 4, 8), ('e', 5, 8)] ; bo.parseMove(test_move)
        True
        >>> test_move = [('s',6,8), ('m', 6, 6), ('s', 6,9)] ; bo.parseMove(test_move)
        True
        >>> test_move = [('a', 4,6), ('i',5,6)]; bo.parseMove(test_move)
        True
        """
        print self.parseMove.__name__
        #pdb.set_trace()()
        # Check validity of move from player's perspective
        pdb.set_trace()
        if player is not None:
            tile_bag = player._isValidMove(move_tuples)
        else:
            tile_bag = None
            
        # Invalid move from player's perspective
        if tile_bag is False:
            print "Tiles not in player's bag"
            return False
        
        
        try:
            moves_df = DataFrame(move_tuples, columns=['Letter', 'Row', 'Column'])
            moves_df.set_index(['Row','Column'], inplace=True, drop=False)
            moves_df['Points'] = [TILE_DICT[let][1] for let in moves_df['Letter']]
        except:
#            print "Spots are occupied"
            if player is not None:
                player.addBag(tile_bag)
            return False
        
        ### How to Determine logic for blank tiles
        
        # Define Orientation of Primary Move (Not ancillary words)
        # Confirm All moves in the same row OR the same column
        # Define the main index (row/col) which the primary words resides in
        orientation = True # True = horizontal, False = vertical
        if (len(moves_df.Row.unique()) == 1):
            orientation = True
            prim_index = moves_df.Row.unique()[0]
            moves_df = moves_df.sort('Column')
        elif (len(moves_df.Column.unique()) == 1):
            orientation = False
            prim_index = moves_df.Column.unique()[0]
            moves_df = moves_df.sort('Row')
        else:
            print "Tiles must be placed same row or column"
            if player is not None:
                player.addBag(tile_bag)
            return False
                    
        if (moves_df.Column.min()<0 or moves_df.Row.min()<0 or moves_df.Column.max()>15 or moves_df.Row.max()>15):
            print "Moves out of bounds"
            if player is not None:
                player.addBag(tile_bag)
            return False
                    
        # Confirm tiles only placed in vacant spots
        try:
            self.board_df.append(moves_df)
        except:
            print "Played space(s) occupied"
            if player is not None:
                player.addBag(tile_bag)
            return False
        
        # Confirm all words created are valid words
        if not self._parseWords(moves_df, orientation, prim_index, tile_bag, player, exchange):
            if player is not None:
                player.addBag(tile_bag)
            return False
        else:
            return True
            
#         self._insert_move(moves_df)
#         return True
    
    def _parseWords(self, moves_df, orientation, prim_index, tile_bag, player, exchange):
        """
        Check's that the player's move is valid with reference to the board.
        This is part 2 of 2 of logic for checking validity of a player's move. 
        The other part checks aspects of move validity related to the player
        itself (i.e. valid tiles played, not too many tiles played, exchanges, etc.)
        
        ###### Inputs ######
        moves_df:  a DataFrame with columns=['Letter', 'Row', 'Column']
        
        ###### Returns ###### 
        DataFrame:  Valid Move(s) with details for scoring
        False: Invalid Move
                
        ###### Usage ###### 
        No direct usage.  Only used by parseMove(.) as a helper function.
        """
        #pdb.set_trace()()
        print self._parseWords.__name__
        require_anc_word = False # for words where only attachment point is via an ancillary word
        found_anc_word = False # boolean indicating an ancillary word found
        temp_board = moves_df.append(self.board_df)
        words_df = DataFrame(columns = ['Row','Column','Letter','WordID', 'Point', 'placed'])
        temp_words_df = DataFrame(columns = ['Row','Column','Letter','WordID', 'LetterPoint', 'ScorePoint', 'placed'])
        
#        placed = True # requires to be global name?  Something not connecting????
        
        if orientation: #Horizontal
            min_i, max_i = min(moves_df.Column), max(moves_df.Column)
            
            # Letters not placed continuously, confirm letter between
            if np.max(Series(moves_df.index.levels[1])) != 1: 
                for i in range(min_i, max_i):
                    if (prim_index, i) not in temp_board.index:
                        return False

            # Get Primary Word                    
            while True:
#                print min_i
                if (prim_index, min_i-1) not in temp_board.index:
                    break
                else:
                    min_i -= 1
            while True:
                if (prim_index, max_i+1) not in temp_board.index:
                    break
                else:
                    max_i += 1
            
            prim_word = ""
            for i in range (min_i, max_i+1):
                if i<0: continue
                let_played = temp_board.ix[prim_index,i]['Letter']
                prim_word += let_played
                if (prim_index,i) in moves_df.index:
                    placed = True
                else:
                    placed = False
                temp_words_df = temp_words_df.append( Series( [prim_index, i, let_played, None, TILE_DICT[let_played][1], TILE_DICT[let_played][1], placed ], index =  ['Row','Column','Letter','WordID', 'LetterPoint', 'ScorePoint', 'placed']), ignore_index=True)
            
            # Check if an ancillary word is required for an attachment point and that the board is not empty
            if (min_i == moves_df.Column.min()) and (max_i == moves_df.Column.max()) and (self.board_df.shape != (0,0)):
                print 'Require Ancillary Word'
                require_anc_word = True
            
            print prim_word
            if prim_word not in WORDS[len(prim_word)]:
                print '%s is not a word' % prim_word
                return False
            else:
                temp_words_df['WordID'] = prim_word
                words_df = words_df.append(temp_words_df, ignore_index=True)
            
            # Get Ancillary Words
            for cc in moves_df.Column:
                temp_words_df = DataFrame(columns = ['Row','Column','Letter','WordID', 'LetterPoint', 'ScorePoint', 'placed'])
                min_i = max_i = prim_index
                while True:
                    if (min_i-1, cc) not in temp_board.index:
                        break
                    else:
                        min_i -= 1
                while True:
                    if (max_i+1, cc) not in temp_board.index:
                        break
                    else:
                        max_i+=1
                        
                if (min_i == max_i == prim_index): # No Ancillary Word Found
                    continue
                else: #ancillary word found
                    found_anc_word = True
                    anc_word = ""
                    for i in range(min_i,max_i+1):
                        let_played = temp_board.ix[i, cc]['Letter']
                        anc_word += let_played
                        if (i,cc) in moves_df.index:
                            placed = True
                        else:       
                            placed = False    
                        temp_words_df = temp_words_df.append( Series( [i, cc, let_played, None, TILE_DICT[let_played][1], TILE_DICT[let_played][1], placed ], index =  ['Row','Column','Letter','WordID', 'LetterPoint', 'ScorePoint', 'placed']), ignore_index=True)
                        
                    print "Ancillary Word is " , anc_word
                    if anc_word not in WORDS[len(anc_word)]:
                        print '%s is not a word' % anc_word
                        return False
                    else:
                        temp_words_df['WordID'] = anc_word
                        words_df = words_df.append(temp_words_df, ignore_index=True)
            
            if require_anc_word and not found_anc_word:
                return False

            
        else: #Vertical
            min_i,max_i = min(moves_df.Row), max(moves_df.Row)
            if np.max(Series(moves_df.index.levels[0])) != 1:
                # Letters not placed continuously, confirm letter between 
                for i in range(min(moves_df.Row), max(moves_df.Row)):
                    if (i,prim_index) not in temp_board.index:
                        return False
                    
            # Find Primary Word
            while True:
#                print min_i
                if (min_i-1, prim_index) not in temp_board.index:
                    break
                else:
                    min_i -= 1
            while True:
                if (max_i+1, prim_index) not in temp_board.index:
                    break
                else:
                    max_i += 1
            
            prim_word = ""
            for i in range (min_i, max_i + 1):
                if i < 0: continue
                let_played = temp_board.ix[i, prim_index]['Letter']
                prim_word += let_played
                if (i, prim_index) in moves_df.index:
                    placed = True
                else:
                    placed = False
                temp_words_df = temp_words_df.append(Series([i, prim_index, let_played, None, TILE_DICT[let_played][1], TILE_DICT[let_played][1], placed ], index=['Row', 'Column', 'Letter', 'WordID', 'LetterPoint', 'ScorePoint', 'placed']), ignore_index=True)
            
            # Check if an ancillary word is required for an attachment point and that the board is not empty
            if (min_i == moves_df.Row.min()) and (max_i == moves_df.Row.max()) and (self.board_df.shape != (0,0)):
                print 'Require Ancillary Word'
                require_anc_word = True
                
            print prim_word
            if prim_word not in WORDS[len(prim_word)]:
                print '%s is not a word' % prim_word
                return False
            else:
                temp_words_df['WordID'] = prim_word
                words_df = words_df.append(temp_words_df, ignore_index=True)
                
            # Get Ancillary Words
            for rr in moves_df.Row:
                temp_words_df = DataFrame(columns = ['Row','Column','Letter','WordID', 'LetterPoint', 'ScorePoint', 'placed'])
                min_i = max_i = prim_index
                while True:
                    if (rr, min_i-1) not in temp_board.index:
                        break
                    else:
                        min_i -= 1
                while True:
                    if (rr, max_i+1) not in temp_board.index:
                        break
                    else:
                        max_i+=1
                        
                if (min_i == max_i == prim_index): # No Ancillary Word Found
                    continue
                else: #ancillary word found
                    found_anc_word = True
                    anc_word = ""
                    for i in range(min_i,max_i+1):
                        let_played = temp_board.ix[rr,i]['Letter']
                        anc_word += let_played
                        if (rr, i) in moves_df.index:
                            placed = True
                        else:
                            placed = False
                        temp_words_df = temp_words_df.append( Series( [rr, i, let_played, None, TILE_DICT[let_played][1],  TILE_DICT[let_played][1], placed ], index =  ['Row','Column','Letter','WordID', 'LetterPoint', 'ScorePoint', 'placed']), ignore_index=True)    
                        
                    print "Ancillary Word is " , anc_word
                    if anc_word not in WORDS[len(anc_word)]:
                        print '%s is not a word' % anc_word
                        return False
                    else:
                        temp_words_df['WordID'] = anc_word
                        words_df = words_df.append(temp_words_df, ignore_index=True)
                        
            if require_anc_word and not found_anc_word:
                return False

        # Return a score value, itself returned as return of calcScore function
        words_df.set_index(['Row','Column','WordID'], inplace=True, drop=False) # results in duplicate keys
#         if self._words_df.shape == (0,0):
#             self._words_df = words_df.copy()
#         else:
#             self._words_df = self._words_df.append(words_df)
#         print words_df
#         
#         print "\n\n"
#         
#         print self._words_df
        if not self._calcScore( moves_df, words_df, player, tile_bag):
            return False
        else:
            return True

    def _calcScore(self, moves_df, words_df, player, tile_bag):
        """
        Manipulates "ScorePoints" column of words_df and passes everything to self._insert_move
        """
        #pdb.set_trace()()
        print self._calcScore.__name__
        
        if not self._insert_move(moves_df, words_df, player, tile_bag):
            return False
        else: 
            return True
    
    def _insert_move(self, moves_df, words_df,  player=None, tile_bag=None):
        """
        moves_df:  a DataFrame with columns Letter, Column, and Row
        
        ##############################################################
        Receives a move as a dataframe, appends this to current board_df.
        Appends move to 'moves' dict.
        updates _board nested lists 
        
        """
        #pdb.set_trace()()
        print self._insert_move.__name__
#         print self._insert_move.__name__
        if player is None:
            moves_df['Player'] = None
        else:
            moves_df['Player'] = player.p_id
        
        moves_df['move_num'] = self._move_num
        words_df['move_num'] = self._move_num
        
        if self._words_df.shape == (0,0):
            self._words_df = words_df.copy()
        else:
            self._words_df = self._words_df.append(words_df)
            
        # Remove - Place holder until points logic inserted here
#         moves_df['Points'] = Series([random.randint(0,15) for i in range(0,moves_df.shape[0])], index = moves_df.index)
        
        if self.board_df.shape != (0,0):
            self.board_df = self.board_df.append(moves_df)
        else:
            self.board_df = moves_df.copy()
        self._move_num += 1
        
        pdb.set_trace()
        self._board_bag.append( tile_bag )
#        Use when support logic ready
#        self._score_board = self._score_board.append()    
        return True

        
class Scrabble:
    """
    Primary Class to play a scrabble game.  May play with 2-4 players.
    Follows all the rules of the original game, with the exception of
    removing challenges (possible future addition).
    
    ###### Usage ###### 
    >>> sc = Scrabble()
    
    """
#    self.players
    # def print_bag():
    #     try:
            
        
    def __init__(self):
        self.players = []
    # Select number of Players    
        # while True:
        #     self.n_players = input("Enter Number of Players (2-4)")
        #     if self.n_players in [2,3,4]:
        #         break
        self.n_players = 2
        self._board = Board()
        
    # Create players types and names
    # Uncomment much of this once finished to allow different player and type configs
        for i in range(self.n_players):
            while True:
                #p_type = raw_input("Enter Player #%i Type [%s]" % (i,PLAYER_TYPE))
                #p_name = raw_input("Enter Player Name")
#                if p_type in PLAYER_TYPE:
                if i == 1:
                    self.players.append(Player(i, "P%i" % i, "AI"))
                else:
                    self.players.append(Player(i, "P%i" % i, "HUMAN"))
                break
                    #self.players.append(Player(i, p_name, p_type))
 #                   break

    # Create Tile Bag
        self.bag = Bag()
        t_id = 0
        for let, (num, scr) in TILE_DICT.iteritems():
            for i in range(num):
                self.bag.append(Tile(let, scr, t_id, 'BAG'))
                t_id += 1
                            
    # Draw Tiles
#        print len(self.bag)
        draw_order = range(self.n_players);random.shuffle(draw_order)
#        print draw_order
        self.play_order = []
#        draw_tiles = random.sample(range(len(self.bag)),self.n_players * range(7))
        for i in draw_order:
            self.play_order.append(self.players[i])
            for j in range(7):
#                print (i,j)
                new_tile = self.bag.getRandomTile()
#                print new_tile
                self.players[i].addTile(new_tile)

        print len(self.bag)

    # Play the Game
        for p in itertools.cycle(self.play_order):
            print self._board
            print p.rack
            print "\n\n"
            print len(self.bag)
            contin = True
            while contin:
                print p.name
                assert self._confirmNumTiles() == 100
                p.printRack()
                print "Please insert move"
                inp = self._getPlayerMove()
#                 ###pdb.set_trace()()
#                inp = "---"               
                if inp == "---":
                    contin = False
                    break
                # submit move
                if self._board.parseMove(move_tuples=inp, player=p):
                    break
                else:
                    continue
#                 
# #                     play_bag = p._isValidMove(inp)
#                 if play_bag:
#                     # if valid from the players perspective, send tiles
#                     if self._board.parseMove(move_tuples=inp, tiles=play_bag,  player=p):
#                         # if valid from board's perspective
#                         # 1) submit play
#                         # 2) add to score
#                         # 3) remove tiles from players rack and transfer to board
#                         # 4) Give player new tiles
#                         continue
#                     else:
#                         p.addBag( play_bag )
#                         # repeat and submit another play   
            print len(self.bag)
            if inp == "---":
                break
            else:
                while True:
#                    pdb.set_trace()
                    if not p.getRandomTile(self.bag):
#                    if not p.addTile(self.bag.getRandomTile()):
                        break
                    
                
        
#     @classmethod
    def _confirmNumTiles(self):
        sum = 0    
        for p in self.players:
            sum += len(p.rack)
        sum += len(self._board._board_bag)
        sum += len(self.bag)
        return sum
            
    def _getPlayerMove(self):
        valid = False
        while not valid:
            try:
                inp = raw_input()
                if inp != "---":
                    inp = eval(inp)
                else:
                    valid=True
            except SyntaxError:
                pass
            
            # input is a list
            try:
                if not isinstance(inp, list):
                    continue
                # input is consisting of tuples
                if not all([isinstance(a,tuple) for a in inp]):
                    continue
                # All elements of tuples are string, int, int
                if not all([all([len(el[0])==1,isinstance(el[0],str), isinstance(el[1],int),isinstance(el[2],int)]) for el in inp]):
                    continue
            except UnboundLocalError:
                continue
            except NameError:
                continue
            
            valid = True
            
        return inp
            
if __name__ == "__main__":
    init() # init colorama
#    import doctest
#    doctest.testmod()

    sc = Scrabble()
    print "\n\nScrabble() init complete\n\n"
    bo = Board()
# #    bo._board[7][6].letter = 't'
# #    bo._board[7][7].letter = 'e'
# #    bo._board[7][8].letter = 's'
# #    bo._board[7][9].letter = 't'
# #    
# #    print bo
# #    print len(sc.bag)
#      
# #    ts = 2 * [None]
# #    ts[0] = Tile('a',1,3,'b')
# #    ts[1] = Tile('c',2,4,'e')
# #    ts.append(Tile('q',1,100,'e'))
# #    b = Bag()
# #    b.append(ts[0])
# #    b.append(ts[1])
# #    b.append(Tile('f', 1,2, 'f'))
# #    b.append(Tile('f', 1,1, 'f'))
# #    s = b.getLetterSet()
# #    test_move = list('ff')
# #    print s.issuperset(test_move)
# #    
# #    print 'q' in b
#  
# #    df = DataFrame({'Letter': list('trees'), 'Row': [2,3,4,5,6], 'Column':[8,8,8,8,8]})
# #    test_move = DataFrame({'Letter': list('meat'), 'Row': [5,6,7,8], 'Column':[7,7,7,7]})
# #    test_move2 = DataFrame({'Letter': list('meats'), 'Row': [5,6,7,8,6], 'Column':[7,7,7,7,8]})
# #    
# #    df = DataFrame({'Letter': list('trees')}, index = zip([2,3,4,5,6],[8,8,8,8,8]))
# #    test_move = DataFrame({'Letter': list('meat')}, index=zip([5,6,7,8],[7,7,7,7]))
# #    test_move2 = DataFrame({'Letter': list('meats')}, index = zip([5,6,7,8,6], [7,7,7,7,8]))
#     print 'Test Parsing Moves'
#     print(bo)
#     test_move = [('m',5,7),('e',6,7),('a',7,7),('t',8,7)]
#     print(bo.parseMove(test_move))
#     print(bo)
#     test_move = [('t', 2, 8), ('r', 3, 8), ('e', 4, 8), ('e', 5, 8)] #, ('s', 6, 8)]
#     print(bo.parseMove(test_move))
#     print(bo)
#     test_move = [('s',6,8), ('m', 6, 6), ('s', 6,9)]
#     print(bo.parseMove(test_move))
#     print(bo)
#     test_move = [('a', 4,6), ('i',5,6)]
#     print(bo.parseMove(test_move))
    print(bo)
    
    
    deinit() # disable colorama
