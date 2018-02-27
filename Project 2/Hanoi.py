
from Tower import *
import collections

#This is essentially the solution form 3 blue 1 Brown
def moveDisk(nDisk):
    pass #?


def hanoiSolve(nDisk):
    if nDisk == 0:
        return 
    
    hanoiSolve(nDisk-1)
    moveDisk(nDisk-1)
    hanoiSolve(nDisk-1)

class Hanoi(Tower):
    def __init__(self, tStart):
        n = len(tStart) if isinstance(tStart, collections.Iterable) else tStart
        self.tower = (list(range(n)), [], [])
        self.name = "Hanoi"



if __name__ == "__main__":
    hi = Hanoi(4)
    print(hi)


