#
#  knEvent.py
#
"""
	Programmer:	Keith G. Nemitz
	E-mail:		keithn@mousechief.com

	Version 0.0.1 Development
"""

import pyglet
import knFeatures


mousePos = [0,0];
mouseDelta = [0,0];
mouseDown = False;
keyMods = None;

mInputFaces = [];
mKeyBindingStack = []; #[list of dictionaries where each element is {key:handlerProc}]
mWindow = None;

keydownNotices = [];
mousedownNotices = [];



def NOP(): 
    pass

def NotifyAnyKeydown():
    for func in keydownNotices:
        func();
    pass

def NotifyAnyMousedown():
    for func in mousedownNotices:
        func();
    pass


def AsyncTrigger(secs,func):
    pyglet.clock.schedule_once(func,secs);
    pass

def ScheduleIdle(func,*args,**kwargs):
    pyglet.clock.schedule(func,args,kwargs);
    pass


def HandleMouseMotion(x,y, dx,dy):
    global mousePos
    mousePos = [x,y];
    
    mouseDelta[0] = dx;
    mouseDelta[1] = dy;
    
    knFeatures.MouseMoveFeatures(x,y, dx,dy, keyMods);
    pass

class knEventHandlers(object):    
    #@window.event
    def on_key_release(self, key,mods):
        global keyMods;
        keyMods = mods;
        
        if (key == pyglet.window.key.Q and mods): exit();
        
        NotifyAnyKeydown();

        try:
            handler = mKeyBindingStack[-1][key];
        except:
            handler = NOP;
        handler();
        pass
    
    #@window.event
    def on_mouse_motion(self, x,y, dx,dy):
        HandleMouseMotion(x,y, dx,dy);
        pass
        
    #@window.event
    def on_mouse_drag(self, x,y, dx,dy, buttons,mods):
        HandleMouseMotion(x,y, dx,dy);

        global keyMods
        keyMods = mods;
        pass
        
    #@window.event
    def on_mouse_press(self, x,y, button, mods):
        if (button & pyglet.window.mouse.LEFT == 0): return;
        global keyMods,mouseDown
        
        NotifyAnyMousedown();

        keyMods = mods;
        mouseDown = True;
        knFeatures.MousePressFeatures(x,y, keyMods);
        pass
        
    #@window.event
    def on_mouse_release(self, x,y, button, mods):
        if (button & pyglet.window.mouse.LEFT == 0): return;
        global keyMods,mouseDown

        keyMods = mods;
        mouseDown = False;
        knFeatures.MouseReleaseFeatures(x,y, keyMods);
        pass
        
    #@window.event
    def on_draw(self):
        mWindow.clear();
        knFeatures.DrawFeatures();
        pass


def Init(window):
    global mWindow
    mWindow = window;
    pass
    
def FullGameInit(gameState):
    
    #gameState.add_handler(HackEventHandling());
    pass


def RunWindow():
    mWindow.clear();
    mWindow.push_handlers(knEventHandlers());
    mWindow._kn_runFlag = True;
    
    while mWindow._kn_runFlag:
        pyglet.clock.tick();
        mWindow.dispatch_events();
        mWindow.dispatch_event('on_draw');
        mWindow.flip();
    
    mWindow.pop_handlers();
    pass

def StopWindowRun():
    mWindow._kn_runFlag = False;
    pass
    
    

def DoTime():
    pyglet.clock.tick();
    pass
    
    
def SetInputFaces(*faces):
    global mInputFaces
    
    mInputFaces = faces;
    pass


def PushKeyBindings(*bindings): #IMPORTANT: consider third tup item for a feature.
    bDict = {};
    for tup in bindings:
        bDict[tup[0]] = tup[1];
        
    mKeyBindingStack.append(bDict);
    pass

def PopKeyBindings():
    mKeyBindingStack.pop();
    pass



#--------------------------------------------- integration code - temporary

#import reanimate



class HackEventHandling(object):
    def on_key_release(self, key,mods):
        if (key == pyglet.window.key.R):
            AsyncTrigger(.2,FakeStartReanimate);
        pass



def FakeStartReanimate(args):
    reanimate.TransitionIn([],None);
    RunWindow();
    pass
    
    
    
    
    

