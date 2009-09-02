import animatedsprite
#from animate2 import AnimatedSprite
import pyglet
from pyglet.window import key

window = pyglet.window.Window()
sprite_sheet = pyglet.image.load('action1.bmp')
sprite_set_x        = 0
sprite_set_y        = 26#40
sprite_set_height   = 40#346
sprite_set_width    = 540
sprite_set_rows     = 1
sprite_set_cols     = 16
sprite_width        = 34
sprite_height       = 34
'''
res = pyglet.image.load('test_frames.png')
grid = pyglet.image.ImageGrid(res.get_region(0,7*32,32*8,32), 1, 8, 32, 32)
animation = pyglet.image.Animation.from_image_sequence(grid.get_texture_sequence(), 0.1, True )
'''
grid                = pyglet.image.ImageGrid(sprite_sheet.get_region(sprite_set_x, sprite_set_y, sprite_set_width, sprite_set_height), sprite_set_rows, sprite_set_cols, sprite_width, sprite_height)
#Class Method from_image_sequence(cls, sequence, period, loop=True)
animation           = pyglet.image.Animation.from_image_sequence(grid.get_texture_sequence(), 0.1, True )

print "Number of animation frames created: ", len(animation.frames) 
#sprite2 = animatedsprite.AnimatedSprite(animation, 0, 0)
#sprite2.add_lookup( [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,5,6,7] )

#sprite = pyglet.sprite.Sprite(animation)
sprite = animatedsprite.AnimatedSprite(animation, 0, 0)
#sprite.add_lookup( [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,5,6,7] )
#Left Sprite set
sprite.add_lookup( [0, 8] )
#Right sprite set
sprite.add_lookup( [1, 9] )
#Up sprite set
sprite.add_lookup( [2, 11] )
#Down sprite set
sprite.add_lookup( [5, 13] )


sprite.set_active_lookup(4)

@window.event
def on_key_press(symbol, mod):

    # Symbolic names:
    if symbol == key.MOTION_DOWN:
        sprite.set_active_lookup(4)
    elif symbol == key.MOTION_UP:
        print "Up"
        sprite.set_active_lookup(3)
    elif symbol == key.MOTION_LEFT:
        print "Left"
        sprite.set_active_lookup(1)
    elif symbol == key.MOTION_RIGHT:
        print "Right"
        sprite.set_active_lookup(2)


@window.event
def on_draw():
    window.clear()
    sprite.draw()
pyglet.app.run()

