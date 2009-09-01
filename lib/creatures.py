import math
import os
from pyglet.gl import *
import game
import data
import random
import mapgen
import ai

class Spawn():
    '''Class that Handles spawning creatures'''
    MAX_SPAWN_RATE = 1 # maximum number to spawn per second
    MAX_COUNT   = 1 #Maximum number of bugs
    def __init__(self):
        self.interval       = 0
        self.bugs           = []
        #Map string names to classes
        self.spawn_map   = {
          'Portal'  : Portal,
          'Door'    : Door,
          'Wall'    : Wall,
          'Bug'     : Bug,
          'Player'  : Player,
          }

        self.color_map = {
         
          'Red'      : (144,30,9),#
          'Blue'     : (0,5,148),#
          'Violet'   : (127,5,235),#
          'Orange'   : (204,118,12),#
          'Pink'     : (244,71,145),#
          'Yellow'   : (181,255,30),#
          'Turquoise': (22,119,184),#
          'Grey'     : (118,128,105),#
          'White'    : (255,250,250),
          'Black'    : (38,30,33),#
          'Green'    : (7,217,0),#
          'Brown'    : (111,85,7),#
          }

        self.speed_map = {
          'Slow'    : 1,
          'Medium'  : 2,
          'Fast'    : 3,
          }

        self.key              = {'Name': 'Key',    'Number': 1, 'Color': self.color_map['Blue'],  'Speed': self.speed_map['Fast'],  'Count': 0, 'Beats': ('Color4', 'Color3'), 'Score': 15 } #key bugs
        #Number of first group of bugs that can kill the key bug
        self.color_1          = {'Name': 'Color1', 'Number': 2, 'Color': self.color_map['Green'], 'Speed': self.speed_map['Medium'],'Count': 0, 'Beats': ('Key', 'Color4'), 'Score': 10  } 
        #Number of second group of bugs that can kill the key bug
        self.color_2          = {'Name': 'Color2', 'Number': 3, 'Color': self.color_map['White'], 'Speed': self.speed_map['Medium'],'Count': 0, 'Beats': ('Color1', 'Key'), 'Score': 5  } 
        self.color_3          = {'Name': 'Color3', 'Number': 4, 'Color': self.color_map['Yellow'],'Speed': self.speed_map['Slow'],  'Count': 0, 'Beats': ('Color2', 'Color1'), 'Score': 3 } #Rest of the bugs.
        self.color_4          = {'Name': 'Color4', 'Number': 5, 'Color': self.color_map['Red'], 'Speed': self.speed_map['Slow'],  'Count': 0, 'Beats': ('Color3', 'Color2'), 'Score': 2   }#Rest of the bugs.

        self.bug_spawn_map = {
          'Key':       self.key,
          'Color1':    self.color_1,
          'Color2':    self.color_2,
          'Color3':    self.color_3,
          'Color4':    self.color_4,
          }

        #Shuffle the creature colors when the spawn class gets instanciated.
        self.shuffle_bug_map()

    def get_color_bug(self, bug_name):
        return self.bug_spawn_map[bug_name]['Color']

    def set_player_color(self, state):
        #Select random color for player that is not the key bug
        state.set_player_color(self.color_4['Color'], self.bug_spawn_map[self.color_4['Beats'][0]]['Color'], self.bug_spawn_map[self.color_4['Beats'][1]]['Color'])

    def shuffle_bug_map(self):
        '''Function to shuffle colors in the bug_spawn_map'''
        #create set of 5 random colors.
        colors = set()
        while len(colors) < 5:
            colors.add(random.choice(self.color_map.keys()))

        #Assign colors to the different bugs
        for bug, map in self.bug_spawn_map.iteritems():
            map['Color'] = self.color_map[colors.pop()]

    def on_update(self, dt):
        pass

    #I think I should move this into on_update? 
    def spawn(self, dt):
        '''Function which will spawn some random creature on the board'''
        #I want a random interval for spawning. I want to randomly select a bug  to spawn.
        g=game.map.grid[max(0,game.state.player.tile.position[0]-10):min(game.state.player.tile.position[0]+10,game.map.width-1)]
        g=[m[max(0,game.state.player.tile.position[1]-10):min(game.state.player.tile.position[1]+10,game.map.height-1)] for m in g]
        space_tiles=filter(lambda x: x.contents == [],mapgen.flatten(g))   
        sp=random.choice(space_tiles)
        self.on_spawn('Bug', game.map.grid[sp.position[0]][sp.position[1]])
        
    def on_spawn(self, spawn_what, tile):
        '''listens for spawn create/object events'''
        unit_class = self.spawn_map[spawn_what]#grab the class of the requested object (i.e wall, bug, etc)
        if spawn_what == 'Player':
            x, y = tile.position
            u=unit_class(x*32+16, y*32+16, 32, 32, tile=tile, bug_map=self.bug_spawn_map['Color4']) 
            game.state.player=u
            self.set_player_color(game.state)

