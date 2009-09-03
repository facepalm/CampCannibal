import animatedsprite
import math
import os
from pyglet.gl import *
from pyglet.window import key
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
          'Fire'    : Fire,
          'Wall'    : Wall,
          'Bug'     : Bug,
          'Player'  : Player2,
          'Frank'   : Frank,
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
            u=unit_class(tile=tile) #make a unit of that class x*32+16, y*32+16, 32, 32, tile=tile, bug_map=self.bug_spawn_map['Color4']) 
            game.state.player=u
            self.set_player_color(game.state)
            tile.contents.append(u)#add the object to the tile
        elif spawn_what == 'Wall':
            u=unit_class(tile=tile) #make a unit of that class
            tile.contents.append(u)#add the object to the tile
        elif spawn_what == 'Bug':
            u=unit_class(tile=tile) #make a unit of that class
            tile.contents.append(u)#add the object to the tile
        elif spawn_what == 'Frank':
            u=unit_class(tile=tile) #make a unit of that class
            tile.contents.append(u)#add the object to the tile


class Creature(object):
    """Sprite-based creature on the map
       (CCB) Bug / wall behavior was getting different enough that I 
        factored them out into separate subclasses.
    """
    bug_batch = pyglet.graphics.Batch()
    
    #States that a bug can be in
    STOPPED     = 0 
    MOVING      = 1
    
    def __init__(self, centerx=0, centery=0, width=32, height=32, tile=None, color=None, direction = 1, speed = 1, bug_map = None, bug_spawn_map = None):

            self.name       = None #Figure out If I need this
            self.beats      = None
            #Come up with a better way to manage images for Creatures
            self.images         = self.get_images()
            self.image_index    = 0
            self.direction      = direction #Probably should make this an x/y vector but then again, this is a grid that allows for no diagonal movement
            self.speed          = speed
            self.attacking = False
            self.health         = 10
            self.toughness      = 1
            self.strength       = 1
            self.dt= 0.00001
            self.beginingx     = None
            self.beginingy     = None
            self.destinationx  = None
            self.destinationy  = None
            self.tile           = tile #the tile this bug is standing on.  If None, it's floating in limbo
            self.last_tile      = tile #the last tile this bug was standing on.  Used to prevent u-turns.
            self.sprite         = pyglet.sprite.Sprite(self.images[0], 0, 0, batch=self.bug_batch)
            self.width          = self.sprite.width
            self.height         = self.sprite.height
            x, y                = self.tile.position
            if centerx: 
                self.centerx=centerx                 
            else: 
                self.centerx = (x+0.5)*game.map.tilesize
            if centery: 
                self.centery=centery 
            else: 
                self.centery = (y+0.5)*game.map.tilesize    
            self.sprite.x       = self.left#centerx
            self.sprite.y       = self.bottom#centery         

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
            
    def die(self):
        if not self.alive:
            return
        self.alive = False
        self.state = self.STOPPED
        self.spritex = self.sprite.x
        self.spritey = self.sprite.y
        try:
            self.tile.contents.remove(self)
        except:
            print "Dead creature already removed"
        #game.score += self.bug_map['Score']
        #print "Current score: ", game.score
        try:#Prevent error on double deletion
            if not isinstance(self,Player):
                self.sprite.delete()            
        except:
            print 'Double delete caught'
        game.state.remove_handlers(self)

    
