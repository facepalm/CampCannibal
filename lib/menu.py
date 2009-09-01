import math
import os
from pyglet.gl import *
import game
import data
import random
import mapgen
import ai


'''
This class will hold all logic relating to menus
'''
class Menu():
    """pause the game"""
    def __init__(self):
        self.menu_selected = ['Exit Game',
                'Resume Game',
                'How To Play']
        self.menu_items = (
        ('Exit Game', self.exit_game),
        ('Resume Game', self.resume_game),
        ('How To Play', self.how_to_play))
        self.how_to_image       = game.image_map['Menu'][0].get_texture()
        self.how_to_sprite      = pyglet.sprite.Sprite(self.how_to_image)
        self.bug_image          = game.image_map['Bug'][0].get_texture()
        self.menu_pointer       = pyglet.sprite.Sprite(self.bug_image)
        self.max_items          = len(self.menu_selected) -1
        self.menu_current_item  = 0
        self.how_to_play        = False
        game.state.add_handler(self)

    def how_to_play(self):
        self.how_to_play = True
        print "Score: ", game.score
    def new_game(self):
        game.state.state = 'Play'
        return
    def exit_game(self):
        exit()
    def resume_game(self):
        game.state.state = 'Play'
    def on_key_press(self, symbol, modifiers):
        # Overrides default Escape key behaviour
        if symbol ==  pyglet.window.key.ENTER:
            #Call function mapped to menu item
            self.menu_items[self.menu_current_item][1]()
        if symbol ==  pyglet.window.key.ESCAPE:
            if game.state.state == 'Pause':
                game.state.state = 'Play'
                return 
            elif game.state.state == 'Play':
                print "exit game"
                exit()
        if symbol ==  pyglet.window.key.MOTION_UP:
            #print self.menu_current_item
            if not ((self.menu_current_item < 0) or (self.menu_current_item >= self.max_items)):
                self.menu_current_item += 1

        if symbol ==  pyglet.window.key.MOTION_DOWN:
            #print self.menu_current_item
            if not ((self.menu_current_item <= 0) or (self.menu_current_item > self.max_items)):
                self.menu_current_item -= 1

    def draw_menu(self):
        """Draw all menu_items"""

        if self.how_to_play:
            #print "draw how to play"
            glClear(GL_COLOR_BUFFER_BIT)
            self.how_to_sprite.x    = 0
            self.how_to_sprite.y    = 0
            self.how_to_sprite.draw()
            #game.state.state = 'Play'
            return
        menu_position_y =  300
        menu_position_x =  200 
        #Distance between each menu segment 
        item_height = 35
        default_font_size = 20
        selected_font_size = 25
        menu_title = pyglet.text.Label("PestiCide", color=(0, 200, 0, 255), 
                    font_size=35, 
                    x = 180,
                    y = 400)        
        menu_title.draw()
        for key, item in self.menu_items:
            font_size=default_font_size
            if self.menu_selected[self.menu_current_item] == key:
                self.menu_pointer.x = menu_position_x - 20
                self.menu_pointer.y = menu_position_y
                font_size=selected_font_size
            item_segment = pyglet.text.Label(key, color=(0, 200, 0, 255), 
                    font_size=font_size, 
                    x = menu_position_x,
                    y = menu_position_y)
            menu_position_y += item_height
            self.menu_pointer.draw()
            item_segment.draw()
        
    def on_draw(self):
        if game.state.state == 'Pause':
           self.draw_menu() 
        else:
            pass
    def enter(self, window):
        self.game.music_player.pause()
        self.game.background_player.pause()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glDisable(GL_DEPTH_TEST)
        self.on_resize(window.width, window.height)
        window.set_exclusive_mouse(True)
    def on_resize(self, width, height):
        """Set perspective projecion for fish animation"""
        #TODO (CCB): Caclucate the z-value so that this projection works with all window sizes!
        self.width = width
        self.height = height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(60., width / float(height), 0.001, 1000.)
        glMatrixMode(GL_MODELVIEW)        
        glLoadIdentity()
        gluLookAt(width/2.0, height/2.0, 520.0, width/2.0, height/2.0, 0.0, 0.0, 1.0, 0.0) 