class Creature(object):
    """Sprite-based creature on the map
       (CCB) Bug / wall behavior was getting different enough that I 
        factored them out into separate subclasses.
    """
    bug_batch = pyglet.graphics.Batch()
    
    #States that a bug can be in
    STOPPED     = 0 
    MOVING      = 1
    
    def __init__(self, centerx, centery, width, height, tile=None, color=None, direction = 1, speed = 1, bug_map = None, bug_spawn_map = None):

            self.name       = None #Figure out If I need this
            self.beats      = None
            #Come up with a better way to manage images for Creatures
            self.images         = self.get_images()
            self.image_index    = 0
            self.direction      = direction #Probably should make this an x/y vector but then again, this is a grid that allows for no diagonal movement
            self.speed          = speed
            self.beginingx     = None
            self.beginingy     = None
            self.destinationx  = None
            self.destinationy  = None
            self.centerx        = centerx
            self.centery        = centery
            self.width          = width#This number will most likely be derived from images passed in? 
            self.height         = height
            self.tile           = tile #the tile this bug is standing on.  If None, it's floating in limbo
            self.last_tile      = tile #the last tile this bug was standing on.  Used to prevent u-turns.
            self.sprite         = pyglet.sprite.Sprite(self.images[0], 0, 0, batch=self.bug_batch)
            x, y                = self.tile.position
            self.sprite.x       = x*32
            self.sprite.y       = y*32
            self.color          = color
            self.bug_map        = bug_map

            if self.bug_map != None:
                self.speed  = self.bug_map['Speed']
                self.color  = self.bug_map['Color']
                self.name   = self.bug_map['Name'] 
                self.beats  = self.bug_map['Beats']
                
            if self.color:
                self.sprite.color   = self.color
            self.state          = self.STOPPED
            self.time           = 0
            game.state.add_handler(self)
           
    def get_images(self):
        pass
        
    def next_image(self):
        if len(self.images) > 1:
            self.image_index = (self.image_index+1)%len(self.images)
            self.sprite.image = self.images[self.image_index]
            
            
    def die(self):
        if not self.alive:
            return
        self.alive = False
        self.state = self.STOPPED
        self.spritex = self.sprite.x
        self.spritey = self.sprite.y
        game.score += self.bug_map['Score']
        print "Current score: ", game.score
        try:#Prevent error on double deletion
            if not isinstance(self,Player):
                self.sprite.delete()            
        except:
            print 'Double delete caught'
    
