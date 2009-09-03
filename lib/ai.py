import random
import game
import math

class Mind():
    def __init__(self,choice=None):
        self.strat_list= ['Random','LazyFollow']
        if choice and choice in self.strat_list:
            self.strat = choice
        else:
            self.strat=random.choice(self.strat_list)
    
    def choose_tile(self,tile_list,fleeing=False):
        if len(tile_list)==0:
            return None
        if len(tile_list)==1:
            return tile_list[0]
        if self.strat=='Random': #random tile choice
            return random.choice(tile_list)
        if self.strat=='LazyFollow': #pick the tile closest to the player
            pref_tile=None
            for t in tile_list:
                if not pref_tile or self.dist(t.position,game.state.player.tile.position) < self.dist(pref_tile.position,game.state.player.tile.position):
                    pref_tile=t     
            return pref_tile        
                
    def dist(self,pos1,pos2,func='Absolute'):
        if func=='Manhattan':
            return math.fabs(pos2[0]-pos1[0])+math.fabs(pos2[1]-pos1[1])
        elif func == 'Absolute':
            return math.pow(math.fabs(pos2[0]-pos1[0]),2)+math.pow(math.fabs(pos2[1]-pos1[1]),2)
        return 10000 #some arbitrarily high number            
