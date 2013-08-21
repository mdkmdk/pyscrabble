from Consts import *
from Other import *
from Bag import *
from Player import *
from Board import *

if os.getcwd() == 'N:\\Workspace\\krausm\\Python':
    os.chdir("h:\\scr\\")
    
    
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