class Bug(Creature):
    """This class represent a bug. Player object will be a subclass of bug"""

    def __init__(self, *args, **kwargs):
        super(Bug, self).__init__(*args, **kwargs)
        #adujust for centered anchor point (for rotation)
        self.ai=ai.Mind()
        
        self.sprite.x += self.sprite.width // 2
        self.sprite.y += self.sprite.height // 2
        self.alive = True
        
    def get_images(self):
        return game.image_map['Bug']

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

    def collide_neighbors(self):
        collidables = []
        map(lambda x: collidables.extend(x.contents), self.tile.neighbors())
        collidables = [i for i in collidables if (isinstance(i, Player)  or isinstance(i, Bug))]
        for c in collidables:
            if ((self.left >= c.left and self.left < c.right) or (self.right > c.left and self.right <= c.right)) and \
                ((self.top > c.bottom and self.top <= c.top) or (self.bottom < c.top and self.bottom >= c.bottom)):
                    self.resolve_collision(c)
                    #print 'bug collided', c

    def on_update(self, dt):
        '''Update sprites postion/state'''
        if not self.alive:
            return
        self.collide_neighbors()    
        if self.state != self.MOVING:
            #maybe check if we're still alive at this point
            if not isinstance(self,Player) and random.random() < 0.02:
                self.warp_to_random_tile()
            self.move()            
        if self.state == self.MOVING:
            self.time += 1
            changex		= self.destinationx - self.beginingx
            changey		= self.destinationy - self.beginingy
            duration	= math.sqrt( (changex * changex) + (changey * changey))//self.speed
            if not (self.time > duration):
                self.centerx 		= self.linear_tween(self.time, duration, changex, self.beginingx)
                self.centery 		= self.linear_tween(self.time, duration, changey, self.beginingy)
                self.sprite.x		= self.right
                self.sprite.y		= self.top
                if isinstance(self, Player):
                    game.map.set_center( self.centerx, self.centery)
            else:
                self.state = self.STOPPED
        if self.time % 5 == 0 and self.state != self.STOPPED:
            self.next_image()
        #if not isinstance(self,Player) and random.random() < 0.0005:
        #    self.die()

    def warp_to_random_tile(self):
        old_t = self.tile 
        t = game.map.random_tile()
        while t.contents:
            t = game.map.random_tile()
        game.effects.draw_burrow(t)
        game.effects.draw_burrow(old_t)        
        mp = game.sounds['dig.wav'].play()
        mp.pitch += random.gauss(0.05, 0.05)
        self.tile = t

    def move(self):
        all_neighbors=self.tile.neighbors() #get surrounding squares
        valid_neighbors=[]
        if self.last_tile in all_neighbors: #remove the most recent square
            all_neighbors.remove(self.last_tile)     
        for n in all_neighbors:
            if not self.check_occlusion(n):
                valid_neighbors.append(n)   
        if len(valid_neighbors) >= 1: #do we have at least one square to move to?
            self.move_to_tile( self.ai.choose_tile(valid_neighbors) ) #pick tile at random to move into, brads AI of doom is going to use this: python mouse brain scanning at work!
        else: #we must be trapped.  
            self.last_tile=self.tile #Update last_tile to reflect this

    def move_to_dest(self, dest):
        '''Function calls linear tween and makes bugs move nicely. Not implemented yet'''
        x, y   = self.tile.position
        x1, y1 = dest.position
        self.destinationx = x1*32
        self.destinationy = y1*32
        self.beginingx    = x*32
        self.beginingy    = y*32
        self.time = 0
        self.last_tile = self.tile
        self.tile = dest
        self.state = self.MOVING
        self.set_rotation()
 
    def linear_tween(self, t, d, c, b):
        '''
        function used to make movement of bugs look smooth
        t = time, d = duration, c = changes in position, b = begin position
        '''
        return c*t//d + b

    def check_occlusion(self, target_tile):
        '''If something is in the tile, do not move into it.
        perhaps later, return the object in the tile'''
        for c in target_tile.contents:
            if self.check_blocked(c):
                return True
        return False

    def move_to_tile(self, target_tile):
        '''Check that a given tile is free to move into'''
        #May want to put code in here, to parse what was on tile and decide what to do
        if self.check_occlusion(target_tile):#check for blocking collisions
            return False #fail
        else:
            if self in self.tile.contents:
                 self.tile.contents.remove(self)#Remove from current tile
            self.move_to_dest(target_tile) #Go to this tile 
            target_tile.contents.append(self)#add to the dest tile
            if len([i for i in target_tile.contents if isinstance(i, Portal)]):
                game.sounds['squish.wav'].play()
            return True

    def check_blocked(self,other):
        if self==other: #if we are the other bug as well, we don't need to bother
            return False
        if isinstance(other, Portal):#Objects of the same color can pass through portals.
            if self.color == other.color:
                return False
            else:
                return True
        if isinstance(self, Player) and isinstance(other, Door):#Doors block us from moving, I need a check for player color
            if self.color == other.color:

                game.state.state = 'GameOver'
                print "Game over man"
                return False
            else:
                return True
            return True #There is a blockage
        if isinstance(other, Door):
            return True
        if isinstance(other, Wall):#walls block us from moving
            return True #There is a blockage
        if isinstance(self, Player) and isinstance(other, Bug): #player can hit bugs
            return False
        if isinstance(self, Bug) and isinstance(other, Player): #bugs can hit player
            return False
        if isinstance(self, Bug) and isinstance(other, Bug): #bugs block other bugs
            return True
        return False #there is NOT a blockage with whatever object this is
    
    def check_collision(self,other):        
        '''Function for handling non-blocking collisions (attacks and stuff)'''
        if self==other: #possibly useful for masochism-based attacks
            return
        if isinstance(self, Player) and isinstance(other, Bug): #player can hit bugs            
            #Color-based damage
            self.resolve_collision(other)
        if isinstance(self, Bug) and isinstance(other, Player): #bugs can hit player
            #color-based damage
            self.resolve_collision(other)
            
    def resolve_collision(self,other):
        if not other.alive:
            return
        if other.name in self.beats:
            #they die
            if isinstance(self, Player):# player_color, color1, color2):
                game.state.dispatch_event('on_set_player_color', other.bug_map['Color'],  game.state.get_color_bug(other.bug_map['Beats'][0]), game.state.get_color_bug(other.bug_map['Beats'][1]))
                print "Bug dies! Change player color to", self.bug_map['Color'], " Beats: ",self.bug_map['Beats'][0], " and: ", self.bug_map['Beats'][1]
                other.die()
                self.bug_map = other.bug_map
                self.beats  = self.bug_map['Beats']
        #elif self.name in other.beats:
        elif other.color != self.color and isinstance(self, Player):
            #print other.color, self.color
            #I die
            #if isinstance(self, Player):
            self.die()
            #print "Player dies!"    
            
    def set_rotation(self):
        """Set sprite's rotation, based off of our current and last tile"""
        x_c, y_c = self.tile.position
        x_o, y_o = self.last_tile.position        
        dx = x_c - x_o
        dy = y_c - y_o
        
        if dx == 1:
            self.sprite.rotation = 90
        elif dx == -1:
            self.sprite.rotation = 270
        elif dy == 1:
            self.sprite.rotation = 0
        elif dy == -1:
            self.sprite.rotation = 180
            
    def die(self):
        super(Bug, self).die()
        #x, y = self.tile.position        
        #game.effects.draw_splat(x*32+16, y*32+16, color=(0, 255, 0))        
        game.number_of_bugs -= 1
        self.bug_map['Count'] -= 1
        self.draw_death()
        self.deathsound()
        if isinstance(self,Player):
            self.alive=True
            player_space=filter(lambda x: x.char == '@',mapgen.flatten(game.map.mapgrid.grid))              
            t=random.choice(player_space)
            self.tile = game.map.grid[t.x][t.y]
            #self.kill_all_bugs()                             
            x, y   = self.tile.position
            self.sprite.x       = x*32+16
            self.sprite.y       = y*32+16
                

    #broken atm
    def kill_all_bugs(self):
        for i in game.map.grid:
            for j in i:
                for c in j.contents:
                    if isinstance(c,Bug) and not isinstance(c,Player):
                        c.die()
                        j.contents.remove(c)

    def draw_death(self):
        game.effects.draw_splat(self.spritex, self.spritey, color=(0, 255, 0))

    def deathsound(self):
        choices = ['bugdie1.wav', 'bugdie2.wav', 'bugdie3.wav']
        game.sounds[random.choice(choices)].play()
        mp = game.sounds['squish.wav'].play()
        mp.pitch = 1.5
         
