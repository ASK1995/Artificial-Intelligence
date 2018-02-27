"""

Santosh Kumar,Daniel Mageed


"""


from Tower import *
import time
import sys
import random

mean = lambda x: sum(x)/len(x)

class Corvallis(Tower):
    def __init__(self, initial, beam, admissible=True):
        super().__init__(initial, beam=beam)
        self.name="Corvallis"
        self.pow = 1 if admissible else 2
        if self.pow == 1:
            self.hName = "Admissible"
        else:
            self.hName = "Non-Admissible"

    def mDistAll(self, newTower):
        lz = len(newTower[0])
        hf=0
        for i in range(self.nDisks):
            disk = self.nDisks - (i+1)
            if lz <= i or disk != newTower[0][i]:
        
                hf = (disk+1)**self.pow
                break 

        hf += lz/self.nDisks
        return int(hf)

    #Takes the action on each node of the expanded parent.    
    def heuristic(self, newTower, lastmov):
        h = []
        for a in self.acts:
            if len(newTower[a[0]]) == 0  or a[0] == lastmov:
                continue
            
            moved = pathmove(newTower, a)
 
            if self.goalTest(moved[0]):
                return -1

            h.append((self.mDistAll(moved), self.depth, [newTower, moved]))
        
        return h

    def reconstructPath(self):
        
        pnow = tupler(self.tower)
        self.pg = pnow
        self.tower = (self.goal, [], [])
        tgoal = tupler(self.tower)
        path = [tgoal, pnow]     

        while pnow in self.pq.path.keys():
            pnow = self.pq.path[pnow]
            path.append(pnow)
            
            
        return path[:-1]

    def takeTurn(self):
        parents = self.pq.pop()
        self.jail = parents
        hg, lastm = parents[0]
        _, g, tow = hg
        self.depth = g+1
        self.tower = tow[-1]
        hNow = self.heuristic(tow[-1], lastm)
        if hNow == -1:
            self.nodeCount += 1
            return self.reconstructPath()
            
        for i, p in enumerate(parents[1:]):
            hg, lastm = p
            _, _, tow = hg
            _, newT = tow
            hN = self.heuristic(newT, lastm)
            if hN == -1:
                self.tower = newT
                self.nodeCount += (i+1)
                return self.reconstructPath()

            hNow.extend(hN)

        self.nodeCount += len(parents)
    
        self.pq.pushList(hNow)
    
        return len(parents)

def getargs(argvs):
    argvs.reverse()
    print(len(argvs))
    a = 50 if argvs == [] else int(argvs.pop())
    aa=list(range(a))
    random.shuffle(aa)
    b = 10 if argvs == [] else int(argvs.pop())
    c = True if argvs == [] else bool(argvs.pop())
    print(a,b,c)

    return aa, b, c



if __name__ == "__main__":
    testRun = getargs(sys.argv[1:])
    cVal = Corvallis(*testRun)
    print("INITIAL STATE:")
    print(cVal)
    cnt = 0
    goal = 0
    t = time.time()
    while not isinstance(goal, list) and cnt < 50000:
        goal = cVal.takeTurn()
        cnt += 1
        if not cnt % 500:
            print(cnt, tupler(cVal.tower)[0], cVal.depth)
            
    t2 = time.time()
    dt = t2-t
    print("--------------------------")
    print("Nodes Expanded: ", cVal.nodeCount) 
    print("Solution Depth:  ",cVal.depth)
    print("RunTime: ", dt)
    print("--------------------------")
    print("Final State: ")
    print(cVal)
    # print("PATH:")
    # print(goal)






        
            
