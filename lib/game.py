import os
from pyglet.gl import *
from data import scanDirectory, loadImages
from game_map import Map
from render import Render
from creatures import Spawn

def init():
    window                                          = pyglet.window.Window(width=800,height=600, resizable=True, visible=False)
    window.clear()
    window.resize                                   = resize
    window.set_visible(True)
    window.resize(window.width, window.height)
    current_dir                                     = os.path.abspath(os.path.dirname(__file__))
    load_files_from_dir                             = 'data'
    data_dir                                        = os.path.normpath(os.path.join(current_dir, '..', load_files_from_dir))
    game_data                                       = {}
    scanDirectory(data_dir, game_data)
    loadImages(game_data['data']['agents']['Monster01']['animations'])
    loadImages(game_data['data']['map']['elements']['House01'])

    game_data["window"]                             = window
    state                                           = GameState(game_data)
    game_data["game"]                               = state
    map                                             = Map(32, 32, game_data, 32)
    spawner                                         = Spawn(game_data)
    map.populate()
    render                                          = Render(game_data)
    print game_data

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
    def __init__(self, game_data):
        self.time = 0
        self.window = game_data["window"]
        self.window.push_handlers(self)
        pyglet.clock.schedule_interval(self.update, 1.0/60)

    def add_handler(self, handler):
        '''Add an event handler to the gamestate.
        event handlers are objects which accept and generate events'''
        if handler != None:
            self.push_handlers(handler)
        else:
            pass

    def update(self, dt):
        self.dispatch_event('on_update', dt)

    # Relay many window events to our child handlers
    def on_draw(self, *args):
        self.window.clear()
        self.relay_event('on_draw', *args)

    def on_key_press(self, *args):
        self.relay_event('on_key_press', *args)

    def on_key_release(self, *args):
        self.relay_event('on_key_release', *args)

    def on_mouse_motion(self, *args):
        self.relay_event('on_mouse_motion', *args)

    def on_mouse_press(self, *args):
        self.relay_event('on_mouse_press', *args)

    def spawn(self, class_name, tile):
        self.dispatch_event('on_spawn', class_name, tile)

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
