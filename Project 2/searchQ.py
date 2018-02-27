'''
    The queues for searching
'''

import heapq

def listStr(lst):
    return "".join(map(str, lst))

def tupler(tow):
    return tuple([listStr(t) for t in tow])

def twoTowers(a, b):
    for k in range(len(a)):
        if len(b[k]) > len(a[k]):
            return k
        
    return -1

class queue(object):
    def __init__(self, tStart):
        self.q = [(-1, 0, [([0]*len(tStart[0]),[],[]), tStart])]
        self.path = dict()
        
    def setPath(self, qn):
        dad = qn[-1][0]
        kid = qn[-1][-1]
        dadS = tupler(dad)
        kidS = tupler(kid)
        self.path[kidS] = dadS #Pop expands a node so count when it happens.
        

class Astar(queue):
    def push(self, hTup):        
        for i, qs in enumerate(self.q):
            if hTup[-1][-1] == qs[-1][-1]:
                if hTup[0] >= qs[0]:
                    return

                self.q[i] = hTup
                self.q.sort()
                return
        
        heapq.heappush(self.q, hTup)

    def pushList(self, tList):
        for i in tList:
            if tupler(i[-1][-1]) in self.path.keys():
                continue

            self.push(i)

    def pop(self):
        p = heapq.heappop(self.q)
        self.setPath(p)
        return [(p, twoTowers(*p[-1]))]

class beamQueue(queue):
    def __init__(self, initial, beam):
        super().__init__(initial)
        self.B = beam

    def pushList(self, hTup):        
        self.q = [hTup[0]]
        for h in hTup[1:]:
            if tupler(h[-1][-1]) in self.path.keys():
                continue
            
            for ii, hh in enumerate(self.q):
                if h[-1][-1] == hh[-1][-1]:
                    if h[0] < hh[0]:
                        self.q[ii] = h
                        break

            self.q.append(h)

        heapq.heapify(self.q)
        self.q = heapq.nsmallest(self.B, self.q)
        
    def pop(self):
        pa = []
        while self.q:
            pg = heapq.heappop(self.q)
            self.setPath(pg)
            pa.append((pg, twoTowers(*pg[-1])))

        return pa