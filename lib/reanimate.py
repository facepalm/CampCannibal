
#reanimate.py

#to do
    # add labels to organ slots in monster chest cavity
    # replace instruction line with warning about aging organs.
        #generic tips list
    
    
    

import random

import knFeatures
import knImages
import knEvents
import knTimers
import knFonts

organsInLab = [("heart",0,'H'),("lungs",0,'S'),("lungs",1,'H'),
                ("liver",0,'T'),("kidneys",1,'T')];
organBins = {};
monsterOnSlab = None;
nxtBtn = None;

organsOnTheMarch = [];
monsterAttrs = {'S':2, 'T':1, 'H':10};
monsterAttrNames = {'S':"STRENGTH: ", 'T':"TOUGHNESS: ", 'H':"HEALTH: "};
monsterAttrStrs = {'S':None, 'T':None, 'H':None}; #features
monsterOrgans = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
monsterOrganSlots = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
monsterOrganLocs = {'lungs':(185,385), 'heart':(290,385), 
                    'liver':(185,280), 'kidneys':(290,280)};



def AnimateOrganPlacement(dt,args,kwargs):
    if (len(organsOnTheMarch) == 0): return;
    removeList = [];
    
    x,y = knEvents.mousePos;
    knFeatures.MouseTestFeatures(x,y);
    
    for f in organsOnTheMarch:
        f.MoveTo(f.timerY.ReadValue(),f.timerX.ReadValue());
        if (f.timerY.HasEnded() and f.timerX.HasEnded()):
            removeList.append(f);
    for f in removeList:
        f.timerY = None;
        f.timerX = None;
        organsOnTheMarch.remove(f);
    pass


                    #organ tuple: (organName, bonus, attribute affected)
def TransitionIn(organsGathered, monster):
    global organsInLab
    
    #AgeOrgans(); #unused organs lose one bonus every day. remove organs with bonus < 0.
    organsInLab += organsGathered;
    InitScreen(monster);
    pass

def InitScreen(monster):
    global monsterOnSlab,nxtBtn,toReviveStr,toNextNightStr
    
    monsterOnSlab = knFeatures.FtreSprite("onSlab",0,0);
    for key in monsterOrganLocs:
        x,y = monsterOrganLocs[key];
        f = knFeatures.FrameRect(y-50,x-50,y+50,x+50);
        f.SetVisible(False);
        f.lineThickness = 2.0;
        monsterOrganSlots[key] = f;
    
    toReviveStr = knFeatures.FtreString("To revive creature, drag in a set of organs.",450,235,fSize=12);
    toNextNightStr = knFeatures.FtreString("When ready to rampage, press 'It's Alive'.",450,235,fSize=16);
    toNextNightStr.SetVisible(False);
    
    y = 150;
    for key in ['H','S','T']:
        attrName = monsterAttrNames[key];
        attrVal = monsterAttrs[key];
        monsterAttrStrs[key] = knFeatures.FtreString(attrName+str(attrVal),y,240,fSize=18,fFont='Arial Bold');
        y -= 50;

    nxtBtn = knFeatures.FtreButton("itsAlive", 480,135);
    #nxtBtn = knFeatures.FtreStrBtn("IT'S ALIVE!", 520,235);
    nxtBtn.SetVisible(False);
    nxtBtn.clickAction = NextNight;
        
    organBins['H'] = knFeatures.FtreSprite("organBin",430,500);
    organBins['S'] = knFeatures.FtreSprite("organBin",230,500);
    organBins['T'] = knFeatures.FtreSprite("organBin",30,500);
    
    knFeatures.FtreString("Health Parts",450,630,fSize=12,fFont='Arial Bold');
    knFeatures.FtreString("Strength Parts",250,630,fSize=12,fFont='Arial Bold');
    knFeatures.FtreString("Toughness Parts",50,630,fSize=12,fFont='Arial Bold');
    
    for o in organsInLab:
        AddOrgan(o[0],o[1],o[2]);
    
    #button NEXT NIGHT enables when a full set of organs is in creature.
    knEvents.ScheduleIdle(AnimateOrganPlacement);
    pass



