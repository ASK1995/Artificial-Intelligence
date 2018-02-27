from vacuum_cleaning_agent import *
from Global import *

import numpy
import pylab

class BestNoMemory(vacuum_cleaning_agent):
    actions = [0] * 8
    def __init__(self,a):
        self.actions = a

    def Move(self, percept):
        [wall, dirt, home] = percept
        if dirt == 1 and wall == 0 and home == 1:
            return self.actions[0]
        if dirt == 1 and wall == 1 and home == 0:
            return self.actions[1]
        if dirt == 1 and wall == 1 and home == 1:
            return self.actions[2]
        if dirt == 1 and wall == 0 and home == 0:
            return self.actions[3]

        if dirt == 0 and wall == 0 and home == 1:
            return self.actions[4]
        if dirt == 0 and wall == 1 and home == 0:
            return self.actions[5]
        if dirt == 0 and wall == 1 and home == 1: 
            return self.actions[6]
        if dirt == 0 and wall == 0 and home == 0:
            return self.actions[7]

def performance(clean, draw):
    print numpy.mean([x*1.0 / y for x,y in zip(clean, range(1,len(clean)+1))])
    if draw == 1:
        pylab.plot(range(1,len(clean)+1), clean)
        pylab.show()

def brute_force(max_steps):
    best_action_num = 0
    clean = 0

    actions = [1, 4, 4, 1, 2, 2, 2, 2]

    agent = FakeNoMemory(actions)

    n = 4
    m = 4
    p = 1.0

    state = Global(n, m, p)

    limit = max_steps   
    test = True
    current = 0
    clean = [0] * max_steps
    while (test and current < limit):
        print "Action " + str(current)
        state.printCurrentWorld()

        percept = state.getPercept()

        action = agent.takeStep(percept)

        test = state.updateWorld(action)

        clean[current] = state.getNumCleanCells()
        current += 1
        print str(current) + ", " + str(clean)

    return clean
