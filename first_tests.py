
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
        if x not in self.bag_tiles:
            self.bag_tiles.append(x)
            self._populateLetters()
        else:
            return False

    def remove(self, tile):
        try:
            self.bag_tiles.remove(tile)
        except ValueError:
            return False
        else:
            self._populateLetters()
            return True

    def pop(self, t_id=None, let=None):
        if t_id is not None:
            for t in self.bag_tiles:
                if t_id == t.t_id:
                    self.remove(t)
                    return t
            return None
        elif let is not None:
            for t in self.bag_tiles:
                if t.letter == let:
                    self.remove(t)
                    return t
                return None 
        else:
            return None

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
        #       pdb.set_trace()
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
         pass


class Player:
    def __init__(self, p_id, name, p_type):
        self.rack = Bag()
        self.name = name
        self.p_id = p_id
        self.p_type = p_type

    def addTile(self, tile):
        if len(self.rack) < 7:
            self.rack.append(tile)
            return
        else:
            return - 1

    def printRack(self):
        for t in self.rack:
            print t

    def __str__(self):
        return str(self.name)
    
    def isValidMove(self, move_tuples):
        # ADD LOGIC FOR DEALING WITH BLANK TILES
        
        # Confirm tiles played are in the player's rack and that they are not used multiple times
        try:
            play_letters = [a for (a,b,c) in move_tuples]
        except ValueError:
            # return ValueError: need more than 1 value to unpack
            return False
        
        if not play_letters in self.rack:
            return False
        
        return True
    
class AIPlayer(Player):
    pass


class Spot:
    def __init__(self, r_, c_):
        self.r = r_
        self.c = c_
        self.letter = " "
        self.score = None

    def __str__(self):
        return str((self.letter, self.score))
    
    def insertLetter(self):
        pass

class Move:
    def __init__(self, move_tuple):
        # of format (letter, row, column)
        pass


    
class Board:
    BOARD_SIZE = 15
    def __init__(self):
        self._board = 15 * [[]]
        for i in range(15):
            self._board[i] = []
            for j in range(15):
                self._board[i].append(Spot(i, j))
#               self._board[i].append(None)
#        self.board_df = DataFrame([(a,b, None, np.nan) for a in range(0,15) for b in range(0,15)], columns=['Row','Column','Letter', 't_id'])
        self.board_df = DataFrame()
        self.moves = {}

    def check_move(self, mve):
        pass

    def _insert_move(self, moves_df, player=None, move_num=None):
        """
        moves_df:  a DataFrame with columns Letter, Column, and Row
        
        ##############################################################
        Receives a move as a dataframe, appends this to current board_df.
        Appends move to 'moves' dict.
        updates _board nested lists 
        
        """
        if player is None:
            moves_df['Player'] = None
        else:
            moves_df['Player'] = player.p_id
        
        if move_num is None:
            moves_df['move_num'] = None
        else:
            moves_df['move_num'] = move_num
                   
        self.board_df = self.board_df.append(moves_df)    
        return True

    def __str__(self):      
        ans = 15 * " ___" + "\n"
        for i in range(15):
            for j in range(15):
                if (i,j) in self.board_df.index:
                    ans += "| %s " % self.board_df.ix[i,j]['Letter']
                else:
                    ans += "|   "
            ans += "|\n"
            ans += 15 * "|___" + "|\n"
#        for i in range(15):
            # ans+= "\n" + 15* "|   " + "|"
            # ans+= "\n" + 15* "|___" + "|"
        return ans

