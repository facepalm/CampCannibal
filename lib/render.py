from pyglet.gl import *
from creatures import Wall
from animation_example import Tween, ease_none, ease_in_quad

class Render(object):

    def __init__(self, game_data):
        """
            width, height: dimension in tiles
            background: background image to use
        """
        self.window         = game_data["window"]
        self.game_data      = game_data
        self.game           = game_data["game"]
        self.width = self.window.width
        self.height = self.window.height
        self.game.add_handler(self)
        self.sprite = pyglet.sprite.Sprite(self.game_data['data']['agents']['Monster01']['animations']['Monster_Up1.png'], 100, 100)
        self.Tween = Tween(self.sprite, "x", ease_in_quad, self.sprite.x, self.sprite.x+200, 5, True, False, "Testobj1")
        self.Tween2 = Tween(self.sprite, "y", ease_none, self.sprite.y, self.sprite.y+100, 10, True, False, "Testobj2")
        self.Tween.start()
        self.Tween2.start()
        #def __init__(self, obj, prop, func, begin, finish, duration, use_seconds, looping=False, name=None)
    def on_draw(self):
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix() 
        #Tile.tile_batch.draw()
        #EffectsManager.effects_batch.draw()
        #Bug.bug_batch.draw()
        Wall.object_batch.draw()
        self.sprite.draw()
        #Creature.creature_batch.draw()
        #Add in animation code
        glPopMatrix()
        glLoadIdentity()
 
