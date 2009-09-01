#
#  knFeatures.py

"""
	Programmer:	Keith G. Nemitz
	E-mail:		keithn@mousechief.com

	Version 0.0.1 Development

"""


import knRect
import knImages
import knFonts
import knEvents



allFeatures = [];
currentHilite = None;


def fNOP(feature):
    return;



class FtreRect(knRect.Rect):

    def __init__(self, left,top,right,bottom):
        knRect.Rect.__init__(self, left=left,top=top,right=right,bottom=bottom);
        
        allFeatures.append(self);
        
        self.enabled = True;
        self.visible = True;
        
        self.clickAction = fNOP;
        self.altHilite = None;
        self.animator = None;
        pass
    
    def Load(self): pass
    def Unload(self): pass
    
    def Draw(self): pass
    
    def DrawHilite(self):
        self.Draw();
        pass
    
    def SetOpacity(self, opac):
        pass
        
    def GetVisible(self):
        return self.visible;
        
    def GetEnabled(self):
        return self.enabled;
    
    def SetVisible(self, bool):
        self.visible = bool;
        pass
        
    def SetEnabled(self, bool):
        if (bool != self.enabled): self.ReqDraw();
        self.enabled = bool;
        pass
    
    def MoveTo(self,bottom,left):
        self._left = left;
        self._bottom = bottom;
        self.top = bottom+self._height;
        self.right = left+self._width;
        pass
        
    def Move(self,dx,dy):
        self._left += dx;
        self._top += dy;
        self.right += dx;
        self.bottom += dy;
        pass
        
    def Place(self): pass
    
    def TestPoint(self,x,y):
        if (self.visible and self.enabled):
            return (x > self.left and y < self.top and 
                    x < self.right and y > self.bottom);
        return False;
        
    def ClickPoint(self,x,y):
        return False;
        
    def xClickPoint(self,x,y):
        if (self.visible and self.enabled):
            return (x > self.left and y < self.top and 
                    x < self.right and y > self.bottom);
        return False;
        
    def GainHilite(self):
        pass
        
    def LoseHilite(self):
        pass
        
        


#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------



#
class FrameRect(FtreRect):
    def __init__(self, bottom,left,top,right):
        FtreRect.__init__(self, left,top,right,bottom);
        self.lineThickness = 1.0;
        pass
    
    def Draw(self):
        knImages.DrawRect(self,self.lineThickness);
        pass


#
class ColorRect(FtreRect):
    def __init__(self, bottom,left,top,right):
        FtreRect.__init__(self, left,top,right,bottom);
        self.color = (255,255,255,255);
        pass
        
    def Draw(self):
        knImages.FillRect(self, self.color);
        pass

#
class FtreImage(FtreRect):
    def __init__(self, name, bottom,left):
        self.image = knImages.LoadImage(name+'.png');
        FtreRect.__init__(self, left, bottom+self.image.height,
                                   left+self.image.width, bottom);
        pass
    
    def Draw(self):
        self.image.blit(self.left,self.bottom);
        pass

#                
class FtreSprite(FtreRect):
    def __init__(self, name, bottom,left):
        self.image = knImages.BuildLoadSprite(name+'.png');
        FtreRect.__init__(self, left, bottom+self.image.height,
                                   left+self.image.width, bottom);
        knImages.PlaceFeature(self);
        pass
    
    def Draw(self):
        self.image.draw();
        pass

#
class FtreButton(FtreRect):
    def __init__(self, name, bottom,left):
        self.image = knImages.BuildLoadSprite(name+'.png');
        self.imageHi = knImages.BuildLoadSprite(name+'HI.png');
        self.imagePs = knImages.BuildLoadSprite(name+'PS.png');
        FtreRect.__init__(self, left, bottom+self.image.height,
                                   left+self.image.width, bottom);
                                   
        knImages.PlaceFeature(self,self.image);
        knImages.PlaceFeature(self,self.imageHi);
        knImages.PlaceFeature(self,self.imagePs);
        pass
    
    def Draw(self):
        if (currentHilite == self):
            if (knEvents.mouseDown):
                self.imagePs.draw();
            else:
                self.imageHi.draw();
        else:
           self.image.draw();
        pass
                
