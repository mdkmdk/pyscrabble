from Consts import *

class Tile:
    def __init__(self, let, scr, t_id, owner):
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

    def check_move(self, mve):
        pass

    def insert_move(self, mve):
        pass

    def __str__(self):
        ans = 15 * " ___" + "\n"
        for i in range(15):
            for j in range(15):
                ans += "| %s " % self._board[i][j].letter
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
            return False
    
        
    def parseMove(self, player, move_tuples):
        """
        Player:  Player id
        move_tuples:  A list of tuples with elements ordered as letter, row, column
        ##############################################
        
        """
        # Define Orientation of Primary Move (Not ancillary words)
        orientation = True # True = horizontal, False = vertical
        try:
            moves = DataFrame(move_tuples, columns=['Letter', 'Row', 'Column'])
        except:
            return False

        # Confirm tiles played are in the player's rack and that they are not used multiple times
        if not list(moves['Letter']) in player.rack:
            return False
        
        ### How to Determine logic for blank tiles
        
        # Confirm All moves in the same row OR the same column
        # Define the main index (row/col) which the primary words resides in
        if (len(moves.Row.unique()) == 1):
            orientation = True
            prim_index = moves.Row.unique()
        elif (len(moves.Column.unique()) == 1):
            orientation = False
            prim_index = moves.Column.unique()
        else:
            return False
        
#        for 
        
        words_played = []
        tiles_played = []
        attachments = []
            
        # Confirm all words created are valid words
        
        
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
        print len(self.bag)
        draw_order = range(self.n_players);random.shuffle(draw_order)
        print draw_order
        self.play_order = []
#        draw_tiles = random.sample(range(len(self.bag)),self.n_players * range(7))
        for i in draw_order:
            self.play_order.append(self.players[i])
            for j in range(7):
#                print (i,j)
                new_tile = self.bag.getRandomTile()
                print new_tile
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
    print len(sc.bag)
    
    import timeit
    
    ts = 2 * [None]
    ts[0] = Tile('a',1,3,'b')
    ts[1] = Tile('c',2,4,'e')
    ts.append(Tile('q',1,100,'e'))
    b = Bag()
    b.append(ts[0])
    b.append(ts[1])
    b.append(Tile('f', 1,2, 'f'))
    b.append(Tile('f', 1,1, 'f'))
    s = b.getLetterSet()
    test_move = list('ff')
    print s.issuperset(test_move)
    
    print 'q' in b