class Wall(Creature):
    def __init__(self, *args, **kwargs):
        kwargs['color'] = None #Don't want a blend color
        super(Wall, self).__init__(*args, **kwargs)

    def get_images(self):
        return game.image_map['Wall']
        
    def move(self): #walls don't move
        return False

class Door(Creature):
    def __init__(self, *args, **kwargs):
        super(Door, self).__init__(*args, **kwargs)
        self.color          = (255, 0, 0)
        self.sprite.color   = self.color

    def get_images(self):
        return game.image_map['Door']

    def on_key_spawned(self, color):
        self.color  = color
        self.sprite.color = self.color
        #print "boom"

    def set_color(self, color):
        self.color        = color 
        self.sprite.color = self.color

    def get_color(self):
        return self.color

    def move(self): #walls don't move
        return False

class Portal(Creature):
    def __init__(self, *args, **kwargs):
        super(Portal, self).__init__(*args, **kwargs)
        #self.color          = color#(255, 0, 0)
        self.sprite.color   = self.color

    def get_images(self):
        return game.image_map['Door']

    def set_color(self, color):
        self.color        = color 
        self.sprite.color = self.color

    def get_color(self):
        return self.color

    def move(self): #walls don't move
        return False


class Hud(object):
    '''Display colors of bugs player can currently kill'''
    hud_batch = pyglet.graphics.Batch()

    def __init__(self, x=570, y=20):
        self.images                 = game.image_map['Bug']
        self.x                      = x
        self.y                      = y
        self.color_1_sprite         = pyglet.sprite.Sprite(self.images[0], 0, 0, batch=self.hud_batch)
        self.color_1_sprite.x       = self.x
        self.color_1_sprite.y       = self.y
        #self.color_1_sprite.color   = (255, 255,0)
        self.color_2_sprite         = pyglet.sprite.Sprite(self.images[0], 0, 0, batch=self.hud_batch)
        self.color_2_sprite.x       = self.x + 48
        self.color_2_sprite.y       = self.y
        #self.color_2_sprite.color   = (255, 0,0)
        game.state.add_handler(self)


    def on_set_player_color(self, player_color, color1, color2):
        '''Change color to represent bugs you can kill. When you have the key bug. Should display text KEY above correct bug'''
        #print "change ", color1, " and", color2
        self.color_1_sprite.color = color1
        self.color_2_sprite.color = color2

        
