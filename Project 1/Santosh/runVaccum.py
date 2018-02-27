'''
Santosh Kumar Aenugu, Daniel Magee
'''

import os 
import os.path as op
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import subprocess as sp
import shlex

from NoMemory import *
from MemoryModel import *
from RandomAgent import *
from environmentDan import *

thispath = op.abspath(op.dirname(__file__))
impath = op.join(thispath, "images")
binpath = op.join(thispath, "bin")
exe = op.join(binpath, "vacAgent")

mpl.rcParams['lines.linewidth'] = 3
#mpl.rcParams['lines.markersize'] = 8
mpl.rcParams["figure.figsize"] = 14,8
mpl.rcParams["figure.titlesize"]="x-large"
mpl.rcParams["figure.titleweight"]="bold"
mpl.rcParams["grid.alpha"] = 0.5
mpl.rcParams["axes.grid"] = True
mpl.rcParams["savefig.dpi"] = 1000
mpl.rcParams["savefig.bbox"] = "tight"

MAXACTION = 50

def runexperiment(room, agent):
    origDirt = room.sumDirt()
    howDirty = [origDirt]
    runFlag=True
    while runFlag and len(howDirty) < MAXACTION:
        #room.printWorld()

        perc = room.getPercept()

        act = agent.Move(perc)

        runFlag = room.updateWorld(act)
        print(room.dirt)

        howDirty.append(origDirt - room.sumDirt())

    return howDirty

        
# FOR CPP VERSION
# def getcsv():
#     fcsv = [k for k in os.listdir(thispath) if k.endswith('csv')]
#     fcsv = fcsv[0]
#     df = pd.read_csv(fcsv)
#     os.remove(fscv)
#     df.columns=["Turns", "Dirty"]
#     return df

# def runexperiment(runline):
#     splitrun = shlex.split(runline)
#     proc = sp.Popen(splitrun)
#     sp.Popen.wait(proc)
#     return getcsv()
    
# sp.call(["make"])
roomsize = 100
wallstr = ["No Walls", "Walls"] 
agents = [NoMemory, MemoryModel, RandomAgent]
f, ax = plt.subplots(1, 2)
ai = ax.ravel()

# Runs go - walls/nowalls : increasing dirt : types of agents. 
# Number of dirty cells
dfRand = pd.DataFrame(columns=wallstr)
for wall in range(2):
    axi = ai[wall]
    for typ in range(3):
        agency = agents[typ]()
        quarters = Room(wall)
        if typ == 2:
            siv = []
            for k in range(45):
                df = runexperiment(quarters, agency)
                
        
        df = runexperiment(quarters, agency)
        print(df)
        axi.plot(list(range(len(df))), df)
        
    axi.set_ylabel("Number of dirty tiles")
    axi.set_xlabel("Number of turns")
    axi.set_title(wallstr[wall])
    axi.legend([t().title for t in agents])
    
plt.show()
dfRand.to_csv("RandomAgent" + wallstr[wall] + ".csv")
    
    