#    def getSpotLetter(self, r_, c_):
#        let = self._board[r][c].letter
#        if let == " ":
#            return None
#        else:
#            return let
    
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
            return Fals        

    def parseMove(self, move_tuples, player=None):
        """
        Player:  Player id
        move_tuples:  A list of tuples with elements ordered as letter, row, column
        ##############################################
        
        """
        orientation = True # True = horizontal, False = vertical
        try:
            moves = DataFrame(move_tuples, columns=['Letter', 'Row', 'Column'])
            moves.set_index(['Row','Column'], inplace=True, drop=False)
        except:
            return False
        
        ### How to Determine logic for blank tiles
        
        # Define Orientation of Primary Move (Not ancillary words)
        # Confirm All moves in the same row OR the same column
        # Define the main index (row/col) which the primary words resides in
        if (len(moves.Row.unique()) == 1):
            orientation = True
            prim_index = moves.Row.unique()[0]
            moves = moves.sort('Column')
        elif (len(moves.Column.unique()) == 1):
            orientation = False
            prim_index = moves.Column.unique()[0]
            moves = moves.sort('Row')
        else:
            return False
                    
        # Confirm tiles only placed in vacant spots
        try:
            self.board_df.append(moves)
        except:
            return False
        
        if not self._parseWords(moves, orientation, prim_index):
            return False
        
        words_played = []
        tiles_played = []
        attachments = []
            
        # Confirm all words created are valid words
        self._insert_move(moves)
        return True
    
    def _parseWords(self, moves, orientation, prim_index):
        
        temp_board = moves.append(self.board_df)
        
        if orientation:
            #Horizontal
            min_i, max_i = min(moves.Column), max(moves.Column)
            if np.max(Series(moves.index.levels[1])) != 1:
                # Letters not placed continuously, confirm letter between 
                for i in range(min_i, max_i):
                    if (prim_index, i) not in temp_board.index:
                        return False
                    
            while True:
                print min_i
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
                prim_word += temp_board.ix[prim_index,i]['Letter']
                
            print prim_word
            if prim_word not in WORDS[len(prim_word)]:
                print '%s is not a word' % prim_word
                return False
                
            
            
        else:
           #Vertical
            min_i,max_i = min(moves.Row), max(moves.Row)
            if np.max(Series(moves.index.levels[0])) != 1:
                # Letters not placed continuously, confirm letter between 
                for i in range(min(moves.Row), max(moves.Row)):
                    if (i,prim_index) not in temp_board.index:
                        return False
                    
            # Find Primary Word
            while True:
                print min_i
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
            for i in range (min_i, max_i+1):
                if i<0: continue
                prim_word += temp_board.ix[i, prim_index]['Letter']
                
            print prim_word
            if prim_word not in WORDS[len(prim_word)]:
                print '%s is not a word' % prim_word
                return False
            
        return True
        
class Scrabble:
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
        self.n_players = 4
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

    # Play the Game
        contin = True
        for p in itertools.cycle(self.play_order):
            while contin:
                print p
#                inp = raw_input()
                inp = "---"               
                if inp == "---":
                    contin = False
                elif inp == 'abc':
                    break
                if p.isValidMove(inp):
                    if self._board.parseMove(move_tuples=inp, player=p):
                        continue
            if inp == "---":
                break
        
            
if __name__ == "__main__":

    sc = Scrabble()
    bo = Board()
#    bo._board[7][6].letter = 't'
#    bo._board[7][7].letter = 'e'
#    bo._board[7][8].letter = 's'
#    bo._board[7][9].letter = 't'
#    
#    print bo
#    print len(sc.bag)
    
#    ts = 2 * [None]
#    ts[0] = Tile('a',1,3,'b')
#    ts[1] = Tile('c',2,4,'e')
#    ts.append(Tile('q',1,100,'e'))
#    b = Bag()
#    b.append(ts[0])
#    b.append(ts[1])
#    b.append(Tile('f', 1,2, 'f'))
#    b.append(Tile('f', 1,1, 'f'))
#    s = b.getLetterSet()
#    test_move = list('ff')
#    print s.issuperset(test_move)
#    
#    print 'q' in b

#    df = DataFrame({'Letter': list('trees'), 'Row': [2,3,4,5,6], 'Column':[8,8,8,8,8]})
#    test_move = DataFrame({'Letter': list('meat'), 'Row': [5,6,7,8], 'Column':[7,7,7,7]})
#    test_move2 = DataFrame({'Letter': list('meats'), 'Row': [5,6,7,8,6], 'Column':[7,7,7,7,8]})
#    
#    df = DataFrame({'Letter': list('trees')}, index = zip([2,3,4,5,6],[8,8,8,8,8]))
#    test_move = DataFrame({'Letter': list('meat')}, index=zip([5,6,7,8],[7,7,7,7]))
#    test_move2 = DataFrame({'Letter': list('meats')}, index = zip([5,6,7,8,6], [7,7,7,7,8]))
    print 'Test Parsing Moves'
    test_move = [('m',5,7),('e',6,7),('a',7,7),('t',8,7)]
    print bo.parseMove(test_move)
    print bo
    test_move = [('t', 2, 8), ('r', 3, 8), ('e', 4, 8), ('e', 5, 8)] #, ('s', 6, 8)]
    print bo.parseMove(test_move)
    print bo
    test_move = [('s',6,8), ('m', 6, 6), ('s', 6,9)]
    print bo.parseMove(test_move)
    print bo 
    test_move = [('a', 4,6), ('i',5,6)]
    print bo.parseMove(test_move)
    print bo 
    
    