#                
class FtreString(FtreRect):
    def __init__(self, s, midy,midx, fSize=24, fFont=knFonts.gDefaultFont):
        self.string = s;
        self.image = knFonts.RenderStr(s, size=fSize, font=fFont);
        self.image.x = midx;
        self.image.y = midy;
        halfWid = self.image.content_width/2;
        halfHit = self.image.content_height/2;
        FtreRect.__init__(self, midx-halfWid, midy+halfHit,
                                   midx+halfWid, midy-halfHit);
        pass
    
    def UpdateString(self, s, fSize=24, fFont=knFonts.gDefaultFont):
        self.string = s;
        self.image = knFonts.RenderStr(s, size=fSize, font=fFont);
        midx,midy = (self.midx, self.midy);
        self.image.x = midx;
        self.image.y = midy;
        halfWid = self.image.content_width/2;
        halfHit = self.image.content_height/2;
        self.SetBounds(midx-halfWid, midy+halfHit, midx+halfWid, midy-halfHit);
        pass
        
    def TestPoint(self,x,y):
        return False;
        
    def TestClick(self,x,y):
        return False;
    
    def Draw(self):
        self.image.draw();
        pass


#                
class FtreText(FtreRect):
    def __init__(self, s, midy,midx, fSize=12, width=600):
        self.string = s;
        self.image = knFonts.RenderText(s, size=fSize, wid=width);
        self.image.x = midx;
        self.image.y = midy;
        halfWid = self.image.content_width/2;
        halfHit = self.image.content_height/2;
        FtreRect.__init__(self, midx-halfWid, midy+halfHit,
                                   midx+halfWid, midy-halfHit);
        pass
    
    def TestPoint(self,x,y):
        return False;
        
    def TestClick(self,x,y):
        return False;
    
    def Draw(self):
        self.image.draw();
        pass


#                
class FtreStrBtn(FtreRect):
    def __init__(self, s, midy,midx, fSize=24):
        self.string = s;
        self.clickAction = fNOP;
        self.image = knFonts.RenderStr(s, font='Arial Bold',size=fSize);
        self.imageHi = knFonts.RenderStr(s, font='Arial Bold',size=fSize,color = (90,90,250,255));
        self.imagePs = knFonts.RenderStr(s, font='Arial Bold',size=fSize,color = (0,200,90,255));
        
        self.image.x,self.image.y = (midx,midy);
        self.imageHi.x,self.imageHi.y = (midx,midy);
        self.imagePs.x,self.imagePs.y = (midx,midy);

        halfWid = self.image.content_width/2;
        halfHit = self.image.content_height/2;
        FtreRect.__init__(self, midx-halfWid, midy+halfHit,
                                   midx+halfWid, midy-halfHit);
        pass
    
    def Draw(self):
        if (currentHilite == self):
            if (knEvents.mouseDown):
                self.imagePs.draw();
            else:
                self.imageHi.draw();
        else:
           self.image.draw();
        pass



        
#-------------------------------------------------

def RemoveFeature(f):
    if f in allFeatures:
        allFeatures.remove(f);
    pass
    
def BringToFront(f):
    RemoveFeature(f);
    allFeatures.append(f);
    pass
    
            
#-------------------------------------------------

clickedFeature = None;

def DrawFeatures():
    for f in allFeatures:
        if (f.visible):
            f.Draw();


def MouseMoveFeatures(x,y, dx,dy, mods):
    MouseTestFeatures(x,y);
    pass
    
def MouseTestFeatures(x,y):
    global currentHilite
    
    #search for hilites
    for f in reversed(allFeatures):
        if (f.visible and f.TestPoint(x,y)):
            currentHilite = f;
            return;
    currentHilite = None;
    pass


def MousePressFeatures(x,y, keyMods):
    global clickedFeature
    
    if (currentHilite):
        clickedFeature = currentHilite;
        clickedFeature.ClickPoint(x,y);
    pass
    
def MouseReleaseFeatures(x,y, keyMods):
    global clickedFeature
    
    if (currentHilite and currentHilite == clickedFeature):
        clickedFeature.clickAction(clickedFeature);
    
    clickedFeature = None;
    dx,dy = knEvents.mouseDelta;
    MouseMoveFeatures(x,y, dx,dy, keyMods);
    pass
    
