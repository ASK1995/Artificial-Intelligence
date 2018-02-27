from Models import *
from Global import *
from Global2 import *
from printer import *

import sys
import random

vacuum_cleaning_agent = None
model=int(input('Enter Model:1 nomemory, 2 random, 3 MemoryModel '))
if model == 1:
    vacuum_cleaning_agent = NoMemory()
elif model == 2:
    vacuum_cleaning_agent = Random()
elif model == 3:
    vacuum_cleaning_agent = MemoryModel()
else:
    print('Model values should be 1,2 or 3  ')
    sys.exit(1)

m=10
n=10
    
mode=int(input('Map 1 or 2?'))
if(mode!=1 and mode!=2):
    print("default value of 1 taken as given value is not 1 or 2")
    mode=1

if(mode==1):
    state = Global(n, m)
    test = True
    clean = []
    current = 0
    limit = 2000
    while (test and current < limit):
        state.printCurrentWorld()
        percept = state.getPercept()
        action = vacuum_cleaning_agent.Move(percept)
        print("---Action %d---" % action)
        
        test = state.updateWorld(action)
        current += 1

        clean.append(state.getNumCleanCells())
        print("* " + str(current) + ", " + str(clean[current-1]))
    
        if clean[current-1] >= int(n*m*0.90):
            test = 0
            
        titler = vacuum_cleaning_agent.title + " -- No Walls"
        figs=vacuum_cleaning_agent.title+str(mode)+".png"
        state.stats(clean, titler)
        

elif(mode==2):
    state = Global2(n, m)
    test = True
    clean = []
    current = 0
    limit = 2000
    while (test and current < limit):
        state.printCurrentWorld()   
        percept = state.getPercept()
    
        action = vacuum_cleaning_agent.Move(percept)
        print("---Action %d---" % action)
        
        test = state.updateWorld(action)
        current += 1

        clean.append(state.getNumCleanCells())  
        print("* " + str(current) + ", " + str(clean[current-1]))
    
        if clean[current-1] >= int(n*m*0.90):
            test = 0
        
        titler = vacuum_cleaning_agent.title + " -- Walls"
        figs = vacuum_cleaning_agent.title+str(mode)+".png"
    
        state.stats(clean, titler)
        
