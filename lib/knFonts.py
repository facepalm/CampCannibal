#
#  knFont.py
#
"""
	Programmer:	Keith G. Nemitz
	E-mail:		keithn@mousechief.com

	Version 0.0.1 Development
"""

import pyglet


#global names
gDefaultFont = None;  #defined to be the font added at init time.

fontColorWhite = (255,255,255,255);
fontColorBlack = (0,0,0,255);

fontDict = {};



def Init():
    global gDefaultFont;
    #pyglet.font.add_file('data/fonts/freesansbold.ttf');
    gDefaultFont = "Times New Roman";
    pyglet.font.load(gDefaultFont);
    pass

    
def AddFont(fileName, fontName):
    #pyglet.font.add_file(fileName);
    #action_man = pyglet.font.load(fontName)
    return None; #fontName
    
def RenderStr(s, font=gDefaultFont,size=24,color=(255,255,255,255)):
    image = pyglet.text.Label(s,font,size, color=color, 
                                anchor_x='center', anchor_y='center');
    return image;

def RenderText(s, font=gDefaultFont,size=24,color=(255,255,255,255),wid=None):
    image = pyglet.text.Label(s,font,size, color=color, multiline=True, width=wid, 
                                anchor_x='center', anchor_y='center'); 
    return image;

def RenderGlyphs(s, font=gDefaultFont,size=24,color=(255,255,255,255)):
    font = pyglet.font.load(font);
    glyphs = font.get_glyphs(s);
    

def PlaceText(f, image=None):
    if (not image): 
        image = f.image;
    image.x = f.left;
    image.y = f.bottom;
    pass

def SetOpacity(image, opac):
    image.color = image.color[:3]+(int(opac),);
    pass
    
