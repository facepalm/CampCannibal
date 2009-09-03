import random

def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


class mapgen():
    def __init__(self,width=32,height=32):
        self.width=width
        self.height=height
        self.grid = [[simpleTile('#',x,y) for y in range(height)] for x in range(width)]

        #exit portal
        exitx=random.choice(range(width/2+1,width-1))
        self.grid[exitx][0].char='#'
        Walker(self,exitx,0,quad=4,d=3,req_loop=False)
        
        #portal to exit portal
        stg1x=random.choice(range(3*width/4+1,width-1))
        self.grid[stg1x][self.height/2].char='.'
        Walker(self,stg1x,self.height/2,quad=4,d=1,req_loop=False)
        Walker(self,stg1x,self.height/2,quad=3,d=3,req_loop=False)

        #portal to portal
        stg2y=random.choice(range(3*height/4+1,height-1))
        self.grid[self.width/2][stg2y].char='.'
        Walker(self,self.width/2,stg2y,quad=3,d=2,req_loop=False)
        Walker(self,self.width/2,stg2y,quad=2,d=0,req_loop=False)

        #portal to portal
        stgx=random.choice(range(1,width/4))
        self.grid[stgx][self.height/2].char='.'
        Walker(self,stgx,self.height/2,quad=2,d=3,req_loop=False)
        Walker(self,stgx,self.height/2,quad=1,d=1,req_loop=False)
        
        #portal to portal
        stgy=random.choice(range(1,3*height/4))
        self.grid[self.width/2][stgy].char='.'
        Walker(self,self.width/2,stgy,quad=2,d=3,req_loop=False)
        Walker(self,self.width/2,stgy,quad=1,d=1,req_loop=False)
        
        for i in range(400):
            for q in [1,2,3,4]:
                g=self.quad_grid(q)
                space_tiles=filter(lambda x: x.char != '#',flatten(g))
                if len(space_tiles)==0:
                    print "ERROR!  No empty tiles found!"
                    break
                t=random.choice(space_tiles)
                Walker(self,t.x,t.y,quad=q)


            
        g=self.quad_grid(1)        
        space_tiles=filter(lambda x: x.char == '.',flatten(g))   
        random.choice(space_tiles).char='@'        
        
        g=self.quad_grid(1)        
        space_tiles=filter(lambda x: x.char == '.',flatten(g))   
        random.choice(space_tiles).char='F'  
        
        space_tiles=filter(lambda x: x.char == '.',flatten(self.grid)) 
        for i in range(30):       
            random.choice(space_tiles).char='b' 
        
    def quad_grid(self,quad=1):
        '''
        Given a desired grid quandrant, returns that quarter of the total map
        '''
        if quad==1:
            t=self.grid[0:self.width/2]
            t=[m[0:self.height/2] for m in t]
            return t
        if quad==2:
            t=self.grid[0:self.width/2]
            t=[m[self.height/2:self.height] for m in t]
            return t
        if quad==3:
            t=self.grid[self.width/2:self.width]
            t=[m[self.height/2:self.height] for m in t]
            return t
        if quad==4:
            t=self.grid[self.width/2:self.width]
            t=[m[0:self.height/2] for m in t]
            return t

    def print_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                print self.grid[x][y].char,
            print
        
    def is_fully_inside(self,x,y,grid=-1):
        if grid==1 and x>0 and y>0 and x < self.width/2 and y < self.height/2:
            return True
        if grid==2 and x>0 and y>self.height/2 and x < self.width/2 and y < self.height-1:
            return True
        if grid==3 and x>self.width/2 and y>self.height/2 and x < self.width-1 and y < self.height-1:
            return True
        if grid==4 and x>self.width/2 and y>0 and x < self.width-1 and y < self.height/2:
            return True
        if grid==-1 and not (x<1 or y<1 or x >= self.width-1 or y >= self.height-1):
            return True
        return False
        
class simpleTile():
    def __init__(self,char,x,y):
        self.char=char
        self.x=x
        self.y=y
        
class Walker():
    def __init__(self,system,x,y,quad=1,d=-1,req_loop=True,duration=30):
        oldd=-1
        self.x=x
        self.y=y
        self.grid=system.grid
        self.quad=quad
        self.visited=[self.grid[x][y]]
        self.loop=req_loop
        self.burn=False
        if d==-1:
            d=random.randint(0,3)
            
        for tmp in range(duration):
            for i in range(3): #make each 'run' at least two squares
                if d==0:
                    self.x -= 1
                elif d==1:
                    self.y -= 1     
                elif d==2:
                    self.x += 1
                else:
                    self.y += 1
                    
                if not system.is_fully_inside(self.x,self.y,self.quad):
                    break    
                    
                if not self.is_valid():
                    if self.is_end_point():
                        self.visited.append(self.grid[self.x][self.y])
                        if len(self.visited) > 2:
                            self.burn=True
                    break
                
                self.visited.append(self.grid[self.x][self.y])
            
            if not system.is_fully_inside(self.x,self.y,self.quad) or not self.is_valid():
                break    

            dperc=random.randint(1,100)
            oldd=d
            if dperc>50:
                d=oldd
            elif dperc > 25:
                d=(4+oldd+1)%4
            else:
                d=(4+oldd-1)%4

        if self.burn or not self.loop:
            self.burn_in()

    def burn_in(self):
        for x in self.visited:
            if x.char=='#':
                x.char='.'
                
    def is_valid(self):
        n=self.get_neighbors()
        blank_count=0
        for x in n:
            if x in self.visited or x.char != '#':
                 blank_count += 1
        if blank_count >= 2:
            return False
        return True
        
    def is_end_point(self):
        n=self.get_neighbors()
        blank_count=0
        for x in n:
            if x in self.visited or x.char != '#':
                 blank_count += 1
        if blank_count == 2:
            return True
        return False

    def get_neighbors(self):
        l=self.grid[self.x-1][self.y]      
        r=self.grid[self.x+1][self.y]       
        u=self.grid[self.x][self.y-1]   
        d=self.grid[self.x][self.y+1]
        return [l,r,u,d]
  
        
if __name__ == '__main__':
	m=mapgen()
	m.print_grid()


