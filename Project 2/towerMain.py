'''
    The Main Function
'''
import os
import os.path as op
import sys


from Corvallis import *
import matplotlib as mpl
mpl.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import time
import collections

thispath = op.abspath(op.dirname(__file__))
impath = op.join(thispath, "images")
datapath = op.join(thispath, "data")

mpl.rcParams['lines.linewidth'] = 3
#mpl.rcParams['lines.markersize'] = 8
mpl.rcParams["figure.figsize"] = 11,5
mpl.rcParams["figure.titlesize"]="x-large"
mpl.rcParams["figure.titleweight"]="bold"
mpl.rcParams["grid.alpha"] = 0.5
mpl.rcParams["axes.grid"] = True
mpl.rcParams["savefig.dpi"] = 1000
mpl.rcParams["savefig.bbox"] = "tight"

NMAX = 1e5

def getTests(path):
    data = [op.join(path, k) for k in os.listdir(path) if k.endswith('txt')]
    dfile = data[0]
    tests = []
    with open(dfile, "r") as f:
        for line in f:
            tests.append(line.strip())

    return tests

def dictify(tests):
    testDict = {}
    for t in tests:
        n = len(t)
        if n in testDict.keys():
            testDict[n].append(t)
        else:
            testDict[n] = [t]

    return testDict

def runTower(initState, beam=1, admit=True):
    cVal = Corvallis(initState, beam, admissible=admit)
    cnt = 0
    np = 50
    goal = 0
    t = time.time()
    while not isinstance(goal, list) and cnt < NMAX:
        cnt += goal
        goal = cVal.takeTurn()

    t2 = time.time()
    dt = t2-t
    print("Run State: ", cVal.hName, initState, cVal.alg, cVal.nodeCount, dt)
    return dt, cVal.nodeCount, cVal.depth, goal

def lastRun(inits):
    algo = {"Astar": 1, "Beam-5": 5}
    admit = ['admissible', 'non-admissible']
    for alg, nalg in algo.items():
        for a in admit:
            ab = (a == "admissible")
            pthfile = op.join(datapath, "pathz.csv")
            _, _, _, goals = runTower(inits, beam=nalg, admit=ab)
            with open(pthfile, "w") as pf:
                strw = alg+","+a+","+inits+","
                for step in i[::-1]:
                    strw += str(step) + "," 
                pf.write(strw+"\n")  

def beamTest(testDict, beams):
    
    admit = ['admissible', 'non-admissible'] 
    beamWidthTest = {'expanded': collections.defaultdict(dict),
                     'cputime (s)': collections.defaultdict(dict),
                     'depth': collections.defaultdict(dict)}

    for a in admit:
        for n, it in testDict.items():
            beamWidthTest['expanded'][a][n] = []
            beamWidthTest['depth'][a][n] = []
            beamWidthTest['cputime (s)'][a][n] = []
            for b in beams:
                ab = (a == "admissible")
                print(it[3], b, ab)
                tma, nca, dpa, pp = runTower(it[3], beam=b, admit=ab)
                print(it[-3], b, " || ", nca, dpa, tma)
                tmb, ncb, dpb, pp = runTower(it[-3], beam=b, admit=ab)
                
                beamWidthTest['expanded'][a][n].append((nca+ncb)/2)
                beamWidthTest['depth'][a][n].append((dpa+dpb)/2)
                beamWidthTest['cputime (s)'][a][n].append((tma+tmb)/2)

    return beamWidthTest


def beamTestSave(beamWidthTest, beams):
    for k, i in beamWidthTest.items():
        for kk, ii in i.items():
            ifr = pd.DataFrame.from_dict(ii)
            ifr.index=beams
            ifr.index.name = "BeamWidth"
            frpath = op.join(datapath, "Beam"+k.split(" ")[0].title()+kk.title()+".csv")
            ifr.to_csv(frpath)
        
    return True

def beamTestPlot(beamWidthTest, beams):
    for k, it in beamWidthTest.items():    
        f, axs = plt.subplots(1,2)
        axi = axs.ravel()    
        pdfpath = op.join(impath, "BeamTest"+k.split(" ")[0].title()+".pdf")
        for i, ky in enumerate(it.keys()):
            dfb = pd.DataFrame.from_dict(it[ky])
            dfb.index=beams
            dfb.index.name = "BeamWidth"
            dfb = dfb.T
            dfb.plot(ax=axi[i], grid=True)
            axi[i].set_title(ky)
            axi[i].set_xlabel("Number of Disks")
            axi[i].set_ylabel(k)
            hd, lb = axi[i].get_legend_handles_labels()
            axi[i].legend().remove()
            
        f.legend(hd, lb, 'upper right', title="Beam Width", fontsize='large')
        f.savefig(pdfpath)
        plt.close('all')

    return True

