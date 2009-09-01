#knAudio.py

"""
	Programmer:	Keith G. Nemitz
	E-mail:		keithn@mousechief.com

	Version 0.0.1 Development

"""

import pyglet
import knTimers


daSong = None
daSinger = None;
faderTimer = None;

#-------------------------------------------

def LoadSFX(name):
    return pyglet.resource.media(name,streaming=False);

def PlaySFX(sfx):
    if (type(sfx) == type('str')):
        sfx = pyglet.resource.media(sfx,streaming=False);
    sfx.play();
    pass

#-------------------------------------------
def PrepMusic(name):
    global daSong
    daSong = pyglet.resource.media(name, streaming=True)
    pass
    
def PlayMusic(name):   #, loopCount=1
    global daSinger, daSong
    
    if (daSinger and daSinger.playing): daSinger.pause();
    
    if (daSong == None):
        daSong = pyglet.resource.media(name, streaming=True)
    daSinger = daSong.play();
    #daSinger.eos_action = daSinger.EOS_PAUSE;
    daSong = None;
    pass

def IsMusicPlaying():
    return (daSinger and daSinger.playing);

def StopMusic():
    global daSinger

    if (daSinger and daSinger.playing): 
        daSinger.pause();
        daSinger = None;
    pass
    
def GetMusicVol():
    if (daSinger): 
        return daSinger.volume;
    return 0.0;
    
def MusicFader(dt):
    global faderTimer, daSinger
    
    if (faderTimer == None): return;
    if (daSinger.playing == False or faderTimer.HasEnded()): 
        pyglet.clock.unschedule(MusicFader);
        faderTimer = None;
        daSinger = None;
        return;
    value = faderTimer.ReadValue();
    daSinger.volume = value;
    pass
    
def FadeMusicOut(milsecs):
    global faderTimer, daSinger

    if (daSinger == None): return;
    if (daSinger.playing == False): 
        daSinger = None;
        return;

    if (faderTimer or daSinger == None): return;
    faderTimer = knTimers.RangeTimer(milsecs,1.0,0.0);
    pyglet.clock.schedule_interval(MusicFader, 0.01)
    pass
    