class Bug(Creature):
    """This class represent a bug. Player object will be a subclass of bug"""

    def __init__(self, *args, **kwargs):
        super(Bug, self).__init__(*args, **kwargs)
        self.ai=ai.Mind()
        self.alive = True
        
    def get_images(self):
        return game.image_map['Bug']

    def collide_neighbors(self):
        collidables = []
        map(lambda x: collidables.extend(x.contents), self.tile.neighbors())
        collidables = [i for i in collidables if (isinstance(i, Frank)  or isinstance(i, Fire))]
        for c in collidables:
            if ((self.left >= c.left and self.left < c.right) or (self.right > c.left and self.right <= c.right)) and \
                ((self.top > c.bottom and self.top <= c.top) or (self.bottom < c.top and self.bottom >= c.bottom)):
                    self.resolve_collision(c)
                    #print 'bug collided', c'''

    def on_update_old(self, dt):
        '''Update sprites postion/state'''
        if not self.alive:
            return
        self.collide_neighbors()    
        if self.state != self.MOVING:
            #maybe check if we're still alive at this point
            self.move()            
        if self.state == self.MOVING:
            self.time += 1
            changex		= self.destinationx - self.beginingx
            changey		= self.destinationy - self.beginingy
            duration	= math.sqrt( (changex * changex) + (changey * changey))//self.speed
            if not (self.time > duration):
                self.centerx 		= self.linear_tween(self.time, duration, changex, self.beginingx)
                self.centery 		= self.linear_tween(self.time, duration, changey, self.beginingy)
                self.sprite.x		= self.centerx#right
                self.sprite.y		= self.centery#top
                if isinstance(self, Player):
                    game.map.set_center( self.centerx, self.centery)
            else:
                self.state = self.STOPPED

    def on_update(self, dt):   
        '''Update sprites postion/state'''
        if not self.alive:
            return
        
        self.dt=dt   
        if self.health <= 0:
            self.die()
            return

        '''if len(self.images) > 1:
            self.image_index = (self.image_index+1)%len(self.images)
            self.sprite.image = self.images[self.image_index]'''    

        if self.state == self.STOPPED:
            self.idle()            
        elif self.state == self.MOVING:            
            self.time += 1
            changex             = self.destinationx - self.beginingx
            changey             = self.destinationy - self.beginingy
            duration    = math.sqrt( (changex * changex) + (changey * changey))//self.speed
            if not (self.time > duration):
                self.centerx            = self.linear_tween(self.time, duration, changex, self.beginingx)
                self.centery            = self.linear_tween(self.time, duration, changey, self.beginingy)
                self.sprite.x           = self.centerx#right
                self.sprite.y           = self.centery#top
                ctile=game.map.tile_from_coords((self.centerx,self.centery))
                if ctile and self.tile != ctile:
                    #move to new tile
                    if self in self.tile.contents:
                         self.tile.contents.remove(self)#Remove from current tile                    
                    ctile.contents.append(self)#add to the dest tile
                    self.last_tile = self.tile
                    self.tile=ctile
            else:
                self.state = self.STOPPED
            #if random.random() <= 0.02:
            #    self.state=self.STOPPED
        if self.attacking:
            self.collide_nearby() 
                
        if self.time % 5 == 0 and self.state != self.STOPPED:
            self.next_image()
    
    def idle(self):
        #find an enemy to move to        
        u=self.get_nearby_units()
        if len(u) > 0:
            u=random.choice(u)
            self.move_to_pt((u.centerx,u.centery))
            self.attacking = True
        else:
            self.move()  
            self.attacking = False
        self.collide_nearby() 
        
    def get_nearby_units(self,friend=False):
        collidables = []
        collidables.extend(self.tile.contents)
        collidables = [i for i in collidables if (self != i and ((isinstance(self, Frank) and isinstance(i, Bug)) or (isinstance(self, Bug) and isinstance(i, Frank))))]
        return collidables
    
    def collide_nearby(self):
        for c in self.tile.contents:
            if ((self.left >= c.left and self.left < c.right) or (self.right > c.left and self.right <= c.right)) and \
                ((self.top > c.bottom and self.top <= c.top) or (self.bottom < c.top and self.bottom >= c.bottom)):
                    self.resolve_collision(c)
       
        

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
            self.move_to_tile( self.ai.choose_tile(valid_neighbors) )
        else: #we must be trapped.  
            self.last_tile=self.tile #Update last_tile to reflect this

    def move_to_pt(self,dest):
        self.destinationx = dest[0]
        self.destinationy = dest[1]
        self.beginingx    = self.centerx
        self.beginingy    = self.centery
        self.time = 0
        self.state = self.MOVING   

    def move_to_dest(self, dest):
        '''Function calls linear tween and makes bugs move nicely. Not implemented yet'''
        tile_width=game.map.tilesize
        tile_height=game.map.tilesize
        wideload=1.0*self.sprite.width/tile_width
        highload=1.0*self.sprite.height/tile_height
        x1, y1 = dest.position
        self.destinationx = (x1+wideload/2+(1-wideload)*random.random())*tile_width
        self.destinationy = (y1+highload/2+(1-highload)*random.random())*tile_height
        self.beginingx    = self.centerx
        self.beginingy    = self.centery
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
        if isinstance(other, Fire):
            return True
        if isinstance(other, Wall):#walls block us from moving
            return True #There is a blockage
        if isinstance(self, Frank) and isinstance(other, Bug): #frank can hit bugs
            return False
        if isinstance(self, Bug) and isinstance(other, Frank): #bugs can hit frank
            return False
        if isinstance(self, Bug) and isinstance(other, Bug): #bugs block other bugs
            return True
        return False #there is NOT a blockage with whatever object this is
    
    def check_collision(self,other):        
        '''Function for handling non-blocking collisions (attacks and stuff)'''
        if self==other: #possibly useful for masochism-based attacks
            return
        if isinstance(self, Frank) and isinstance(other, Bug): #player can hit bugs            
            #Color-based damage
            self.resolve_collision(other)
        if isinstance(self, Bug) and isinstance(other, Frank): #bugs can hit player
            #color-based damage
            self.resolve_collision(other)
            
    '''def resolve_collision(self,other):
        #attack collisions
        if not other.alive:
            return
        other.health -= 1.0*self.strength/other.toughness  '''
            
    def resolve_collision(self,other):
        if not other.alive:
            return
        if self != other and ((isinstance(self, Frank) and isinstance(other, Bug)) or (isinstance(self, Bug) and isinstance(other, Frank))):
            #melee scuffle
            self.state=self.STOPPED
            other.state=other.STOPPED
            other.attacking=True
            other.health -= 1.0*self.strength/other.toughness
            pass
            
            
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
        #self.bug_map['Count'] -= 1
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

