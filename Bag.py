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