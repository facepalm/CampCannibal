#
#  knTimers.py
#
"""
	Programmer:	Keith G. Nemitz
	E-mail:		future@mousechief.com

	Version 0.0.1 Development
"""


from time import time
import math

import pyglet



def GetMilSecs():
    return int(time()*1000);

class RangeTimer:
    def __init__(self, duration, startVal=None, endVal=None):
        self.totalDuration = duration;
        self.startValue = startVal;
        self.startTime = time()*1000;
        self.endTime = self.startTime + duration;
        
        if (startVal == None): return;
            
        self.endValue = endVal;
        self.deltaValue = endVal - startVal;
        
        self.pauseValue = None;
        self.pauseTime = None;
        pass

    def ReadValue(self):
        if (self.pauseTime): return self.pauseValue;
        
        ct = time()*1000;
        
        if (self.startValue == None):
            if (ct >= self.endTime): return self.totalDuration;
            return time()*1000 - self.startTime;

        if (ct >= self.endTime):
            return self.endValue;
        else:
            return (( (ct-self.startTime) * self.deltaValue) / self.totalDuration) + self.startValue;
        pass

    def IsTicking(self):
        return (time()*1000 < self.endTime);

    def HasEnded(self):
        return (time()*1000 >= self.endTime);
    
    def EndTimer(self):
        self.endTime = time()*1000;
        pass
        
    def Restart(self):
        self.startTime = time()*1000;
        self.endTime = self.startTime + self.totalDuration;
        
        if (self.startValue):
            self.deltaValue = self.endValue - self.startValue;
        pass
    
    def Pause(self):
        self.pauseValue = self.ReadValue();
        self.pauseTime = time()*1000;
        pass
    
    def UnPause(self):
        delta = time()*1000 - self.pauseTime;
        self.startTime += delta;
        self.endTime += delta;
        self.pauseValue = None;
        self.pauseTime = None;
        pass
    

class PicketTimer(RangeTimer):
    def ReadValue(self):
        ct = time()*1000;
        if (ct >= self.endTime):
            RangeTimer.__init__(self, self.totalDuration, self.endValue, self.startValue);
        return (( (ct-self.startTime) * self.deltaValue) / self.totalDuration) + self.startValue;


class CycleTimer(RangeTimer):
    def ReadValue(self):
        ct = time()*1000;
        if (ct >= self.endTime):
            self.Restart();
            return self.endValue;
        return (( (ct-self.startTime) * self.deltaValue) / self.totalDuration) + self.startValue;

    
class AcDcTimer(RangeTimer):
    def __init__(self, duration, startVal, endVal): #assume values are floats.
        self.totalDuration = float(duration); #total time in milliseconds
        self.startValue = startVal; #starting position in pixels
        self.endValue = endVal;     #final position in pixels
        self.deltaValue = endVal - startVal;
        
        self.startTime = time()*1000;
        self.endTime = self.startTime + duration;
        pass

    def ReadValue(self):
        curTime = time()*1000;
        if (curTime >= self.endTime): 
            return self.endValue;
        pctT = float(curTime - self.startTime)/self.totalDuration;
        return (3.0-2.0*pctT)*pctT*pctT * self.deltaValue + self.startValue; #percent value