class Fire(Creature):
    def __init__(self, *args, **kwargs):
        super(Fire, self).__init__(*args, **kwargs)
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

#Begin new player
class Creature2(object):
    """Sprite-based creature on the map
       (CCB) Bug / wall behavior was getting different enough that I 
        factored them out into separate subclasses.
    """
    creature_batch = pyglet.graphics.Batch()
    
    #States that a bug can be in
    STOPPED     = 0 
    MOVING      = 1
    
    def __init__(self, centerx=0, centery=0, width=32, height=32, tile=None, color=None, direction = 1, speed = 1, bug_map = None, bug_spawn_map = None):

            self.name       = None #Figure out If I need this
            self.beats      = None
            #Come up with a better way to manage images for Creatures
            #self.images         = self.get_images()
            self.image_index    = 0
            self.direction      = direction #Probably should make this an x/y vector but then again, this is a grid that allows for no diagonal movement
            self.speed          = speed
            self.attacking = False
            self.health         = 10
            self.toughness      = 1
            self.strength       = 1
            self.dt= 0.00001
            self.beginingx     = None
            self.beginingy     = None
            self.destinationx  = None
            self.destinationy  = None
            self.tile           = tile #the tile this bug is standing on.  If None, it's floating in limbo
            self.last_tile      = tile #the last tile this bug was standing on.  Used to prevent u-turns.
            #New
            #Internal image map stuff this needs to refactored -htormey
            sprite_set_x        = 0
            sprite_set_y        = 26
            sprite_set_height   = 40
            sprite_set_width    = 540
            sprite_set_rows     = 1
            sprite_set_cols     = 16
            sprite_width        = 34
            sprite_height       = 34
            grid                = pyglet.image.ImageGrid(game.imageAtlas.get_region(sprite_set_x, sprite_set_y, sprite_set_width, sprite_set_height), sprite_set_rows, sprite_set_cols, sprite_width, sprite_height)
            animation           = pyglet.image.Animation.from_image_sequence(grid.get_texture_sequence(), 0.1, True )
            self.sprite = animatedsprite.AnimatedSprite(animation, 0, 0, batch=self.creature_batch)
            #Left Sprite set
            self.sprite.add_lookup( [0, 8] )
            #Right sprite set
            self.sprite.add_lookup( [1, 9] )
            #Up sprite set
            self.sprite.add_lookup( [2, 11] )
            #Down sprite set
            self.sprite.add_lookup( [5, 13] )
            self.sprite.set_active_lookup(4)
            #New
            #self.sprite         = self.get_sprite()#= pyglet.sprite.Sprite(self.images[0], 0, 0, batch=self.bug_batch)
            self.width          = self.sprite.width
            self.height         = self.sprite.height
            x, y                = self.tile.position
            if centerx: 
                self.centerx=centerx                 
            else: 
                self.centerx = (x+0.5)*game.map.tilesize
            if centery: 
                self.centery=centery 
            else: 
                self.centery = (y+0.5)*game.map.tilesize    
            self.sprite.x       = self.left#centerx
            self.sprite.y       = self.bottom#centery         

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

    def get_sprite(self):
        pass
    def get_images(self):
        pass

    def next_image(self):
        pass 
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
            
    def die(self):
        if not self.alive:
            return
        self.alive = False
        self.state = self.STOPPED
        self.spritex = self.sprite.x
        self.spritey = self.sprite.y
        try:
            self.tile.contents.remove(self)
        except:
            print "Dead creature already removed"
        #game.score += self.bug_map['Score']
        #print "Current score: ", game.score
        try:#Prevent error on double deletion
            if not isinstance(self,Player2):
                self.sprite.delete()            
        except:
            print 'Double delete caught'
        game.state.remove_handlers(self)

