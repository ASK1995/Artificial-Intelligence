import Solver
import sys
from time import clock, time

import os
import os.path as op
import matplotlib as mpl
mpl.use("Agg") #This lets you plot (and save) if you run remotely.

import matplotlib.pyplot as plt
import pandas as pd
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

def valid(sequence):               #checks if sequence is valid or not
	if len(sequence) != 81:
		return False
	validity = [str(i) for i in range(10)] 
	for i in sequence:
		if i not in validity:
			return False
	return True

#This is useful to separate a program which can run a test or suite in it's own right from the function namespace that may accompany it.  It's like putting your c++ program in int main{} rather than global space.

if __name__ == "__main__":
	problemSet = []
	Comments = []

	sequence=input("Sudoku Sequence: ")
	if not valid(sequence):
		raise ValueError("Invalid sudoku sequence. ")
	problemSet.append(sequence)	
	Comments.append("start")	
	noSearch = False
	RandomUnassignedVariable = False
	RuleTwo = False
	NakedStrategy = []
	#above initialized variables for backtracking allow/not , randomness of choosing next cell allowed or not, Rule2(assign to cell if it's value not in domain of another cell) , naked doubles,triples,4 etc

	temp1 = int(input("1:noSearch-True , 2:noSearch-False "))
	noSearch=True if temp1==1 else False
	temp2 = int(input("1:Random-True , 2:Random-False "))
	RandomUnassignedVariable=True if temp2==1 else False
	temp3 = int(input("1:ruleTwo-True , 2:ruletwo-False "))
	RuleTwo=True if temp3==1 else False
	strategyused=input('Naked Strategy in strings eg"23" for both naked doubles and naked triples: ')  
	NakedStrategy=[int(x) for x in set(strategyused)] 


	sudoku = Solver.Solver(noSearch, RandomUnassignedVariable, RuleTwo, NakedStrategy)


for problem, comment in zip(problemSet, Comments):
	print 
	
	sudoku.start(problem)
	print("\nStarting board:")
	sudoku.printBoard()

	print("solving....")
	(success, numBacktracking, numRuleOne, numRuleTwo, numNakedStrategy, numFilled, time) = sudoku.solve()

	print "solution exists" if success else "No solution exists"
	print "\nFinal board:"
	sudoku.printFullBoard()

	print "Time: \t\t\t\t", time
	print "Initially filled: \t\t", numFilled
	print "Num backtrackings: \t\t", numBacktracking
	print "Num Rule One's: \t\t", numRuleOne
	if RuleTwo is True:
		print "Num Rule Two's: \t\t", numRuleTwo
	for k in numNakedStrategy:
		print "Num Rule Three's ( K =", k, "):\t", numNakedStrategy[k]
