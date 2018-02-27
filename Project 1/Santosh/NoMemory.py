from vacuum_cleaning_agent import *

class NoMemory(vacuum_cleaning_agent):
    def __init__(self):
        self.title = "Forgetful"

    def Move(self, percept):
        dirt, wall, home = percept
        if dirt == 1:
            return self.SUCK
        if wall == 0 and home == 1:
            return self.FORWARD
        if wall == 1 and home == 0:
            return self.RIGHT
        if wall == 1 and home == 1:
            return self.OFF
        if wall == 0 and home == 0:
            return self.FORWARD

if __name__ == "__main__":
    mv = NoMemory()
    print(mv.title)