class Player(Bug):
    def __init__(self, *args, **kwargs):#centerx, centery, width, height, tile=None, color=None, direction = 1, velocity = 1):
        super(Player, self).__init__(*args, **kwargs)
        self.move_x=0
        self.move_y=0
        self.speed = 4
        self.state = self.STOPPED
        #self.sprite.color = color#(0, 0, 0)
        if self.color:
                #print "set color p"
                self.sprite.color   = self.color


    def collide_neighbors(self):
        collidables = []
        map(lambda x: collidables.extend(x.contents), self.tile.neighbors())
        collidables = [i for i in collidables if not (isinstance(i, Wall) or isinstance(i, Door) or isinstance(i, Player) or isinstance(i, Portal))] #This needs to be refactored -htormey
        for c in collidables:
            if ((self.left >= c.left and self.left < c.right) or (self.right > c.left and self.right <= c.right)) and \
                ((self.top > c.bottom and self.top <= c.top) or (self.bottom < c.top and self.bottom >= c.bottom)):
                    self.resolve_collision(c)
                    #print 'player collided', c


    def move(self): #the player doesn't move in the normal way (for a bug)
        if not self.alive:
            return
        x,y = self.tile.position
        x += self.move_x
        y += self.move_y        
        if self.state == self.STOPPED and (self.move_x or self.move_y):
            target_tile = game.map.grid[x][y]
            self.move_to_tile( target_tile )
            return True
        return False
        
    def on_key_press(self, *args):
        if args[0] == pyglet.window.key.P:
           if game.state.state == 'Play':
               print "Game Paused"
               game.state.state = 'Pause'
           else:
               game.state.state = 'Play'
       
        if not self.alive:
            return
        symbol, mods = args
        if not (mods & pyglet.window.key.MOD_SHIFT):
            if symbol == pyglet.window.key.MOTION_UP:
                self.sprite.rotation = 0                
                self.move_y=1
            if symbol == pyglet.window.key.MOTION_DOWN:
                self.sprite.rotation = 180
                self.move_y=-1
            if symbol == pyglet.window.key.MOTION_LEFT:
                self.sprite.rotation = 270
                self.move_x=-1
            if symbol == pyglet.window.key.MOTION_RIGHT:
                self.sprite.rotation = 90
                self.move_x=1

    def on_key_release(self, *args):   
        symbol, mods = args
        if self.move_y==1 and symbol == pyglet.window.key.MOTION_UP:
            self.move_y=0
        if self.move_y==-1 and symbol == pyglet.window.key.MOTION_DOWN:
            self.move_y=0
        if self.move_x==-1 and symbol == pyglet.window.key.MOTION_LEFT:
            self.move_x=0
        if self.move_x==1 and symbol == pyglet.window.key.MOTION_RIGHT:
            self.move_x=0         

    def on_set_player_color(self, player_color, color1, color2):
        '''Change color to represent bugs you can kill. When you have the key bug. Should display text KEY above correct bug'''
        print "Current player color: ", self.sprite.color
        self.color = player_color
        self.sprite.color = player_color
        print "change player color to:  ", player_color, " current stored p value ", self.sprite.color

    def draw_death(self):
        game.effects.draw_splat(self.spritex, self.spritey, color=(255, 0, 0))

    #def die(self):
        #super(Player, self).die()
        #x, y = self.tile.position        
        #game.effects.draw_splat(x*32+16, y*32+16)
        
    def deathsound(self):
        mp = game.sounds['playerdie.wav'].play()
        mp.pitch += random.gauss(0.1, 0.2)

    def get_images(self):
        return game.image_map['Player']


