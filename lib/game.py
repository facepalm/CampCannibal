import os
from pyglet.gl import *
from creatures import Bug, Spawn
import data
import ctypes
import faction
fourfv = ctypes.c_float * 4

from game_map import Map, EffectsManager

#handles the title screens
import titles
import knEvents


'''
Setup global variables such as gamestate, loading pictures, map.
This is done so you do not have to include map or system in the declaration
just access game.state or game.map
'''
 
def init():
    global score
    global state
    global map
    global number_of_bugs
    global window
    global images
    global image_map
    global sounds
    global effects
    global factions
    #Hack in new animation system -htormey
    global imageAtlas

    score =  0
    number_of_bugs = 0
    window = pyglet.window.Window(width=800,height=600, resizable=True, visible=False)
    window.clear()
    window.resize = resize
    window.set_visible(True)
    window.resize(window.width, window.height)
    
    titles.StartTitleScreens(window);
    #Hack, needs to be be refactored -htormey
    data.loadTextureAtlas()
    data.loadimages()
    data.loadsounds()
    #Hack -htormey
    imageAtlas  = data._imageAtlas
    #print "atlas: ", imageAtlas
    images      = data._images
    sounds      = data._sounds
    image_groups = data._image_groups
    #Global that maps images to creatures/objects
    image_map = {
        'Door': image_groups['walls/door01'],
        'Wall': image_groups['walls/wall01'],
        'Bug' : image_groups['agents/bug01'],
        'Map' : image_groups['background/background01'],
        'Player' : image_groups['agents/player'],
        'Splats' : image_groups['effects/splat'],
        'Burrow' : image_groups['effects/burrow'],
    }
    state = GameState(image_map = image_map) #Filthy fix this later
    effects = EffectsManager()
    map = Map(32, 32, window,64)
    map.populate()
    
    knEvents.FullGameInit(state);
    pass
    
    
'''
OpenGL settings, may want to tweak this and or move this else where
'''
def resize(widthWindow, heightWindow):
    """Initial settings for the OpenGL state machine, clear color, window size, etc"""
    glEnable(GL_BLEND)
    glEnable(GL_POINT_SMOOTH)
    glShadeModel(GL_SMOOTH)# Enables Smooth Shading
    glBlendFunc(GL_SRC_ALPHA,GL_ONE)#Type Of Blending To Perform
    glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);#Really Nice Perspective Calculations
    glHint(GL_POINT_SMOOTH_HINT,GL_NICEST);#Really Nice Point Smoothing
    glDisable(GL_DEPTH_TEST)


'''
All objects the create/receive events register with the game state
'''
class GameState(pyglet.event.EventDispatcher):
    def __init__(self, image_map=None):
        self.time = 0
        self.image_map = image_map
        self.spawn = Spawn()
        #Perhaps I should changes this to just instansiate spawn here? -htormey
        self.add_handler(self.spawn)
        self.window = window
        self.player=None
        window.push_handlers(self)
        pyglet.clock.schedule_interval(self.update, 1.0/60)
        #Set player color
        #State
        self.state = 'Start'        
        self.factions = faction.FactionManager()
        pass
                

    def set_player_color(self):
        self.spawn.set_player_color(self)

    def get_color_bug(self, bug_name):
        return self.spawn.get_color_bug(bug_name)

    def add_handler(self, handler):
        '''Add an event handler to the gamestate.
        event handlers are objects which accept and generate events'''
        if handler != None:
            self.push_handlers(handler)
        else:
            pass

    def key_spawned(self, key_color):
        self.dispatch_event('on_key_spawned', key_color)

    def set_player_color(self, player_color, color1, color2):
        self.dispatch_event('on_set_player_color', player_color,  color1, color2)

    def spawn(self, class_name, tile):
        self.dispatch_event('on_spawn', class_name, tile)

    def update(self, dt):
        
        if self.state == 'Play':
            self.time += dt
            self.dispatch_event('on_update', dt)
    # Relay many window events to our child handlers
    def on_draw(self, *args):
        window.clear()
        if self.state == 'GameOver':
            return
        elif self.state == 'Start':
            self.relay_event('on_draw', *args)
        else:
            self.relay_event('on_draw', *args)

    def on_key_press(self, *args):
        if self.state == 'Start':
            if args[0] == pyglet.window.key.S:
                self.state = 'Play'
        else:
            self.relay_event('on_key_press', *args)

    def on_key_release(self, *args):
        self.relay_event('on_key_release', *args)

    def on_mouse_motion(self, *args):
        self.relay_event('on_mouse_motion', *args)

    def on_mouse_press(self, *args):
        self.relay_event('on_mouse_press', *args)

    def relay_event(self, event_type, *args):
        '''Similar to dispatch_event, only it does not call the event
        handler on the dispatcher itself, which is not deisired for relaying.

        :Parameters:
            `event_type` : str
                Name of the event.
            `args` : sequence
                Arguments to pass to the event handler.
        '''
        assert event_type in self.event_types

        # Search handler stack for matching event handlers
        for frame in list(self._event_stack):
            handler = frame.get(event_type, None)
            if handler:
                try:
                    if handler(*args):
                        return
                except TypeError:
                    self._raise_dispatch_exception(event_type, args, handler)

GameState.register_event_type('on_key_press')
GameState.register_event_type('on_key_release')
GameState.register_event_type('on_mouse_motion')
GameState.register_event_type('on_mouse_press')
GameState.register_event_type('on_draw')
GameState.register_event_type('on_update')
#Custom events live here
GameState.register_event_type('on_spawn')
GameState.register_event_type('on_key_spawned')
GameState.register_event_type('on_set_player_color')
