'''
Loads data files from the "data" directory shipped with a game.
'''

import os
import pyglet

_images = {}
_image_groups = {}
_sounds = {}

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))
art_dir = os.path.normpath(os.path.join(data_py, '..', 'art'))

def imagepath(filename):
    """Determine the path to a file in the art directory"""
    return os.path.join(art_dir, filename)


def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(art_dir, filename), mode)

def loadimages():
    '''Load all of the images in the data  dir'''
    global _image_groups
    targets = os.listdir(art_dir)
    targets = [i for i in targets if i !='.svn' and os.path.isdir( os.path.join(art_dir, i))]
    for t in targets:
        spritegroups = os.listdir( os.path.join(art_dir, t))
        spritegroups = [i for i in spritegroups if i !='.svn' and os.path.isdir( os.path.join(art_dir, t, i))]
        for s in spritegroups:
            rotate = (t == 'agents') or (t == 'effects')
            images = [i for i in os.listdir( os.path.join(art_dir, t, s)) if i.endswith('.png')]
            images = [image(os.path.join(t, s, i), rotate) for i in images]
            _image_groups["%s/%s"%(t, s)] = images

def image(filename, rotate=False):
    '''Return an image loaded from the data directory
        rotate: Whether to rotate
    '''
    global _images
    if filename not in _images:
        img = pyglet.image.load(imagepath(filename))
        if rotate:
            img.anchor_x = img.width//2
            img.anchor_y = img.height//2
        _images[filename] = img
    return _images[filename]

def loadsounds():
    for f in os.listdir(os.path.join(data_dir, 'sound')):
        if f.endswith('.wav'):
            sound(f)
    
def sound(filename):
    global _sounds
    if filename not in _sounds:
        _sounds[filename] = pyglet.media.load(os.path.join(data_dir, 'sound', filename), streaming = False)
    return _sounds[filename]
