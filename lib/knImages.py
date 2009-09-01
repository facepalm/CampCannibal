"""
	Programmer:	Keith G. Nemitz
	E-mail:		future@mousechief.com

	Version 0.0.1 Development
"""

#The images module handles the loading of all graphics files
#conceptually, everything is a sprite.
#It also handles some graphics manipulations


#----------------------------------------------- IMPORTS
import os
import sys

import pyglet

#----------------------------------------------- Module Variables

#Paths to this game's data.
rootPath = "data"
rsrcPaths = ["icons","animations","backdrops","buttons","actors",
                'music','sounds']; #last check is the root datapath


screenSize = None;
theWindow = None;

#----------------------------------------------- Module Functions

        
def Init(window):
    global screenSize,theWindow
    
    theWindow = window;
    screenSize = window.get_size();

    pyglet.resource.path = [rootPath]+[os.path.join(rootPath,x) for x in rsrcPaths];
    pyglet.resource.reindex();
    return theWindow;
    
    
#load an image file and convert it to the current display environment, adjusting for alpha info.
def LoadImage(name):
    return pyglet.resource.image(name);

def BuildLoadSprite(name): #, batch=None, group=None):
    image = pyglet.resource.image(name);
    return pyglet.sprite.Sprite(image); #, batch=batch, group=group);

def BuildLoadSpriteBatch(name, batch=None, group=None):
    image = pyglet.resource.image(name);
    return pyglet.sprite.Sprite(image, batch=batch, group=group);

def BuildSprite(image, batch=None, group=None):
    return pyglet.sprite.Sprite(image, batch=batch, group=group);
    
def LoadAnimFrame(path):
    pass;


def NewBatch():
    return pyglet.graphics.Batch();

def MakeRank(n):
    return pyglet.graphics.OrderedGroup(n);
    

#Horizontal flip of the supplied surface
def FlipImageH(image):
    image.anchor_x = image.width/2;
    image.anchor_y = image.height/2;
    image = image.get_texture().get_transform(flip_x=True);
    image.anchor_x = 0;
    image.anchor_y = 0;
    return image;
    
#vertical flip of the supplied surface
def FlipImageV(surf):
    image.anchor_x = image.width/2;
    image.anchor_y = image.height/2;
    image = image.get_texture().get_transform(flip_y=True);
    image.anchor_x = 0;
    image.anchor_y = 0;
    return image;

#def Rot90(surf, degrees):
#
#    return surf;

def MapBoundsToQuad(br):
    r0,r1,r2,r3 = (int(br[0]), int(br[1]), int(br[2]), int(br[3]));
    return (r0,r1, r2,r1, r2,r3, r0,r3);

def DrawRect(r, lineWidth = 1.0, color = (255, 255, 255, 255)):
    pyglet.gl.glLineWidth(lineWidth);
    pyglet.graphics.draw( 4, pyglet.gl.GL_LINE_LOOP,
        ('c4B', color * 4),
        ('v2i', MapBoundsToQuad(r.GetBounds())),
        );
    pass
    
def FillRect(r, color = (255, 255, 255, 255)):
    pyglet.graphics.draw( 4, pyglet.gl.GL_QUADS,
        ('c4B', color * 4),
        ('v2i', MapBoundsToQuad(r.GetBounds())),
        );
    pass
    
#def FillTriangle(verts, color = (255, 255, 255, 255)):
#    pyglet.graphics.draw( 4, pyglet.gl.GL_TRIANGLES,
#        ('c4B', color * 3),
#        ('v2i', MapVertsToTri(verts)),
#        );
#    pass
    
def PlaceFeature(f, image=None):
    if (not image): 
        image = f.image;
    image.set_position(f.left,f.bottom);
    pass

def MoveImageTo(image, x,y):
    image.set_position(x,y);
    pass

def MoveImage(image, dx,dy):
    image.x += dx;
    image.y += dy;
    pass

def RotatePict(f, deg):
    f.image.rotation = deg;
    pass
    
def SetAnchor(f, anchorX = 0, anchorY = 0):
    f.image.image.anchor_x = anchorX;
    f.image.image.anchor_y = anchorY;
    f.image.set_position(f.left+anchorX,f.bottom+anchorY);
    pass
    
def SetImageAnchorAndPos(image, anchorX = 0, anchorY = 0):
    image.anchor_x = anchorX;
    image.anchor_y = anchorY;
    image.set_position(x,y);
    pass
    
def SetVisible(image, flag):
    image.visible = flag;
    pass

def SetOpacity(image, opac):
    image.opacity = opac;
    pass

