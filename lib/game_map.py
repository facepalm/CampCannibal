"""
Map object
"""

import data
import pyglet
from creatures import Bug
from pyglet.gl import *
import game
import random
import mapgen

class Map(object):
    """
    Grid-based map.
    """
    
    def __init__(self, width, height, window, tilesize = 32):
        """
            width, height: dimension in tiles
            background: background image to use
        """
        self.width = width
        self.height = height
        self.tilesize = tilesize
        self.window = window
        self.window_offset = (0, 0)
        self.scroll_dir = (0, 0)
        self.center_target = (0, 0)
        self.grid = [[Tile( (x, y), self) for y in range(height)] for x in range(width)]
        game.state.add_handler(self)

        #Set up tiled background
        self.background = game.image_map['Map'][0].get_texture()

        x_size = self.width * tilesize
        y_size = self.height * tilesize

        

        geom = []
        for x in range(0, x_size, self.background.width):
            for y in range(0, y_size, self.background.height):
                geom.extend((x, y, x+self.background.width, y, x+self.background.width, y+self.background.width, x, y+self.background.width))

        self.bg_geometry = pyglet.graphics.Batch()
        tex = (0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0) * (len(geom)/8)
        self.bg_geometry.add( len(geom)/2, GL_QUADS, None, ('v2f', geom), ('t2f' ,tex))
        score_text = "score: " + str(game.score) 
        self.score = pyglet.text.Label(score_text, color=(200, 0, 0, 255), font_size=15, x = 545, y = 40)

        

    def on_draw(self):
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix() 
        x_off, y_off = self.window_offset
        glTranslatef(x_off, y_off, 0)
        glBindTexture(self.background.target, self.background.id)
        glEnable(self.background.target)
        self.bg_geometry.draw()
        glDisable(self.background.target)

        Tile.tile_batch.draw()
        EffectsManager.effects_batch.draw()
        Bug.bug_batch.draw()

        glPopMatrix()
        score_text = "score: " + str(game.score) 
        glLoadIdentity()
        if game.state.state == 'Start':
            #Wait for someone to press s
            start_screen = pyglet.text.Label("Press S to start", color=(0, 200, 0, 255), 
                        font_size=35, 
                        x = 180,
                        y = 400)
            start_screen.draw()
 
    def populate(self):   
        '''Fill the map with walls and bugs and stuff.'''
        #print len(mapstr),len(mapstr[0])
        self.mapgrid=mapgen.mapgen(self.width,self.height)
        self.mapgrid.print_grid()
        for y in range(self.width):
            for x in range(self.height):
                self.process_tile(self.grid[x][y],self.mapgrid.grid[x][y].char) #the parser should do this now

    def process_tile(self, tile,symbol):
        if symbol=='#': #wall symbol
            game.state.dispatch_event('on_spawn', 'Wall', tile)#spawn wall
        elif symbol=='b': #generic bug
            game.state.dispatch_event('on_spawn', 'Bug', tile)#spawn bug
        elif symbol=='F': #frank
            game.state.dispatch_event('on_spawn', 'Frank', tile)#spawn frank
        elif symbol=='@' and not game.state.player: #unique player
            game.state.dispatch_event('on_spawn', 'Player', tile)#spawn player
            game.state.dispatch_event('on_spawn', 'Portal', tile)#spawn player
        elif symbol=='d' : #unique door
            game.state.dispatch_event('on_spawn', 'Door', tile)#spawn door
        elif symbol=='p' : #portal
            game.state.dispatch_event('on_spawn', 'Portal', tile)#spawn Portal

    def random_tile(self):
        return self.grid[random.randint(0, self.width-1)][random.randint(0, self.height-1)]

    def on_key_press(self, *args):
        symbol, mods = args
        if mods & pyglet.window.key.MOD_SHIFT:
            if symbol == pyglet.window.key.MOTION_UP:
                scroll_x, scroll_y = self.scroll_dir
                scroll_y = 8
                self.scroll_dir = (scroll_x, scroll_y)
                self.center_target = (0, 0)
            if symbol == pyglet.window.key.MOTION_DOWN:
                scroll_x, scroll_y = self.scroll_dir
                scroll_y = -8
                self.scroll_dir = (scroll_x, scroll_y)
                self.center_target = (0, 0)
            if symbol == pyglet.window.key.MOTION_LEFT:
                scroll_x, scroll_y = self.scroll_dir
                scroll_x = -8
                self.scroll_dir = (scroll_x, scroll_y)
                self.center_target = (0, 0)
            if symbol == pyglet.window.key.MOTION_RIGHT:
                scroll_x, scroll_y = self.scroll_dir
                scroll_x = 8
                self.scroll_dir = (scroll_x, scroll_y)
                self.center_target = (0, 0)

    def on_key_release(self, *args):
        symbol, mods = args
        if symbol == pyglet.window.key.LSHIFT or symbol == pyglet.window.key.RSHIFT:
            self.scroll_dir = (0, 0)
        if mods & pyglet.window.key.MOD_SHIFT:
            if symbol == pyglet.window.key.MOTION_UP or symbol == pyglet.window.key.MOTION_DOWN:
                scroll_x, scroll_y = self.scroll_dir
                self.scroll_dir = (scroll_x, 0)
            if symbol == pyglet.window.key.MOTION_LEFT or symbol == pyglet.window.key.MOTION_RIGHT:
                scroll_x, scroll_y = self.scroll_dir
                self.scroll_dir = (0, scroll_y)

    def on_update(self, dt):
        scroll_x, scroll_y = self.scroll_dir
        if scroll_x or scroll_y:
            self.scroll(scroll_x, scroll_y)

        tx, ty = self.center_target
        ox, oy = self.window_offset
        if tx or ty:
            x_scroll = cmp(tx, 0)*4
            y_scroll = cmp(ty, 0)*4
            self.scroll(x_scroll, y_scroll)
            tx -= x_scroll
            ty -= y_scroll
            if abs(tx) < 4:
                tx = 0
            if abs(ty) < 4:
                ty = 0
            self.center_target = (tx, ty)

    def scroll(self, x, y):
        x_off, y_off = self.window_offset
        w, h = self.window.get_size()

        if (x < 0 and x_off - x <= 0) or (x > 0 and x_off - x >= -(self.width * self.tilesize - w)):
            x_off -= x

        if (y < 0 and y_off - y <= 0) or (y > 0 and y_off - y >= -(self.height * self.tilesize - h)):
            y_off -= y

        self.window_offset = (x_off, y_off)

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


