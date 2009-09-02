import random
import math

NUMBER_OF_FACTIONS = 6 #number of factions in the town

SYNERGY_MU = 2 #average relationship between the factions. >1 indicates overall like
SYNERGY_SIGMA = 0.05 #std deviation of relationships

STR_MU = 0.5 #average strength of each faction
STR_SIGMA = 0.05 #std dev of str

ANGER_PER_POP_PERCENT = 1 #anger % gained per pop % lost

FACTION_COLORS = [  (150,050,050,100),(050,050,150,100), #IMPORTANT: change these to match hat colors.
                    (150,050,150,100),(255,050,150,100),
                    (150,050,255,100),(150,055,150,100)   ];
#random.shuffle(FACTION_COLORS);



class Faction():
    '''An independent group of people in the city'''
    def __init__(self, pop=0):
        self.population = pop if pop else random.randint(900,1000)
        self.anger_level = random.random()/10
        self.strength = random.gauss(STR_MU,STR_SIGMA)
        self.fresh_dead = 0
        self.change_in_anger_level = 0.0
        self.color = FACTION_COLORS.pop(0);

    @property 
    def perc_dead(self):
        return 1.0*self.fresh_dead/self.population if self.fresh_dead else 0
    

    def process_dead(self, perc=0.0):
        new_anger_perc = perc if perc else self.perc_dead
        self.change_in_anger_level += new_anger_perc*ANGER_PER_POP_PERCENT

    def new_round (self):
        self.population -= self.fresh_dead
        self.fresh_dead = 0
        self.anger_level = 0.8*self.anger_level + 0.2*self.change_in_anger_level
        self.anger_level = min(1,max(self.anger_level,0))
        self.change_in_anger_level = 0
    

class FactionManager():
    '''Class that Handles Factions'''
    def __init__(self):
        self.factions=[] #this will hold our town factions
        self.faction_relationships = [] #this will hold our town interaction graph
        for i in range(NUMBER_OF_FACTIONS):
            self.factions.append(Faction()) #make the faction
            self.faction_relationships.append([])
            for j in range(NUMBER_OF_FACTIONS):
                self.faction_relationships[i].append(random.gauss(SYNERGY_MU,SYNERGY_SIGMA))

    def new_round(self):
        for ei,i in enumerate(self.factions):            
            for ej,j in enumerate(self.factions):
                if i==j: continue
                perc=i.perc_dead*self.faction_relationships[ei][ej]
                if perc: j.process_dead(perc)
            i.process_dead()
        for i in self.factions: 
            i.new_round()

    def on_death(faction,n=1):
        self.factions[faction].fresh_dead += n        

    def get_angry_meter(self):
        return map(lambda x : x.population * x.anger_level, self.factions)

    def kill_em_all_adolf(self):
        print sum(self.get_angry_meter()), self.get_angry_meter()
        for i in range(10):
            for f in self.factions:
                f.fresh_dead += min(f.population,random.randint(0,10))
            self.new_round()
            print sum(self.get_angry_meter()), self.get_angry_meter()   

    def kill_one_adolf(self):
        print sum(self.get_angry_meter()), self.get_angry_meter()
        for i in range(10):
            f = random.choice(self.factions)
            f.fresh_dead += min(f.population,NUMBER_OF_FACTIONS*random.randint(0,10))
            self.new_round()
            print sum(self.get_angry_meter()), self.get_angry_meter()           
