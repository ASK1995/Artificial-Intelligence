from __future__ import print_function

import Solver
import sys
import os
import os.path as op
import re
import statsmodels.api as sm

import matplotlib as mpl
mpl.use("Agg")  # This lets you plot (and save) if you run remotely.

import matplotlib.pyplot as plt
import pandas as pd
from numpy import *
import collections
import json

#thispath = op.abspath(op.dirname(__file__))
thispath = op.abspath(os.getcwd())
impath = op.join(thispath, "images")


mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams["figure.figsize"] = 7, 5
mpl.rcParams["figure.titlesize"]="xx-large"
mpl.rcParams["figure.titleweight"]="bold"
mpl.rcParams['axes.titlesize']="x-large"   # fontsize of the axes title 
mpl.rcParams['axes.labelsize']="large"
mpl.rcParams["xtick.major.size"]=6
mpl.rcParams["xtick.labelsize"]="large"
mpl.rcParams["ytick.labelsize"]="large"
mpl.rcParams["ytick.major.size"]=6
mpl.rcParams["grid.alpha"] = 0.5
mpl.rcParams["axes.grid"] = True
mpl.rcParams["savefig.dpi"] = 1000
mpl.rcParams["savefig.bbox"] = "tight"

hristics = ["Fixed Selector", "Most Constrained Variable"]

def valid(sequence):  # checks if sequence is valid or not
    if len(sequence) != 81:
    	return False
    validity = [str(i) for i in range(10)]
    for i in sequence:
    	if i not in validity:
    		return False
    return True

problemSet = []
problemComments = []
datafile = op.join(thispath, "TESTCASES.txt")

def getFile(f=datafile):

    with open(f, 'r') as f:
    	lines = [line.strip() for line in f]

    problem = ""
    for i, line in enumerate(lines):
    	if i % 11 == 0:
    		problemComments.append(line)
    	elif i % 11 == 10:
    		if not valid(problem):
    			raise ValueError("Invalid board sequence.")
    		problemSet.append(problem)
    		problem = ""
    	else:
    		problem += ''.join(line.split())

    return problemSet, problemComments

def getDifficulty(prob, comm):

    diffdict = {'easy': [[],[]], 'medium': [[],[]], 'hard': [[],[]], 'evil': [[],[]]}
    sudoku = Solver.Solver(1, 2)
    cnt = 0
    for problem, comment in zip(prob,comm):
    
        fstr = re.search('[a-zA-Z][a-zA-Z]', comment)
        fstr = fstr.group(0).lower()

        initFill = sudoku.start(problem)
        for k in diffdict.keys():
    	    if k.startswith(fstr):
                diffdict[k][0].append(cnt)
                diffdict[k][1].append(initFill)
                continue
        cnt += 1

    return diffdict


def runall(ht, su, prob=[], comm=[], f=datafile):

    
    if not prob:
        prob, comm = getFile(f)

    nBacktracks = []
    nRuleNakedK = []

    times = []

    sudoku = Solver.Solver(ht, su)
    for problem, comment in zip(prob, comm):
#        print("--------------------------------------------------")
#        print("--------------------------------------------------")
#        print("Running: " + comment)

        fstr = re.search('[a-zA-Z][a-zA-Z]', comment)

        sudoku.start(problem)
        # print("\nStarting board:")
#        # sudoku.printBoard()
#
#        print("solving....")
        success, nBackTrack, nStrategy, time = sudoku.solve()

        if not success:
            print("Whoa! Problem " + fstr + " FAILED: ")
            inp = int(input("What should we do. Press 1 to abort, 0 to continue: "))
            if inp:
                print("Abobo! ")
                sys.exit(-1)

        #IsSucc.append(int(success))

        # print("\nFinal board:")
        # sudoku.printFullBoard()

#        print("Time: \t\t\t\t ", time)
#        print("Num backtrackings: \t\t ", nBackTrack)
#        for i, n in enumerate(nStrategy):
#            print("Num Strategy Level: \t", i+1, n)

        
        nRuleNakedK.append(tuple(nStrategy))
        times.append(time)
        nBacktracks.append(nBackTrack)

    return array(nBacktracks), array(nRuleNakedK).T, array(times)


