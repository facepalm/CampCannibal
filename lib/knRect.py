#
#  knRect.py

"""
	Programmer:	Keith G. Nemitz
	E-mail:		keithn@mousechief.com


	Version 0.0.1 Development
"""


class Rect(object):

    def __init__(self, left=0,top=0,right=0,bottom=0):
        assert left <= right and top >= bottom, "bad rectangle: "+str(self)
        
        self._left = left;
        self._bottom = bottom;
        self.top = top;
        self.right = right;
        pass

#    def __init__(self, bottom,left,wid=0,hit=0):
#        self._left = left;
#        self._bottom = bottom;
#        self.width = wid;
#        self.height = hit;
#
#        assert self._left <= self._right and self._top >= self._bottom, "bad rectangle: "+str(self)
#        pass


    def GetRect(self):
        return (self.left, self.top, self.width, self.height);
    
    def GetBounds(self):
        return (self.left, self.top, self.right, self.bottom);
        

    def SetRect(self, bottom,left,width,height):
        self._left = left;
        self._bottom = bottom;
        self.width = width;
        self.height = height;
        pass
    
    def SetBounds(self, left,top,right,bottom):
        self._left = left;
        self.top = top;
        self.right = right;
        self._bottom = bottom;
        pass
    
    def PtInRect(self,pt):
        return (pt[0] > self.left and pt[1] < self.top and \
                    pt[0] < self.right and pt[1] > self.bottom);
                    


    def __repr__(self):
        return "(%d,%d,%d,%d)"%(self.left,self.top,self.right,self.bottom);
        
    def PrintFull(self):
        print self;
        print '[',self.width,',',self.height,']  <',self.midx,',',self.midy,'>'
        pass
        

    @property
    def left(self): return self._left;
    
    @left.setter
    def left(self,value):
        self._left = value;
        self._width = self._right - value;
        self._midx = (value + self._right)/2;
        
        assert self._left <= self._right, "bad rectangle: "+str(self)
        pass
    

    @property
    def top(self): return self._top;
    
    @top.setter
    def top(self,value):
        self._top = value;
        self._height = value - self._bottom;
        self._midy = (value + self._bottom)/2;
        
        assert self._top >= self._bottom, "bad rectangle: "+str(self)
        pass
    

    @property
    def right(self): return self._right;
    
    @right.setter
    def right(self,value):
        self._right = value;
        self._width = value - self._left;
        self._midx = (value + self._left)/2;
        
        assert self._left <= self._right, "bad rectangle: "+str(self)
        pass
    

    @property
    def bottom(self): return self._bottom;
    
    @bottom.setter
    def bottom(self,value):
        self._bottom = value;
        self._height = self._top - value;
        self._midy = (value + self._top)/2;
        
        assert self._top >= self._bottom, "bad rectangle: "+str(self)
        pass
    

    @property
    def width(self): return self._width;
    
    @width.setter
    def width(self,value):
        self._width = value;
        self._right = self._left + value;
        self._midx = (self._left + self._right)/2;
        
        assert self._left <= self._right, "bad rectangle: "+str(self)
        pass
    

    @property
    def height(self): return self._height;
    
    @height.setter
    def height(self,value):
        self._height = value;
        self._top = self._bottom + value;
        self._midy = (self._top + self._bottom)/2;
        
        assert self._top >= self._bottom, "bad rectangle: "+str(self)
        pass
    

    @property
    def midx(self): return self._midx;
    
    @midx.setter
    def midx(self,value):
        self._midx = value;
        self._left = value - self._width/2;
        self._right = self._left + self._width;
        
        assert self._left <= self._right, "bad rectangle: "+str(self)
        pass
    

    @property
    def midy(self): return self._midy;
    
    @midy.setter
    def midy(self,value):
        self._midy = value;
        self._top = value + self._height/2;
        self._bottom = self._top - self.height;
        
        assert self._top >= self._bottom, "bad rectangle: "+str(self)
        pass
    