class Bug2(Creature2):
    """This class represent a bug. Player object will be a subclass of bug"""

    def __init__(self, *args, **kwargs):
        super(Bug2, self).__init__(*args, **kwargs)
        self.alive = True

    def collide_neighbors(self):
        collidables = []
        map(lambda x: collidables.extend(x.contents), self.tile.neighbors())
        collidables = [i for i in collidables if (isinstance(i, Frank)  or isinstance(i, Fire))]
        for c in collidables:
            if ((self.left >= c.left and self.left < c.right) or (self.right > c.left and self.right <= c.right)) and \
                ((self.top > c.bottom and self.top <= c.top) or (self.bottom < c.top and self.bottom >= c.bottom)):
                    self.resolve_collision(c)
                    #print 'bug collided', c'''

    def on_update(self, dt):   
        '''Update sprites postion/state'''
        if not self.alive:
            return
        
        self.dt=dt   
        if self.health <= 0:
            self.die()
            return

        if self.state == self.STOPPED:
            self.idle()            
        elif self.state == self.MOVING:            
            self.time += 1
            changex             = self.destinationx - self.beginingx
            changey             = self.destinationy - self.beginingy
            duration    = math.sqrt( (changex * changex) + (changey * changey))//self.speed
            if not (self.time > duration):
                self.centerx            = self.linear_tween(self.time, duration, changex, self.beginingx)
                self.centery            = self.linear_tween(self.time, duration, changey, self.beginingy)
                self.sprite.x           = self.centerx#right
                self.sprite.y           = self.centery#top
                ctile=game.map.tile_from_coords((self.centerx,self.centery))
                if ctile and self.tile != ctile:
                    #move to new tile
                    if self in self.tile.contents:
                         self.tile.contents.remove(self)#Remove from current tile                    
                    ctile.contents.append(self)#add to the dest tile
                    self.last_tile = self.tile
                    self.tile=ctile
            else:
                self.state = self.STOPPED

        if self.attacking:
            self.collide_nearby() 
                
    def idle(self):
        #find an enemy to move to        
        u=self.get_nearby_units()
        if len(u) > 0:
            u=random.choice(u)
            self.move_to_pt((u.centerx,u.centery))
            self.attacking = True
        else:
            self.move()  
            self.attacking = False
        self.collide_nearby() 
 
    def get_nearby_units(self,friend=False):
        collidables = []
        collidables.extend(self.tile.contents)
        collidables = [i for i in collidables if (self != i and ((isinstance(self, Frank) and isinstance(i, Bug)) or (isinstance(self, Bug) and isinstance(i, Frank))))]
        return collidables
    
    def collide_nearby(self):
        for c in self.tile.contents:
            if ((self.left >= c.left and self.left < c.right) or (self.right > c.left and self.right <= c.right)) and \
                ((self.top > c.bottom and self.top <= c.top) or (self.bottom < c.top and self.bottom >= c.bottom)):
                    self.resolve_collision(c)

    def move(self):
        
        all_neighbors=self.tile.neighbors() #get surrounding squares
        valid_neighbors=[]
        if self.last_tile in all_neighbors: #remove the most recent square
            all_neighbors.remove(self.last_tile)     
        for n in all_neighbors:
            if not self.check_occlusion(n):
                valid_neighbors.append(n)   
        if len(valid_neighbors) >= 1: #do we have at least one square to move to?
            self.move_to_tile( self.ai.choose_tile(valid_neighbors) )
        else: #we must be trapped.  
            self.last_tile=self.tile #Update last_tile to reflect this

    def move_to_pt(self,dest):
        self.destinationx = dest[0]
        self.destinationy = dest[1]
        self.beginingx    = self.centerx
        self.beginingy    = self.centery
        self.time = 0
        self.state = self.MOVING   

    def move_to_dest(self, dest):
        '''Function calls linear tween and makes bugs move nicely. Not implemented yet'''
        tile_width=game.map.tilesize
        tile_height=game.map.tilesize
        wideload=1.0*self.sprite.width/tile_width
        highload=1.0*self.sprite.height/tile_height
        x1, y1 = dest.position
        self.destinationx = (x1+wideload/2+(1-wideload)*random.random())*tile_width
        self.destinationy = (y1+highload/2+(1-highload)*random.random())*tile_height
        self.beginingx    = self.centerx
        self.beginingy    = self.centery
        self.time = 0
        self.last_tile = self.tile
        self.tile = dest
        self.state = self.MOVING

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
        if isinstance(other, Fire):
            return True
        if isinstance(other, Wall):#walls block us from moving
            return True #There is a blockage
        if isinstance(self, Frank) and isinstance(other, Bug): #frank can hit bugs
            return False
        if isinstance(self, Bug) and isinstance(other, Frank): #bugs can hit frank
            return False
        if isinstance(self, Bug) and isinstance(other, Bug): #bugs block other bugs
            return True
        return False #there is NOT a blockage with whatever object this is
    
    def check_collision(self,other):        
        '''Function for handling non-blocking collisions (attacks and stuff)'''
        if self==other: #possibly useful for masochism-based attacks
            return
        if isinstance(self, Frank) and isinstance(other, Bug): #player can hit bugs            
            #Color-based damage
            self.resolve_collision(other)
        if isinstance(self, Bug) and isinstance(other, Frank): #bugs can hit player
            #color-based damage
            self.resolve_collision(other)
            
    '''def resolve_collision(self,other):
        #attack collisions
        if not other.alive:
            return
        other.health -= 1.0*self.strength/other.toughness  '''
            
    def resolve_collision(self,other):
        if not other.alive:
            return
        if self != other and ((isinstance(self, Frank) and isinstance(other, Bug)) or (isinstance(self, Bug) and isinstance(other, Frank))):
            #melee scuffle
            self.state=self.STOPPED
            other.state=other.STOPPED
            other.attacking=True
            other.health -= 1.0*self.strength/other.toughness
            pass
            
            
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
        super(Bug2, self).die()
        #x, y = self.tile.position        
        #game.effects.draw_splat(x*32+16, y*32+16, color=(0, 255, 0))        
       # game.number_of_bugs -= 1
        #self.bug_map['Count'] -= 1
        self.draw_death()
        self.deathsound()
        if isinstance(self,Player2):
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
 
