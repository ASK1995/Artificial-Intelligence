from vacuum_cleaning_agent import *

class MemoryModel(vacuum_cleaning_agent):
	state = 0

	def __init__(self):
		self.state = 0
		self.title = "Remembering"
	
	def Move(self, percept):
		[wall, dirt, home] = percept
		if self.state == 0 and dirt == 1:
			return vacuum_cleaning_agent.SUCK
		if self.state == 0 and wall == 0:
			return vacuum_cleaning_agent.FORWARD
		if self.state == 0 and wall == 1:
			self.state = 1
			return vacuum_cleaning_agent.RIGHT
		if self.state == 1 and wall == 1:
			self.state = 6
			return vacuum_cleaning_agent.RIGHT 
		if self.state == 1 and wall == 0:
			self.state = 2
			return vacuum_cleaning_agent.FORWARD
		if self.state == 2:
			self.state = 3
			return vacuum_cleaning_agent.RIGHT
		if self.state == 3 and dirt == 1:
			return vacuum_cleaning_agent.SUCK
		if self.state == 3 and wall == 0:
			return vacuum_cleaning_agent.FORWARD
		if self.state == 3 and wall == 1:
			self.state = 4
			return vacuum_cleaning_agent.LEFT
		if self.state == 4 and wall == 1:
			self.state = 6
			return vacuum_cleaning_agent.RIGHT
		if self.state == 4 and wall == 0:
			self.state = 5
			return vacuum_cleaning_agent.FORWARD
		if self.state == 5:
			self.state = 0
			return vacuum_cleaning_agent.LEFT
		if self.state == 6 and home == 1:
			return vacuum_cleaning_agent.OFF
		if self.state == 6 and wall == 0:
			return vacuum_cleaning_agent.FORWARD
		if self.state == 6 and wall == 1:
			return vacuum_cleaning_agent.RIGHT
		raise NotImplementedError("State change not possible.")

