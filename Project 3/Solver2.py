from time import clock, time

class Solver:
	def __init__(self, noSearch = False, RandomUnassignedVariable = False, RuleTwo = False, NakedStrategy = [2, 3]): #default values 
		self.RuleTwo = RuleTwo
		self.NakedStrategy = NakedStrategy
		self.RandomUnassignedVariable = RandomUnassignedVariable
		self.noSearch = noSearch
		self.defaultVariables()

	def defaultVariables(self):
		self.rows = "123456789"
		self.cols = "abcdefghi"         #Giving different values to rows and columns to not get confused
		self.squares = [it + j for it in self.rows for j in self.cols]
		self.domain = "123456789"

		self.variables = dict((s, self.domain) for s in self.squares)
		#to ensure all different values in rows,columns,box(3*3)
		self.rowAlldiffs = [[it +j for it in self.rows for j in c] for c in self.cols]
		self.colAlldiffs = [[it +j for it in r for j in self.cols] for r in self.rows]
		self.boxAlldiffs = [[it +j for it in r for j in c] for r in ['123','456','789'] for c in ['abc','def','ghi']]
		self.alldiffs = (self.rowAlldiffs + self.colAlldiffs + self.boxAlldiffs)

		self.neighbors = dict((s, list(set(sum([i for i in self.alldiffs if s in i],[]))-set([s]))) for s in self.squares)
		#storing the values to be printed in the following variables for counting,checking if it is solved
		self.numBacktrack = 0
		self.numRuleOne = 0
		self.numRuleTwo = 0
		self.numNakedStrategy = dict((k, 0) for k in self.NakedStrategy) 
		self.numFilled = 0
		self.solved = None

	def start(self, board):
		self.defaultVariables()
		for i, value in enumerate(board):
			index = '' + self.rows[i//9] + self.cols[i%9]
			if value != "0":
				self.variables[index] = value
				self.numFilled += 1

	def solve(self):
		if self.solved is not None:
			return self.solved

		startC = time()
		if self.noSearch is True:
			self.variables = self.constraintPropagation(self.variables)
		else:
			self.variables = self.backtrackSearch(self.variables)
		endC = time()

		self.solved = [self.Solved(self.variables), self.numBacktrack, self.numRuleOne, self.numRuleTwo, self.numNakedStrategy, self.numFilled, endC - startC]
		return self.solved 
	
	def Solved(self, variables):
		for square in self.variables:
			if len(variables[square]) != 1:
				return False
		return True
	
	def printBoard(self, variables = None):
		if variables is None:
			variables = self.variables

		#print "  a b c   d e f   g h i"
		for r in self.rows:
			print(r, ''.join((variables[r+c] if len(variables[r+c]) == 1 else '-')+' '+('| ' if c in 'cf' else '') for c in self.cols))
			if r in '36':
				print(' ' + '-'*23)
                
	
	def printFullBoard(self, variables = None):
		if variables is None:
			variables = self.variables
		
		width = 1+max(len(variables[s]) for s in self.squares)
		print('  ' + ''.join(c.center(width)+('  ' if c in 'cf' else '') for c in "abcdefghi"))
		for r in self.rows:
			print(r, ''.join(variables[r+c].center(width)+('| ' if c in 'cf' else '') for c in self.cols))
			if r in '36':
				print(' ---' + '-'.join(['-'*(width*3)]*3))
		print

	def constraintPropagation(self, variables):
		changed = True
		while changed:
			changed = False

			if self.RuleTwo is True:
				(variables, changed) = self.ruleTwo(variables, changed)

			for k in self.NakedStrategy: 
				(variables, changed) = self.nakedK(k, variables, changed)

			for square in variables:
				values = variables[square]
				if len(values) == 0:
					return False

				elif len(values) == 1:
					for neighbor in self.neighbors[square]:
						if values in variables[neighbor]:
							variables[neighbor] = variables[neighbor].replace(values,'')
							if len(variables[neighbor]) == 1:
								self.numRuleOne = self.numRuleOne + 1
							changed = True
		return variables

	def ruleTwo(self, variables, changed):
		for square in variables:
			candidates = variables[square]
			if len(candidates) < 2:
				break
			for value in candidates:
				found = False
				for neighbor in self.neighbors[square]:
					if value in variables[neighbor]:
						found = True
						break
				if found is False:
					if value not in variables[square]:
						assert(False)
					variables[square] = value
					self.numRuleTwo =self.numRuleTwo + 1
					changed = True
					break
		return [variables, changed]

	def nakedK(self, K, variables, changed):
		if K not in range(1,10):
			raise ValueError("K must be between 1 and 9")

		for unit in self.alldiffs:
			for square in unit:
				foundSet = []
				if square not in foundSet and len(variables[square]) == K:
					nakedValues = set(variables[square])
					nakedSet = [square]
					for s in unit:
						if s != square and set(variables[s]).issubset(nakedValues):
							nakedSet.append(s)
					if len(nakedSet) == K:
						foundSet.extend(nakedSet)
						affected = False
						for s in unit:
							if s not in nakedSet:
								for value in nakedValues:
									oldLen = len(variables[s])
									variables[s] = variables[s].replace(value, '')
									if oldLen != len(variables[s]):
										changed = True
										affected = True
						if affected is True:
							self.numNakedStrategy[K] =self.numNakedStrategy[K] + 1
		return [variables, changed]

	def backtrackSearch(self, variables):
		if self.Solved(variables):
			return variables

		square = self.UnassignedVariable(variables)
		for value in self.orderDomainValues(square, variables):
			newVar = variables.copy()
			newVar[square] = value
			newVar = self.constraintPropagation(newVar)

			if newVar is not False:
				result = self.backtrackSearch(newVar)
				if result is not False:
					return result
		self.numBacktrack =self.numBacktrack + 1
		return False

	def UnassignedVariable(self, variables):
		if self.RandomUnassignedVariable is True:
			return self.RandomVariable(variables)
		else:	
			return self.MostConstrainedVariable(variables)

	def MostConstrainedVariable(self, variables):
		minLength = 10
		minSquare = ""
		for square in variables:
			length = len(variables[square])
			if length < minLength and length > 1:
				minSquare = square
				minLength = length
		return minSquare

	def RandomVariable(self, cells):
		squaresRemaining = [square for square in cells if len(cells[square]) > 1]
		return choice(squaresRemaining)

	def orderDomainValues(self, var, variables):
		return variables[var]
	
	
	
