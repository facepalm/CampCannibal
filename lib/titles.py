"""
	Programmer:	Keith G. Nemitz
	E-mail:		keithn@mousechief.com

	Version 0.0.1 Development

"""

#Main contains the setup and exit code for the game.

import sys
import os
import random

import knImages
import knEvents
import knFonts
import knFeatures
import knTimers
import knAudio


#---------------------------
#----------- main ----------
#---------------------------

titleFeatures = [];

def StartTitleScreens(window):
    #make sure we're in the correct directory
    fullpath = os.path.abspath(sys.argv[0]);
    dir = os.path.split(fullpath)[0];
    #change the directory to this file
    os.chdir(dir);

    knImages.Init(window);
    knFonts.Init();
    knEvents.Init(window);
    
    f = knFeatures.FtreString("Monstarred & Feathered",400,400);
    titleFeatures.append(f);
    f = knFeatures.FtreString("An interpretation of Martin Niemoller's poem, 'First they came...'",100,400,fSize=10);
    titleFeatures.append(f);
    
    knEvents.mousedownNotices.append(Skip);
    knEvents.keydownNotices.append(Skip);
    knAudio.PlayMusic("title.ogg");
    
    knEvents.AsyncTrigger(8.5,TitlesPage2);
    knEvents.RunWindow();
    #game is finished at this point, do any
    #uninitialization needed
    pass

skipFlag = False;

def Skip():
    global skipFlag
    skipFlag = True;
    StartScreen(None);
    pass
    
def TitlesPage2(args):
    global titleFeatures
    if (skipFlag): return;
    
    for f in titleFeatures:
        knFeatures.RemoveFeature(f);
    titleFeatures = [];

    f = knFeatures.FtreString("A Camp Cannibal Production",350,400, fSize = 18);
    titleFeatures.append(f);
    f = knFeatures.FtreString("In association with",100,340,fSize=10);
    titleFeatures.append(f);
    f = knFeatures.FtreString("Mousechief Co.",108,460,fSize=12);
    titleFeatures.append(f);

    knEvents.AsyncTrigger(7,TitlesPage3);
    pass
    
def TitlesPage3(args):
    global titleFeatures
    if (skipFlag): return;
    
    for f in titleFeatures:
        knFeatures.RemoveFeature(f);
    titleFeatures = [];
    
    names = ["Brad Busse","Harry Tormey","Keith Nemitz","George Cochrane"];
    random.shuffle(names);

    f = knFeatures.FtreString("DEVELOPERS",500,400,fSize=12);
    titleFeatures.append(f);
    y = 400;
    for name in names:
        f = knFeatures.FtreString(name,y,400, fSize = 18);
        titleFeatures.append(f);
        y -= 300/len(names);

    knEvents.AsyncTrigger(14.2,StartScreen);
    pass
    
def StartScreen(args):
    global titleFeatures
    
    knAudio.StopMusic();
    knEvents.keydownNotices = [];
    knEvents.mousedownNotices = [];
    
    for f in titleFeatures:
        knFeatures.RemoveFeature(f);
    titleFeatures = [];
    
    f = knFeatures.FtreText('''"Far upon the stormy crags of Transylvania, a social outcast explored the shunned craft of reanimating human tissues. One night, his devoted assistant vowed to quell the nearby village for undermining his master's dream of fully funded, indie R&D. Unleashed by the vengeful contractor, his master's experiment lumbered out,\nbeyond the castle walls..."''',400,400);
    titleFeatures.append(f);
    f = knFeatures.FtreString("-from 'Tales of our Struggle', Mad Scientist's Quarterly",340,450,fSize=12);
    titleFeatures.append(f);
    f = knFeatures.FtreText('''GOAL: KILL EVERY VILLAGER. (In a way that prevents factions of the village from uprising together against the good doctor, until it's too late.)\n\nWhen the creature is killed, you can reanimate it, by day, with parts from the deceased villagers, for another night's rampage.''',250,400);
    titleFeatures.append(f);

    f = knFeatures.FtreStrBtn("START", 50, 400);
    titleFeatures.append(f);
    f.clickAction = StartTutorial;
    pass

def StartTutorial(f):
    global titleFeatures
    
    for f in titleFeatures:
        knFeatures.RemoveFeature(f);
    titleFeatures = [];

    knEvents.StopWindowRun();
    pass
    
        
def xStartTutorial(f):
    global titleFeatures
    
    for f in titleFeatures:
        knFeatures.RemoveFeature(f);
    titleFeatures = [];
    
    knAudio.PlaySFX('wheelGrind.ogg');
    #for now, just jump to reanimate screen.
    reanimate.TransitionIn();
    pass
    
    