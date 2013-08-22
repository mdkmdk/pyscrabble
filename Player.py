from Bag import *
from Other import *
import pdb

class Player:
    def __init__(self, p_id, name, p_type):
        pdb.set_trace()
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