class EffectsManager(object):
    effects_batch = pyglet.graphics.Batch()

    def __init__(self):
        self.splats = game.image_map['Splats']
        self.burrow = game.image_map['Burrow'][0]
        self.active_sprites = []
        game.state.add_handler(self)

    def draw_splat(self, x, y, color=(255, 0, 0)):
        splat_sprites = [pyglet.sprite.Sprite(self.splats[0], random.gauss(x, 8), random.gauss(y, 8), batch=self.effects_batch) for i in range(8)]
        for sprite in splat_sprites:
            sprite.color = color
            sprite.time = 0
            sprite.opacity = 255 - random.randint(0, 20)
            sprite.rotation = random.randint(0, 300)
            sprite.scale = 1.0 - random.gauss(0.0, 0.2)
        self.active_sprites.extend(splat_sprites)

    def draw_burrow(self, tile):
        x, y = tile.position
        burrow_sprite = pyglet.sprite.Sprite(self.burrow, x*32+16, y*32+16, batch = self.effects_batch)
        burrow_sprite.time = 0
        self.active_sprites.append(burrow_sprite)

    def on_update(self, dt):
        for sprite in self.active_sprites:
            sprite.time += dt
            if sprite.time > 1:
                sprite.opacity -= 1
                if sprite.opacity == 0:
                    self.active_sprites.remove(sprite)
                    sprite.delete()
