from vacuum_cleaning_agent import *
import numpy

class NoMemory(vacuum_cleaning_agent):
    def __init__(self):
        self.title = "Memoryless Agent"

    def Move(self, percept):
        [wall, dirt, home] = percept
        if dirt == 1 and wall == 0 and home == 1:
            return vacuum_cleaning_agent.SUCK
        if dirt == 1 and wall == 1 and home == 0:
            return vacuum_cleaning_agent.SUCK
        if dirt == 1 and wall == 1 and home == 1:
            return vacuum_cleaning_agent.SUCK
        if dirt == 1 and wall == 0 and home == 0:
            return vacuum_cleaning_agent.SUCK

        if dirt == 0 and wall == 0 and home == 1:
            return vacuum_cleaning_agent.FORWARD
        if dirt == 0 and wall == 1 and home == 0:
            return vacuum_cleaning_agent.RIGHT
        if dirt == 0 and wall == 1 and home == 1:
            return vacuum_cleaning_agent.OFF
        if dirt == 0 and wall == 0 and home == 0:
            return vacuum_cleaning_agent.FORWARD

class Random(vacuum_cleaning_agent):
    def __init__(self):
        self.title = "Random Agent"
        self.multinomials = dict([((0,1,1), [0.3,0,0,0.7,0.02]), 
                                  ((1,1,0), [0,0.1,0.1,0.8,0.0]),
                                  ((1,1,1), [0,0.1,0.1,0.8,0.0]),
                                  ((0,1,0), [0.1,0.1,0.1,0.7,0.0]),
                                  ((0,0,1), [0.6,0.2,0.2,0,0.0]),
                                  ((1,0,0), [0,0.5,0.5,0,0.0]),
                                  ((1,0,1), [0,0.5,0.48,0,0.0]),
                                  ((0,0,0), [0.4,0.3,0.3,0,0.0]),
                            ])
        self.multinomials1 = dict([((1,0,1), [0.0,0.67,0.33,0,0.0]), 
                                   ((1,1,0), [0,0.0,0.0,1.0,0]),
                                   ((1,1,1), [0,0.0,0.0,1.0,0.0]),
                                   ((1,0,0), [0.0,0.67,0.33,0.0,0.0]),
                                   ((0,0,1), [0.7,0.15,0.15,0,0.0]), 
                                   ((0,1,0), [0,0.0,0.0,1,0.0]),
                                   ((0,1,1), [0,0.0,0.0,1,0.0]),
                                   ((0,0,0), [0.70,0.15,0.15,0,0.0]),
                            ])

    def Move(self, percept):
        [wall, dirt, home] = percept
        action = list(numpy.random.multinomial(1,self.multinomials1[(wall,dirt,home)])).index(1) + 1
        return action


class MemoryModel(vacuum_cleaning_agent):
    state = 0

    def __init__(self):
        self.state = 0
        self.title = "Memoryfull Agent"
    
    def Move(self, percept):
        [wall, dirt, home] = percept
        if self.state == 0 and dirt == 1:
            return vacuum_cleaning_agent.SUCK
        if self.state == 0 and wall == 0:
            return vacuum_cleaning_agent.FORWARD
        if self.state == 0 and wall == 1:
            self.state = 1
            return vacuum_cleaning_agent.RIGHT
        if self.state == 1 and wall == 1:
            self.state = 6
            return vacuum_cleaning_agent.RIGHT 
        if self.state == 1 and wall == 0:
            self.state = 2
            return vacuum_cleaning_agent.FORWARD
        if self.state == 2:
            self.state = 3
            return vacuum_cleaning_agent.RIGHT
        if self.state == 3 and dirt == 1:
            return vacuum_cleaning_agent.SUCK
        if self.state == 3 and wall == 0:
            return vacuum_cleaning_agent.FORWARD
        if self.state == 3 and wall == 1:
            self.state = 4
            return vacuum_cleaning_agent.LEFT
        if self.state == 4 and wall == 1:
            self.state = 6
            return vacuum_cleaning_agent.RIGHT
        if self.state == 4 and wall == 0:
            self.state = 5
            return vacuum_cleaning_agent.FORWARD
        if self.state == 5:
            self.state = 0
            return vacuum_cleaning_agent.LEFT
        if self.state == 6 and home == 1:
            return vacuum_cleaning_agent.OFF
        if self.state == 6 and wall == 0:
            return vacuum_cleaning_agent.FORWARD
        if self.state == 6 and wall == 1:
            return vacuum_cleaning_agent.RIGHT
        raise NotImplementedError("State change not possible.")

