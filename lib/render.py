from pyglet.gl import *
from creatures import Wall

class Render(object):

    def __init__(self, game_data):
        """
            width, height: dimension in tiles
            background: background image to use
        """
        self.window = game_data["window"]
        self.game           = game_data["game"]
        self.width = self.window.width
        self.height = self.window.height
        self.game.add_handler(self)

    def on_draw(self):
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix() 
        #Tile.tile_batch.draw()
        #EffectsManager.effects_batch.draw()
        #Bug.bug_batch.draw()
        Wall.object_batch.draw()
        #Creature.creature_batch.draw()
        #Add in animation code
        glPopMatrix()
        glLoadIdentity()
 
