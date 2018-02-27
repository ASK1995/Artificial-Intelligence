from vacuum_cleaning_agent import *
import numpy

class RandomAgent(vacuum_cleaning_agent):
    def __init__(self):
        self.title = "Random"
        # self.multinomials = dict([((1,0,1), [0.3,0,0,0.7,0]), # (dirt, wall, home)
        #                     ((1,1,0), [0,0.1,0.1,0.8,0]),
        #                     ((1,1,1), [0,0.1,0.1,0.8,0.0]),
        #                     ((1,0,0), [0.1,0.1,0.1,0.7,0.0]),
        #                     ((0,0,1), [0.6,0.2,0.2,0,0.0]),
        #                     ((0,1,0), [0,0.5,0.5,0,0.0]),
        #                     ((0,1,1), [0,0.5,0.48,0,0.02]),
        #                     ((0,0,0), [0.4,0.3,0.3,0,0.0]),
        #                     ])
        self.multinomials = dict([((0,1,1), [0.3,0,0,0.7,0.02]), # (wall, dirt, home)
                                  ((1,1,0), [0,0.1,0.1,0.8,0.0]),
                                  ((1,1,1), [0,0.1,0.1,0.8,0.0]),
                                  ((0,1,0), [0.1,0.1,0.1,0.7,0.0]),
                                  ((0,0,1), [0.6,0.2,0.2,0,0.0]),
                                  ((1,0,0), [0,0.5,0.5,0,0.0]),
                                  ((1,0,1), [0,0.5,0.48,0,0.0]),
                                  ((0,0,0), [0.4,0.3,0.3,0,0.0]),
                            ])
        self.multinomials1 = dict([((1,0,1), [0.0,0.67,0.33,0,0.0]), # (wall, dirt, home)
                                   ((1,1,0), [0,0.0,0.0,1.0,0]),
                                   ((1,1,1), [0,0.0,0.0,1.0,0.0]),
                                   ((1,0,0), [0.0,0.67,0.33,0.0,0.0]),
                                   ((0,0,1), [0.7,0.15,0.15,0,0.0]), # at home, without wall and dirt, even stronger than (0,0,0)
                                   ((0,1,0), [0,0.0,0.0,1,0.0]),
                                   ((0,1,1), [0,0.0,0.0,1,0.0]),
                                   ((0,0,0), [0.70,0.15,0.15,0,0.0]),# should go ahead in most cases
                            ])

    def Move(self, percept):
        dirt, wall, home = percept
        action = list(numpy.random.multinomial(1, self.multinomials1[(dirt,wall,home)])).index(1) + 1
        return action