#
class FtreOrgan(knFeatures.FtreRect):
    def __init__(self, name, midy,midx):
        self.image = knImages.BuildLoadSprite(name+'.png');
        halfWid = self.image.width/2;
        halfHit = self.image.height/2;
        knFeatures.FtreRect.__init__(self, midx-halfWid, midy+halfHit,
                                            midx+halfWid, midy-halfHit);
        knImages.SetAnchor(self,halfWid,halfHit);
        
        self.followMouse = False;
        pass
    
    def Draw(self):
        self.image.draw();
        if (self.bonusImage):
            self.bonusImage.x = self.midx;
            self.bonusImage.y = self.midy;
            self.bonusImage.draw();
        if (knFeatures.currentHilite == self and not knEvents.mouseDown):
            knImages.DrawRect(self,2.0);
        pass

    def MoveTo(self,bottom,left):
        self._bottom = bottom;
        self._left = left;
        self.top = bottom+self._height;
        self.right = left+self._width;
        knImages.MoveImageTo(self.image, self.midx,self.midy);
        pass
        
    def Move(self,dx,dy):
        knImages.MoveImage(self.image, dx,dy);
        self._left += dx;
        self._top += dy;
        self.right += dx;
        self.bottom += dy;
        pass
        
    def TestPoint(self,x,y):
        if (knEvents.mouseDown):
            if (self.followMouse):
                #if dragging in creature, then hilite organ location.
                x,y = knEvents.mousePos;
                monsterOrganSlots[self.organName].SetVisible(x < 455);
                #follow the mouse
                self.Move(knEvents.mouseDelta[0], knEvents.mouseDelta[1]);
                return False;
        else:
            if (self.followMouse):
                self.DragReleased();
            self.followMouse = False;
            
        if (self.visible and self.enabled):
            return (x > self.left and y < self.top and 
                    x < self.right and y > self.bottom);
        return False;
        
    def ClickPoint(self,x,y):
        self.followMouse = False;
        
        if (self.visible and self.enabled and
                    (x > self.left and y < self.top and 
                    x < self.right and y > self.bottom)):
            self.followMouse = True;
            knFeatures.BringToFront(self);
            
        return self.followMouse;

    def DragReleased(self): #Put organ back in bin.
        for key in monsterOrganSlots:
            monsterOrganSlots[key].SetVisible(False);
            
        #don't move if already in its own bin.
        if (organBins[self.bin].TestPoint(self.midx,self.midy)): 
            if (monsterOrgans[self.organName] == self):
                monsterOrgans[self.organName] = None;
                CalcBonus(self.bin, -self.bonus);#remove bonus
            return;
        
        x,y = knEvents.mousePos;
        if (monsterOnSlab.TestPoint(x,y)):
            #bump existing organ
            f = monsterOrgans[self.organName];
            if (f):
                x,y = RandPosInBin(f.bin);
                f.March(x,y);
                CalcBonus(f.bin, -f.bonus);#remove bonus
                
            #place into monster
            monsterOrgans[self.organName] = self;
            x,y = monsterOrganLocs[self.organName];
            CalcBonus(self.bin, self.bonus); #add bonus
        else:
            #place back in bin
            if (self == monsterOrgans[self.organName]):
                monsterOrgans[self.organName] = None;
                CalcBonus(self.bin, -self.bonus);#remove bonus
            x,y = RandPosInBin(self.bin);
            
        self.March(x,y);
        nxtBtn.SetVisible(None not in monsterOrgans.values());
        toNextNightStr.SetVisible(nxtBtn.visible);
        toReviveStr.SetVisible(not nxtBtn.visible);
        pass
    
    def March(self, x, y):        
        self.timerX = knTimers.RangeTimer(900,self.left, x-self.width/2);
        self.timerY = knTimers.RangeTimer(900,self.bottom, y-self.height/2);
        organsOnTheMarch.append(self);
        pass
        

def AddOrgan(partName,bonus,bin):
    x,y = RandPosInBin(bin);
    f = FtreOrgan(partName,y,x);
    f.bin = bin;
    f.bonus = bonus;
    f.organName = partName;
    f.bonusImage = BonusImage(f,bonus);
    return f;

def CalcBonus(attr,bonus):
    #calc
    if (attr == 'H'): bonus *= 5;
    monsterAttrs[attr] += bonus;
    
    #update string
    s = monsterAttrNames[attr]+str(monsterAttrs[attr]);
    monsterAttrStrs[attr].UpdateString(s,fSize=18,fFont='Arial Bold');
    pass
    
def RandPosInBin(bin):
    y = {'T':90, 'S':290, 'H':490}[bin];
    return (random.randrange(550,730), random.randrange(y,y+85));

def BonusImage(f,bonus):
    if (bonus == 0): return None;
    
    if (f.bin == 'H'): bonus *= 5;
    render = knFonts.RenderStr('+' + str(bonus), size=18, font='Arial Bold');
    return render;
    
    
def NextNight(f):
    #kill everything!!!
    global monsterAttrStrs, monsterOrgans, monsterOrganSlots,organBins
    
    monsterAttrStrs = {'S':None, 'T':None, 'H':None}; #features
    monsterOrgans = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
    monsterOrganSlots = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
    organBins = {};
    
    knFeatures.allFeatures = [];
    knFeatures.currentHilite = None;
    
    knEvents.StopWindowRun();
    pass
        

