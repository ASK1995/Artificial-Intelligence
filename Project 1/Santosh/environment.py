'''

'''

#YOU CAN SEE THE ROOM BY JUST RUNNING THIS FILE ON IT"S OWN.

import os
import os.path as op
import sys

import numpy as np
import random as rnd
import matplotlib.pyplot as plt

roomsize = 10

def addPair(a, b):
    return(a[0] + b[0], a[1] + b[1])

class Room(object):
    gridsize=roomsize+1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def __init__(self, walls):
        
        self.homeCoord = (1, 1)
        self.dirt = np.ones((self.gridsize, self.gridsize), dtype=int)
        self.wallCoord = np.zeros_like(self.dirt)
        self.wallSet = self.__makeWalls(walls)

        for w in self.wallSet:
            self.dirt[w] = 0
            self.wallCoord[w] = 1

        self.nDirt = np.sum(np.sum(self.gridsize))
        self.vacLoc = self.homeCoord
        self.vacOrient = 0
        
    def sumDirt(self):
        return np.sum(np.sum(self.dirt))

    # Make the interior walls somehow
    def __makeWalls(self, w):
        wallx = set([(kx, ky) for kx in [0, roomsize] for ky in range(self.gridsize)])
        wally = set([(ky, kx) for kx in [0, roomsize] for ky in range(self.gridsize)])

        if w:
            doors = {(5, 3), (5, 8), (3, 5), (8, 5)}
            wallsx = set([(5, ky) for ky in range(self.gridsize)])
            wallsy = set([(kx, 5) for kx in range(self.gridsize)])

            w = wallsx.union(wallsy).difference(doors)
        else:
            w = set()

        wallSet = wallx.union(wally.union(w))
        return wallSet

    def testwall(self):
        plt.imshow(self.wallCoord, cmap='Greys',  interpolation='nearest')
        plt.show()

    def getPercept(self):
        pw = self.__seeWall()
        pd = self.dirt[self.vacLoc]
        ph = (self.vacLoc == self.homeCoord and pw)
        return pd, pw, ph
    
    def __seeWall(self):
        return self.wallCoord[addPair(self.vacLoc, self.directions[self.vacOrient])]

    def updateWorld(self, action):

        if action == 1:
            self.vacLoc = addPair(self.vacLoc, self.directions[self.vacOrient])
        if action == 2:
            self.vacOrient = (self.vacOrient+ 1) % 4
        if action == 3:
            self.vacOrient = (self.vacOrient- 1) % 4
        if action == 4:
            self.dirt[self.vacLoc] = 0
        if action == 5:
            return False
        else:
            return True
    

if __name__ == "__main__":
    r = Room(True)
    r.testwall()
