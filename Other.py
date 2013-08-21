
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