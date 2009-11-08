from pyglet.window import key
import animatedsprite
from pyglet.gl import *
from pyglet.sprite import Sprite
import math

class Spawn():
    '''Class that Handles spawning creatures'''
    MAX_SPAWN_RATE = 1 # maximum number to spawn per second
    MAX_COUNT   = 1 #Maximum number of bugs
    def __init__(self, game_data):
        self.game           = game_data["game"]
        self.game.add_handler(self)
        self.game_data      = game_data

        #Map string names to classes
        self.spawn_map   = {
          'Wall'    : Wall,
          }

    def on_spawn(self, spawn_what, tile):
        '''listens for spawn create/object events'''
        if spawn_what in self.spawn_map:
            unit_class = self.spawn_map[spawn_what]
            u=unit_class(tile=tile, game_data=self.game_data) 
            tile.contents.append(u)
'''
class Thing(Sprite):
    thing_batch = pyglet.graphics.Batch()
    def __init
'''
class Wall(object):
    object_batch  = pyglet.graphics.Batch()
    def __init__(self, tile, game_data):
            self.game                           = game_data["game"]
            self.game_data                      = game_data
            self.sprite         = pyglet.sprite.Sprite(self.game_data['data']['map']['elements']['House01']['Wall6.png'], 0, 0, batch=self.object_batch)
            self.tile                           = tile 
            self.width                          = self.sprite.width
            self.height                         = self.sprite.height
            x, y                                = self.tile.position
            self.centerx                    = (x+0.5)*self.tile.return_tile_size()
            self.centery                    = (y+0.5)*self.tile.return_tile_size() 
            self.sprite.x                       = self.left
            self.sprite.y                       = self.bottom 
            self.game.add_handler(self)

    @property
    def left(self):
        return self.centerx - (self.width // 2)

    @property
    def right(self):
        return self.centerx +  (self.width // 2)
        
    @property
    def top(self):
        return self.centery + (self.height // 2)

    @property
    def bottom(self):
        return self.centery -  (self.height // 2)