if __name__ == "__main__":

    prob, comm = getFile()

    #Returns dict
    difficulty = getDifficulty(prob, comm)
    dfill = {k: mean(i[1]) for k, i in difficulty.items()}
    diffidx = {k: array(i[0]) for k, i in difficulty.items()}

    print("Average filled-in num:")
    [print(k, i) for k, i in dfill.items()]        
    diffic = ['easy', 'medium', 'hard', 'evil']

    lsys = len(sys.argv)

    if lsys < 2:
        heuristic = (0, 1)
        strat = tuple(range(4))
        hstrat = [(h,s) for h in heuristic for s in strat]
    else:
        if lsys > 4 or lsys == 2:
            print("Give both heuristic and strategy level and no more. ")
            sys.exit(-1)
        heuristic = bool(int(sys.argv[2])-1)
        hstrat = [tuple(heuristic, int(sys.argv[3]))]

    fullMean = {}
    fullStd = {}
    abc = []
    coll = {}

    for hs in hstrat:
        heuristic, strategy = hs
        hkey = hristics[heuristic]
        if hkey not in fullMean.keys():
            fullMean[hkey] = []
            fullStd[hkey] = []

        nBack, nNaked, timing = runall(heuristic, strategy, prob, comm) 
        metrics = ["time", "backtrack", "strategy"]
        dc = collections.defaultdict(dict)
        dcsum = collections.defaultdict(dict)
        dcstd = collections.defaultdict(dict)
        for k, d in diffidx.items():
            dc[k]['time'] = timing[d]
            dc[k]['backtrack'] = nBack[d]
            dc[k]['strategy'] = nNaked[:, d]

        for k, d in dc.items():
            print("----------------")
            print("Problem Type: " + k)
            for k1, d1 in d.items():
                results = mean(d1.T, axis=0)
                rstd = std(d1.T, axis=0)
                abc.append((results, rstd))
                print("Average " + k1 + ":  " + str(results))
                dcsum[k][k1] = results
                dcstd[k][k1] = rstd


        print("----------------")
        fullMean[hkey].append(dcsum)
        fullStd[hkey].append(dcstd)
        if strategy == 3:
            coll[hkey] = dc
        

    for k, d in fullMean.items():
        print("----------------")
        print("----------------")
        print("Run Type: ", k)
        for ii, dsubs in enumerate(d):
            print("Inference Rules: ", ii)
            for k1, d1 in dsubs.items():
                print("Difficulty: ", k1)
                for k2, d2 in d1.items():
                    print("Metric " + k2 + " | Result : " + str(d2))

            print("----------------")

#%% Plots          
    plott = 1

    if plott:
        ftime, atime = plt.subplots(1,2, sharey=True)
        fback, aback = plt.subplots(1,2, sharey=True)
        ftime.suptitle("Runtime Performance")
        fback.suptitle("Backtracks")

        axi = 0
        drange = list(range(4))
        wid = 0.2
        ttot = []
        btot = []
        for k, d in fullMean.items():
            rct = []
            rcb = []
            for ii, dsubs in enumerate(d):
                ti = []
                bi = []
                ts = []
                bs = []
                label = []
                dr = [d + (ii-2)*wid for d in drange]
                #drn = [[xstrt[xi] + d + ii*wid/2 for d in drange] for xi in range(len(dsubs))]
                for k1, do in dsubs.items():
                    ti.append(do['time'])
                    bi.append(do['backtrack'])
                    ts.append(fullStd[k][ii][k1]['time']/4)
                    bs.append(fullStd[k][ii][k1]['backtrack']/10)
                    label.append(k1)
                    
                ttot.extend(ti)
                btot.extend(bi)
                print(ti)
                rt = atime[axi].bar(dr, ti, wid, yerr=ts)
                rct.append(rt)
                rb = aback[axi].bar(dr, bi, wid, yerr=bs)
                rcb.append(rb)
            
            
            atime[axi].set_title(k)
            aback[axi].set_title(k)
            atime[axi].set_xticks(drange)
            aback[axi].set_xticks(drange)
            atime[axi].set_xticklabels(label)
            aback[axi].set_xticklabels(label)
            if not axi:
                atime[axi].set_ylabel('Average runtime (s)')
                aback[axi].set_ylabel('Average backtracks per puzzle')
                legtime = atime[axi].legend([r[0] for r in rct], (drange))
                legback = aback[axi].legend([r[0] for r in rcb], (drange))
                legtime.set_title('Inference Level')
                legback.set_title('Inference Level')
                
            atime[axi].set_xlabel('Difficulty')
            aback[axi].set_xlabel('Difficulty')
            axi+=1

        ftime.savefig("TimePerform.pdf")
        fback.savefig("BackPerform.pdf")

    fc = plt.figure("Correlate")
    plt.scatter(btot, ttot)
    bX = sm.add_constant(btot)
    mdl = sm.OLS(ttot, bX)
    mdf = mdl.fit()
    pm = mdf.params
    ba = linspace(0, max(btot))
    plt.plot(ba, pm[1] * ba + pm[0], 'k')
    plt.xlabel("Average Runtime (s)")
    plt.xlabel("Average backtracks per puzzle")
    
    plt.show()
