#meters.py


'''
Two meters with lables:
    Body Count - tracks by percentage the original number of villagers dead.
                It's length is segmented by faction colors.
    
    Outcry - track villagers' anger as a percentage of remaining population.
                It's length is segmented by faction colors.
                It's far end has a red zone that indicates point of Uprising.
'''


import pyglet
import knImages
import knRect
import faction
import game


#fctnMgr = faction.FactionManager();

popOutcryToUprisingPercentage = 0.67;

bcLabel, ocLabel = (None,None);
bcFrame, ocFrame = (None, None);
urLabel, urZone = (None, None);

startingPopulation = 0;



def Init():
    global bcLabel, ocLabel, bcFrame, ocFrame, urLabel, urZone, startingPopulation
    
    bcLabel = pyglet.text.Label("BODY COUNT:       % OF POPULATION", font_size=12, x = 15, y = 563, anchor_y = 'center');
    ocLabel = pyglet.text.Label("OUTCRY", font_size=12, x = 750, y = 563, anchor_x = 'center', anchor_y = 'center');
    
    bcFrame = knRect.Rect(10,590,312,574);
    ocFrame = knRect.Rect(488,590,790,574);
    urZone = knRect.Rect(488,590, 488+(300-(300*popOutcryToUprisingPercentage)), 575);
    
    urLabel = pyglet.text.Label("UPRISING", font_size=9, x = 490, y = 582, anchor_y = 'center');
    
    for fctn in game.state.factions.factions:
        startingPopulation += fctn.population;
        fctn.knStartPop = fctn.population;
    
    #TEST CODE to be removed.
#    kills = [100,200,300,400,500,600];
#    for fctn in game.state.factions.factions:
#        fctn.population -= kills.pop(0);
    pass

def Draw(): #draw the meters.
    bcLabel.draw();
    ocLabel.draw();
    knImages.DrawRect(bcFrame);
    knImages.DrawRect(ocFrame);
    knImages.FillRect(urZone, (255,0,0,100));
    urLabel.draw();
    
    x = bcFrame.left;
    xx = ocFrame.right-1;
    totalAlive = 0;
    for fctn in game.state.factions.factions:
        totalAlive += fctn.population;
        wid = 300 * (fctn.knStartPop-fctn.population) / startingPopulation;
        r = knRect.Rect(x,590,x+wid,575);
        knImages.FillRect(r, fctn.color);
        x += wid;
        
        wid = 300 * fctn.anger_level/6;
        r = knRect.Rect(xx-wid,590,xx,575);
        knImages.FillRect(r, fctn.color);
        xx -= wid;
        
    pctKillTot = 100*(startingPopulation-totalAlive) // startingPopulation;
    if (totalAlive != startingPopulation and pctKillTot == 0):
        pctKillTot = 1;
    pyglet.text.Label(str(pctKillTot), font_size=12, x = 155, y = 563, 
                        anchor_x = 'right', anchor_y = 'center').draw(); #DRAW
    
    pass       











