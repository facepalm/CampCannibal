"""
Map object
"""

import pyglet
from pyglet.gl import *
import random
import mapgen

class Map(object):
    """
    Grid-based map.
    """
    
    def __init__(self, width, height, game_data, tilesize = 32):
        """
            width, height: dimension in tiles
            background: background image to use
        """
        self.width          = width
        self.height         = height
        self.tilesize       = tilesize
        self.window         = game_data["window"]
        self.window_offset  = (0, 0)
        self.scroll_dir     = (0, 0)
        self.center_target  = (0, 0)
        self.grid           = [[Tile( (x, y), self) for y in range(height)] for x in range(width)]
        self.game           = game_data["game"]
        self.game.add_handler(self)
        self.game_data      = game_data
        x_size = self.width * tilesize
        y_size = self.height * tilesize
        self.tile_map       = {'#' :  'Wall',
         'b' : 'Bug',
         'F' : 'Frank',
         '@' : 'Player',
         'd' : 'Door',
         'p' : 'Portal',
          }

    def populate(self):   
        '''Fill the map with walls and bugs and stuff.'''
        self.mapgrid=mapgen.mapgen(self.width,self.height)
        self.mapgrid.load(self.game_data['data']['map']['description']['map.txt'])
        self.game_data['data']['map']['description']['map.txt'] = self.mapgrid
        for y in range(self.width):
            for x in range(self.height):
                self.process_tile(self.grid[x][y],self.mapgrid.grid[x][y].char) #the parser should do this now

    def process_tile(self, tile,symbol):
       if symbol in self.tile_map: 
           self.game.dispatch_event('on_spawn', self.tile_map[symbol], tile)
       else:
           #Print/return error?
           pass

    def random_tile(self):
        return self.grid[random.randint(0, self.width-1)][random.randint(0, self.height-1)]

    def tile_from_coords(self,coords):
        try:
            return self.grid[int(coords[0])/self.tilesize][int(coords[1])/self.tilesize]
        except:
            return None

    def set_center(self, x, y):
        w, h = self.window.get_size()

        ox, oy = self.window_offset
        tx, ty = self.center_target

        tx = x- (w/2) + ox
        ty = y - (h/2) + oy
        if abs(tx) < 4:
            tx = 0
        if abs(ty) < 4:
            ty = 0
        self.center_target = (tx, ty)

class Tile(object):
    """Single map tile"""

    tile_batch = pyglet.graphics.Batch()

    def __init__(self, position, map, background = None):
        self.map = map
        self.position = position
        #Things on this tile
        self.contents = []

        if background:
            x, y = self.position
            self.background = pyglet.sprite.Sprite(game.images[background], x*self.map.tilesize, y*self.map.tilesize, batch = self.tile_batch)            

    def up(self):
        """Tile above this one"""
        x, y = self.position
        if y == 0:
            return None
        return self.map.grid[x][y-1]

    def down(self):
        """Tile below this one"""
        x, y = self.position
        if y == self.map.height - 1:
            return None
        return self.map.grid[x][y+1]

    def left(self):
        """Tile left of this one"""
        x, y = self.position
        if x == 0:
            return None
        return self.map.grid[x-1][y]

    def right(self):
        """Tile right of this one"""
        x, y = self.position
        if x == self.map.width - 1:
            return None
        return self.map.grid[x+1][y]

    def neighbors(self):
        """All tiles around this one"""
        neigh=[]
        bores=[self.up(),self.down(),self.left(),self.right()]
        for b in bores:
            if b != None:
                neigh.append(b)
        return neigh

    def is_empty(self):
        return self.contents==[] #I think that will work

    def return_tile_size(self):
        return self.map.tilesize
