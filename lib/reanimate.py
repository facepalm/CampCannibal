
#reanimate.py

#to do
    #add organ aging: added but commented out.
    
    

import random

import knFeatures
import knImages
import knEvents
import knTimers
import knFonts


healthPerBonus = 5;

organsInLab = [("heart",1,'H'),("lungs",1,'S'),("lungs",2,'H'),
                ("liver",1,'T'),("kidneys",2,'T')];
organBins = {};
monsterOnSlab = None;
nxtBtn = None;

organsOnTheMarch = [];
monsterAttrs = {'S':2, 'T':1, 'H':10};
monsterAttrNames = {'S':"STRENGTH: ", 'T':"TOUGHNESS: ", 'H':"HEALTH: "};
monsterAttrStrs = {'S':None, 'T':None, 'H':None}; #features
monsterOrgans = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
monsterOrganSlots = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
monsterOrganLocs = {'lungs':(195,370), 'heart':(285,370), 
                    'liver':(195,280), 'kidneys':(285,280)};
monsterOrganPulses = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #timers
monsterOrganLabels = [];
artistAppreciation = None;

tips = [    "To reanimate creature, drag in a set of organs.",
            "Organs weaken every day. Dead ones are discarded.",
            ];

def AnimateOrganPlacement(dt,args,kwargs):
    PulseOrgans();
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

def PulseOrgans():
    for key in monsterOrganPulses:
        if (monsterOrgans[key]):
            val = monsterOrganPulses[key].ReadValue();
            monsterOrgans[key].image.scale = 1.1 if (val >= 9) else 1.0;
    pass

                    #organ tuple: (organName, bonus, attribute affected)
def TransitionIn(organsGathered, monster):
    global organsInLab
    
    AgeOrgans(); #unused organs lose one bonus every day. remove organs with bonus < 0.
    organsInLab += organsGathered;
    InitScreen(monster);
    pass

def InitScreen(monster):
    global monsterOnSlab,nxtBtn,toReviveStr,toNextNightStr, artistAppreciation, monsterAttrs
    
    monsterOnSlab = knFeatures.FtreSprite("onSlab",0,0);
    for key in monsterOrganLocs:
        x,y = monsterOrganLocs[key];
        f = knFeatures.FrameRect(y-45,x-45,y+45,x+45);
        f.SetVisible(False);
        f.lineThickness = 2.0;
        monsterOrganSlots[key] = f;
        f = knFeatures.FtreString(key.upper(),y,x,fSize=9);
        monsterOrganLabels.append(f);
    
    tip = tips.pop(0) if len(tips) else "";
    toReviveStr = knFeatures.FtreString(tip,20,235,fSize=12);
    toNextNightStr = knFeatures.FtreString("When ready to rampage, press 'It's Alive'.",20,235,fSize=16);
    toNextNightStr.SetVisible(False);
    
    y = 415;
    monsterAttrs = {'S':2, 'T':1, 'H':10};
    for key in ['H','S','T']:
        attrName = monsterAttrNames[key];
        attrVal = monsterAttrs[key];
        monsterAttrStrs[key] = knFeatures.FtreString(attrName+str(attrVal),y,560,fSize=18,fFont='Arial Bold');
        y -= 200;

    nxtBtn = knFeatures.FtreButton("itsAlive", 480,135);
    #nxtBtn = knFeatures.FtreStrBtn("IT'S ALIVE!", 520,235);
    nxtBtn.SetVisible(False);
    nxtBtn.clickAction = NextNight;
    nxtBtn.monster = monster;
        
    organBins['H'] = knFeatures.FtreSprite("organBin",430,500);
    organBins['S'] = knFeatures.FtreSprite("organBin",230,500);
    organBins['T'] = knFeatures.FtreSprite("organBin",30,500);
    
    knFeatures.FtreString("Health Parts",450,630,fSize=12,fFont='Arial Bold');
    knFeatures.FtreString("Strength Parts",250,630,fSize=12,fFont='Arial Bold');
    knFeatures.FtreString("Toughness Parts",50,630,fSize=12,fFont='Arial Bold');
    
    artistAppreciation = knFeatures.FtreString("art by Miriam Sherry", 12, 740, fSize=8);
    
    timings = [300,400,500,600];
    random.shuffle(timings);
    for key in monsterOrganPulses:
        monsterOrganPulses[key] = knTimers.CycleTimer(timings.pop(),0,10);
        
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
    if (attr == 'H'): bonus *= healthPerBonus;
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
    
    if (f.bin == 'H'): bonus *= healthPerBonus;
    render = knFonts.RenderStr('+' + str(bonus), size=18, font='Arial Bold');
    return render;
    
def AgeOrgans():
#    deadOrgans = [];
#    for o in organsInLab:
#        if (o[1] == 0):
#            deadOrgans.append(o);
#            continue;
#        o[1] -= 1;
#    for o in deadOrgans:
#        organsInLab.remove(o);
    pass
    
    
    
def NextNight(f):
    #kill everything!!!
    global monsterAttrStrs, monsterOrgans, monsterOrganSlots,organBins, monsterOrganLabels, artistAppreciation
    
    monsterAttrStrs = {'S':None, 'T':None, 'H':None}; #features
    monsterOrgans = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
    monsterOrganSlots = {'lungs':None, 'heart':None, 'liver':None, 'kidneys':None}; #features
    monsterOrganLabels = [];
    artistAppreciation = None;
    organBins = {};
    
    knFeatures.allFeatures = [];
    knFeatures.currentHilite = None;
    
    #put attribute values generated by the parts back into the main monster dataStruct
#    f.monster.health = monsterAttrs['H'];
#    f.monster.strength = monsterAttrs['S'];
#    f.monster.toughness = monsterAttrs['T'];
    
    knEvents.StopWindowRun();
    pass
        

