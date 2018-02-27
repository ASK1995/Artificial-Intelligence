from Models import *
from Global import *
from Global2 import *

import sys
import random
import pylab
import pandas as pd
import numpy as np
from printer import *



vacuum_cleaning_agent = Random()

m=10
n=10

mode = 1

if not mode:
    room = Global
    t2 = " -- No Walls"
else:
    room = Global2
    t2 = " -- Walls"

all_num_clean_cells = []
sequence = []
gtL = []
for i in range(50):
    print("\n\n\n")
    print("******************************%d***************************************" % i)
    dirty = 100 - mode * 14 #If there are walls it can't clean the walls
    
    state = room(n, m)

    ## Main loop
    limit = 8000 # prevent from running forever
    current = 0
    clean = []
    
    test = True
    while (test and current < limit):
        # print current world
        #print "Action " + str(num_actions)
        #environment.printCurrentWorld()

        # set up percept
        percept = state.getPercept()

        # agent performs a step
        action = vacuum_cleaning_agent.Move(percept)
        print("---Action %d has been taken---" % action)

        # update environment and counters
        test = state.updateWorld(action)
        current += 1

        # print num actions & num clean cells
        clean.append(state.getNumCleanCells())
        print("* " + str(current) + ", " + str(clean[current-1]))

        # for randomized agent experiments
        if clean[current-1] >= int(dirty * 0.90):
            test = 0


    all_num_clean_cells.append(clean)
    sequence.append(current-1)
    gtL.append(clean[current-1]/dirty)


fullResult = pd.DataFrame(all_num_clean_cells).T
fullResult.fillna(method="ffill", inplace=True)
fR = fullResult.mean(axis=1)
pylab.plot(fR)

pylab.xlabel('Moves')
pylab.ylabel('Cleaned squares')
pylab.title(vacuum_cleaning_agent.title + t2 + " -- Averaged")
pylab.grid(True)
pylab.show()
