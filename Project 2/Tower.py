'''
    The Tower itself
'''

from searchQ import *

def pathmove(t, mov):
    p = list(t[:])
    sh = t[mov[0]][-1]
    p[mov[1]] = t[mov[1]] + [sh]
    p[mov[0]] = t[mov[0]][:-1]
    return tuple(p)

class Tower(object):
    def __init__(self, tStart, beam=5):
        ti = [int(t) for t in tStart]
        self.nDisks = len(ti)
        self.tower = (ti, [], [])
        self.name = "Generic"
        self.lastmov = -1
        self.acts = [(i,j) for i in range(3) for j in range(3) if not i ==j]
        self.goal = sorted(ti, reverse=True)
        if beam < 2:
            self.pq = Astar(self.tower)
            self.alg = "Astar"
        else:
            self.pq = beamQueue(self.tower, beam)
            self.alg = "Beam"+str(beam)    
            
        self.depth = 0
        self.nodeCount = 0
        
    def goalTest(self, newTower):
        if newTower == self.goal:
            return True
        else:
            return False

    def printPath(self, towers):
        printAll = ""
        for t in towers:
            q = " | - "
            h1 = " ----------- " + self.name + " ----------- "
            h2 = " | -- 0 -- | -- 1 -- | -- 2 -- |"
            h3 = "---------------------------------"
            tw = [len(k) for k in self.tower]
            mx = max(tw)
            bigsn = h1 + "\n" + h2 + "\n" + h3 + "\n"
            for k in range(mx):
                sn = q[:]
                for t in self.tower:
                    if len(t) <= k:
                        sn += " x-- " + q
                    else:
                        sn += str(t[k]) + " " + "-"*(3-t[k]//10) + q

                bigsn += sn[:-3] + "\n"
            
            printAll += bigsn + "\n"

        return printAll
    
    def __str__(self):
        return self.printPath([self.tower])
    

if __name__ == "__main__":
    testStr = listStr(list(range(15)))
    tow = Tower(testStr, 1)
    print(tow)


