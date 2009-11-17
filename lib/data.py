import os
import pyglet

def scanDirectory(path, data_dict={}):
   '''
   recursivly go through a given directory, set directorys = keys, files (.wav/.png/etc) to values.
   i.e ['data']['agents']['Monster01'] gets you list of all files in directory monster01
   -May want to change list to be dictionary that maps filenames to files
   '''
   if os.path.isdir(path):
     sub_dirs = [p for p in os.listdir(path) if p !='.svn' and os.path.isdir(os.path.join(path, p))] 
     if len(sub_dirs) > 0:
        find_key = path.split('/')
        key = find_key[len(find_key)-1]
        data_dict[key] = {}
        for s in sub_dirs:
           dir_contents = [p for p in os.listdir(path) if p !='.svn' and not(os.path.isdir(os.path.join(path, p)))]
           scanDirectory(os.path.join(path, s), data_dict[key])
     else:
        dir_contents    = [p for p in os.listdir(path) if p !='.svn' and not(os.path.isdir(os.path.join(path, p)))]
        find_key        = path.split('/')
        key             = find_key[len(find_key)-1]
        data_dict[key] = dict([(n, os.path.join(path,n)) for n in dir_contents])

def loadImages(imageDict):
    for imageKey, imageValue in imageDict.items():
        imageDict[imageKey] = image(imageValue)

def sound(filename):
    if filename:
       sound = pyglet.media.load(filename, streaming = False)
       return sound

def image(filename, rotate=False):
    '''
    Return an image loaded from the data directory
    rotate: Whether to rotate
    '''
    if filename:
        img = pyglet.image.load(filename)
        if rotate:
            img.anchor_x = img.width//2
            img.anchor_y = img.height//2
        return img


current_dir               = os.path.abspath(os.path.dirname(__file__))
load_files_from_dir       = 'data'
data_dir                  = os.path.normpath(os.path.join(current_dir, '..', load_files_from_dir))
test = {}
scanDirectory(data_dir, test)

