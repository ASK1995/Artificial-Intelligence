from vacuum_cleaning_agent import *
import os
import random
import numpy
import pylab

class Global2:
    world = None
    n = 0
    m = 0
    p = 1
    INITIAL_X = 0
    INITIAL_Y = 0
    clean = 0
    current_x = 0
    current_y = 0
    current_dire = 0

    def __init__(self, n, m):
        self.n = n
        self.m = m

        self.INITIAL_X = 0 
        self.INITIAL_Y = m-1 

        self.clean = 0

        self.world = [1]*n*m

        self.current_x = self.INITIAL_X
        self.current_y = self.INITIAL_Y
        self.current_dire = vacuum_cleaning_agent.NORTH 

    def getPercept(self):
        wall = self.__isWallAhead__()
        dirt = self.world[self.current_y*self.n+self.current_x]
        home = 1 if self.current_x == self.INITIAL_X and self.current_y == self.INITIAL_Y else 0
        return [wall, dirt, home]

    def __isWallAhead__(self):
        temp_x = self.current_x
        temp_y = self.current_y
        if self.current_dire == vacuum_cleaning_agent.NORTH:
            temp_y -= 1
        if self.current_dire == vacuum_cleaning_agent.EAST:
            temp_x += 1
        if self.current_dire == vacuum_cleaning_agent.SOUTH:
            temp_y += 1
        if self.current_dire == vacuum_cleaning_agent.WEST:
            temp_x -= 1

        if temp_x < 0 or temp_y < 0 or temp_x >= self.n or temp_y >= self.m or (temp_x==5 and (temp_y not in [5, 6, 7])) or (temp_y==6 and (temp_x not in [4, 5, 6])):
            return 1
        else:
            return 0

    def updateWorld(self, action):
        if action == vacuum_cleaning_agent.FORWARD and self.__isWallAhead__() != 1:
            if self.current_dire == vacuum_cleaning_agent.NORTH:
                self.current_y -= 1
            if self.current_dire == vacuum_cleaning_agent.EAST:
                self.current_x += 1
            if self.current_dire == vacuum_cleaning_agent.SOUTH:
                self.current_y += 1
            if self.current_dire == vacuum_cleaning_agent.WEST:
                self.current_x -= 1
        if action == vacuum_cleaning_agent.RIGHT:
            self.current_dire = (self.current_dire + 1) % 4
        if action == vacuum_cleaning_agent.LEFT:
            self.current_dire = (self.current_dire - 1) % 4
        if action == vacuum_cleaning_agent.SUCK:
            if self.world[self.current_y*self.n+self.current_x] != 0:
                self.world[self.current_y*self.n+self.current_x] = 0
                self.clean += 1
        if action == vacuum_cleaning_agent.OFF:
            return False
        else:
            return True

    def getNumCleanCells(self):
        return self.clean

    def printCurrentWorld(self):
        w = self.world
        m = self.m
        n = self.n
        x = self.current_x
        y = self.current_y
        f = self.current_dire

        for row in range(0, m):
            print("+--"*n + "+")

            string = ""
            for col in range(0, n):
                if w[row*n+col] == 1:
                    string += "|*"
                else:
                    string += "| "
                if row == y and col == x:
                    if f == vacuum_cleaning_agent.NORTH:
                        string += "N"
                    if f == vacuum_cleaning_agent.EAST:
                        string += "E"
                    if f == vacuum_cleaning_agent.SOUTH:
                        string += "S"
                    if f == vacuum_cleaning_agent.WEST:
                        string += "W"
                else:
                    string += " "
            print(string + "|")

        print("+--"*n + "+")


    def stats(self, clean, title):
        print("averaged performance vs ideal case is: %f" % numpy.mean([x*1.0 / y for x,y in zip(clean, range(1,len(clean)+1))]))
        pylab.plot(range(1,len(clean)+1), clean)
        pylab.xlabel('number of actions')
        pylab.ylabel('number of clean cells')
        pylab.title(title)
        pylab.grid(True)
        pylab.show()
