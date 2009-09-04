import os
import animatedsprite
#from animate2 import AnimatedSprite
import pyglet
from pyglet.window import key

window = pyglet.window.Window()
data_py     = os.path.abspath(os.path.dirname(__file__))
picture_dir   = os.path.normpath(os.path.join(data_py, '../../art/agents/Monster01/'))
image_names = [i for i in os.listdir(picture_dir) if i.endswith('.png')]
images = [pyglet.image.load(os.path.join(picture_dir, i)) for i in image_names]

animation           = pyglet.image.Animation.from_image_sequence(images, 0.3, True )
print "Number of animation frames created: ", len(animation.frames) 

sprite = animatedsprite.AnimatedSprite(animation, 0, 0, file_names=image_names)
#Left Sprite set
sprite.add_pic_name_look_up(["Monster_Left1.png", "Monster_Left2.png"])
#sprite.add_lookup( [0, 1] ) #Maybe want to change this to map to image name?
#Right sprite set
#sprite.add_lookup( [1, 9] )
sprite. add_pic_name_look_up(["Monster_Right1.png","Monster_Right2.png"])
#Up sprite set
#sprite.add_lookup( [2, 11] )
sprite. add_pic_name_look_up(["Monster_Up1.png", "Monster_Up2.png"])
#Down sprite set
#sprite.add_lookup( [5, 13] )
sprite.add_pic_name_look_up(["Monster_Down1.png", "Monster_Down2.png"])


sprite.set_active_lookup(1)

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

