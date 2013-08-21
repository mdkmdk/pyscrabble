from Consts import *

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
        
        