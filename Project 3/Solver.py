from time import clock, time

def MostConstrainedVariable(variables):
	minLength = 10
	minSquare = ""
	for square in variables:
		length = len(variables[square])
		if length < minLength and length > 1:
			minSquare = square
			minLength = length
	return minSquare

def FixedVariable(variables):
	for s in variables: 
		if len(variables[s]) > 1:
			return s

class Solver:
	def __init__(self, MCVChoice=False, searchLevel=3): #default values 
		self.depth = searchLevel
		self.heuristic = MostConstrainedVariable if MCVChoice else FixedVariable
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
		self.numNS = [0] + [0 for k in range(1, self.depth)]
		self.solved = None

	def start(self, board):
		self.defaultVariables()
		nf = 0
		for i, value in enumerate(board):
			index = '' + self.rows[i//9] + self.cols[i%9]
			if value != "0":
				self.variables[index] = value
				nf += 1
		
		return nf

	def solve(self):
		if self.solved is not None:
			return self.solved

		startC = time()
		self.variables = self.backtrackSearch(self.variables)
		endC = time()

		return self.Solved(self.variables), self.numBacktrack, self.numNS, endC - startC
	
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
			if '' in variables.values():
				return False

			#This is just synonymous with constraint prop
			variables, changed = self.nakedSingle(variables, changed)

			if (self.depth > 0):
				variables, changed = self.hiddenSingle(variables, changed)

			for k in range(1, self.depth): 
				variables, changed = self.nakedK(k+1, variables, changed)
		
		return variables

	def nakedSingle(self, variables, changed):
		for square, values in variables.items():

			if len(values) == 1:
				for neighbor in self.neighbors[square]:
					if values in variables[neighbor]:
						variables[neighbor] = variables[neighbor].replace(values,'')
						if len(variables[neighbor]) == 1:
							self.numNS[0] += 1

						changed = True

		return variables, changed


	def hiddenSingle(self, variables, changed):
		for square, candidates in variables.items():
			if len(candidates) > 1:
				for value in candidates:
					found = False
					for neighbor in self.neighbors[square]:
						if value in variables[neighbor]:
							found = True
							break
					if not found:
						variables[square] = value
						self.numNS[0] += 1
						changed = True
						break

		return variables, changed

	def nakedK(self, K, variables, changed):
		if K > 10:
			print("K= ", K)
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
							self.numNS[K-1] += 1

		return variables, changed

	def backtrackSearch(self, variables):
		if self.Solved(variables):
			return variables

		square = self.heuristic(variables)
		for value in variables[square]:
			newVar = variables.copy()
			newVar[square] = value
			newVar = self.constraintPropagation(newVar)

			if newVar:
				result = self.backtrackSearch(newVar)
				if result:
					return result

		self.numBacktrack += 1
		return False

	
	
	