#imageAtlas
class Player2(Bug2):
    def __init__(self, *args, **kwargs):
        print "Spawning Player2"
        super(Player2, self).__init__(*args, **kwargs)
        self.alive = True
        self.move_x=0
        self.move_y=0
        self.speed = 4
        self.state = self.STOPPED

    def move(self): #the player doesn't move in the normal way (for a bug)
        print "Move "
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
            if symbol == key.MOTION_DOWN:
                print "down"
                self.move_y=-1
                self.sprite.set_active_lookup(4)
            elif symbol == key.MOTION_UP:
                print "Up"
                self.move_y=1
                self.sprite.set_active_lookup(3)
            elif symbol == key.MOTION_LEFT:
                print "Left"
                self.move_x=-1
                self.sprite.set_active_lookup(1)
            elif symbol == key.MOTION_RIGHT:
                print "Right"
                self.move_x=1
                self.sprite.set_active_lookup(2)

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

    def deathsound(self):
        mp = game.sounds['playerdie.wav'].play()
        mp.pitch += random.gauss(0.1, 0.2)

    def get_images(self):
        return game.image_map['Player']


#End new player

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

class Frank(Bug):
    def __init__(self, *args, **kwargs):#centerx, centery, width, height, tile=None, color=None, direction = 1, velocity = 1):
        super(Frank, self).__init__(*args, **kwargs)
        self.move_x=0
        self.move_y=0
        self.speed = 1
        self.attributes = {'S':2, 'T':1, 'H':10}; #Strength, Toughness, Health
        self.state = self.STOPPED
        #self.sprite.color = color#(0, 0, 0)
        if self.color:
                #print "set color p"
                self.sprite.color   = self.color    
    
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