def sendPath(alg, a, pp):
    pthfile = op.join(datapath, alg.title()+a.title()+"path.csv")
    with open(pthfile, "w") as pf:
        strw = str(len(pp))
        for step in pp:
            strw += ","+str(step)
        pf.write(strw+"\n")    

def fullTester(testDict, beam):
    algo = {"Astar": 1, "Beam-10": beam}
    admit = ['admissible', 'non-admissible'] 

    fullTest = {'expanded': collections.defaultdict(dict),
                'cputime (s)': collections.defaultdict(dict),
                'depth': collections.defaultdict(dict)}

    for alg, nAlg in algo.items():
        for a in admit:            
            de = {}
            dd = {}
            dc = {}
            ab = (a == "admissible")
            for n, it in testDict.items():
                if n not in de.keys():
                    de[n] = []
                    dd[n] = []
                    dc[n] = []
                for itt in it:
                    tma, nca, dpa, pp = runTower(itt, beam=nAlg, admit=ab)
                    de[n].append(nca)
                    dd[n].append(dpa)
                    dc[n].append(tma)

            fullTest['expanded'][alg][a] = pd.DataFrame.from_dict(de)
            fullTest['depth'][alg][a]  = pd.DataFrame.from_dict(dd)
            fullTest['cputime (s)'][alg][a] = pd.DataFrame.from_dict(dc)

    return fullTest

def fullSave(fullTest):
    for k, it in fullTest.items():
        for ki, itt in it.items():
            for ix, ikey in enumerate(itt.keys()):
                csvpath = op.join(datapath, "Full" + k.title() + ki.title() + ikey.title() + ".csv")
                dfx = itt[ikey].T
                dfx.to_csv(csvpath)
                
def fullPlot(fullTest):
    for k, it in fullTest.items():
        for ki, itt in it.items():
            pdfpath = op.join(impath, "Full"+k.split(" ")[0].title()+ki.title()+".pdf")
         
            f, axs = plt.subplots(1,2)
            axi = axs.ravel()
            f.suptitle(ki)
            for ix, ikey in enumerate(itt.keys()):
                dfx = itt[ikey].T
                print(k, ki, ikey)
                print(dfx)
                ser = dfx.mean(axis=1)
                dfx.plot(ax=axi[ix], c='b', marker='.', markersize=15, linestyle='', legend=False, grid=True)
                
                ser.plot(ax=axi[ix], c='k', linewidth=3, grid=True, legend=False)
                
                axi[ix].set_xlim([3, 11])
                axi[ix].set_title(ikey)
                axi[ix].set_xlabel("Number of Disks")
                axi[ix].set_ylabel(k)
            
            f.savefig(pdfpath)
            plt.close('all')

    return True
    

if __name__ == "__main__":

    tests = getTests(datapath)

    testDict = dictify(tests)

    beams = list(range(5,26))[::5]
    beams.extend([50,100])

    bwt = beamTest(testDict, beams)
                
    # fp = beamTestSave(bwt, beams)
            
    fp = beamTestPlot(bwt, beams)

    print("BeamTestFinished")

    fullResult = fullTester(testDict, 10)

    # fb = fullSave(fullResult)
        
    fb = fullPlot(fullResult)
    

    # pthfile = op.join(datapath, "pathsfound.csv")
    # with open(pthfile, "a+") as pf:
    #     for k, i in goals.items():
    #         if len(k) == 10:
    #             strw = k+","
    #             for step in i[::-1]:
    #                 strw += str(step) + "," 
    #             pf.write(strw+"\n")
                    
            
                
            
#f.suptitle("Beam Search")
#for i, ky in enumerate(it.keys()):
#    dfb = pd.DataFrame.from_dict(it[ky])
#    dfb.index=beams
#    dfb.index.name = "BeamWidth"
#    dfb = dfb.T
#    pdfpath = op.join(impath, "BeamTest"+k+kk+".pdf")
#    pngpath = op.join(impath, "BeamTest"+k+kk+".png")
#    dfb.plot(ax=axi[i], grid=True)
#    axi[i].set_title(ky)
#    axi[i].set_xlabel("Number of Disks")
#    axi[i].set_ylabel(k)
#    hd, lb = axi[i].get_legend_handles_labels()
#    axi[i].legend().remove()
#    
#f.legend(hd, lb, 'upper right', title="Beam Width", fontsize='large')
#f.savefig(pdfpath)
#f.savefig(pngpath)
#plt.close('all')
#    for a in admit:
#        for t in tests:
#            ac, nc, dp, pp = runTower(t, 1, admit=bool(a))
#            print(t, ac, nc, dp)
#    
#            #frame.append(rslt)

    #fr = pd.DataFrame(frame)



