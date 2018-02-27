class vacuum_cleaning_agent:
    NORTH    = 0
    EAST     = 1
    SOUTH    = 2
    WEST     = 3

    FORWARD  = 1
    RIGHT    = 2
    LEFT     = 3
    SUCK     = 4
    OFF      = 5

    

    def Move(self, percept):
        [wall, dirt, home] = percept
        raise NotImplementedError("Extend functionality of the class")
