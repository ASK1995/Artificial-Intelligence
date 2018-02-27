import Solver
import sys
import re

from time import clock, time
from numpy import *

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

if hasattr(__builtins__, 'raw_input'): input = raw_input

def valid(sequence):               #checks if sequence is valid or not
	if len(sequence) != 81:
		return False
	validity = [str(i) for i in range(10)] 
	for i in sequence:
		if i not in validity:
			return False
	return True

problemSet = []
problemComments = []

if sys.argv[1] == "-f":
	with open(sys.argv[2], 'r') as f:
		lines = [line.strip() for line in f]

	problem = ""
	for i, line in enumerate(lines):
		if i % 11 == 0:
			problemComments.append(line)
		elif i % 11 == 10:
			if not valid(problem):
				raise ValueError("Invalid board sequence.")
			problemSet.append(problem)
			problem = ""
		else:
			problem += ''.join(line.split())
	
	temp1 = int(input("1:noSearch-True , 2:noSearch-False: "))
	noSearch=True if temp1==1 else False
	temp2 = int(input("1:Random-True , 2:Random-False: "))
	RandomUnassignedVariable=True if temp2==1 else False
	temp3 = int(input("1:ruleTwo-True , 2:ruletwo-False: "))
	RuleTwo=True if temp3==1 else False
	strategyused=input('Naked Strategy in strings eg"23" for both naked doubles and naked triples: ')  
	NakedStrategy=[int(x) for x in set(strategyused)] 
	noSearch = False
	RandomUnassignedVariable = False
	RuleTwo = True
	
nBacktracks = []
nRuleOnes = []
nRuleTwos = []
nRuleNakedK = [[],[]]

easy = []
medium = []
hard = []
evil = []

IsSucc = []

nFilled = []

sudoku = Solver.Solver(noSearch, RandomUnassignedVariable, RuleTwo, NakedStrategy)
for problem, comment in zip(problemSet, problemComments):
	print("--------------------------------------------------")
   	print("Running: " + comment)

        fstr = re.search('[a-zA-Z][a-zA-Z]', comment)
        fstr = fstr.group(0)

    	if fstr == 'ea' or fstr == 'Ea':
        	easy.append(1.0)
        	medium.append(0.0)
        	hard.append(0.0)
        	evil.append(0.0)
        elif fstr == 'me' or fstr == 'Me':
        	easy.append(0.0)
        	medium.append(1.0)
        	hard.append(0.0)
        	evil.append(0.0)
    	elif fstr == 'ha' or fstr == 'Ha':
        	easy.append(0.0)
        	medium.append(0.0)
        	hard.append(1.0)
        	evil.append(0.0)
    	elif fstr == 'ev' or fstr == 'Ev':
        	easy.append(0.0)
        	medium.append(0.0)
        	hard.append(0.0)
        	evil.append(1.0)
    	else:
            	print fstr
        	easy.append(0.0)
        	medium.append(0.0)
        	hard.append(0.0)
        	evil.append(0.0)
	
	
	sudoku.start(problem)
	print("\nStarting board:")
	sudoku.printBoard()

	print("solving....",
	(success, numBacktracking, numRuleOne, numRuleTwo, numNakedStrategy, numFilled, time) = sudoku.solve()
    	IsSucc.append(int(success)))

	
	print("solution exists" if success else "No solution exists")
	print("\nFinal board:")
	sudoku.printFullBoard()

	print("Time: \t\t\t\t", time)
	print("Initially filled: \t\t", numFilled)
	print("Num backtrackings: \t\t", numBacktracking)
	print("Num Rule One's: \t\t", numRuleOne)
	if RuleTwo is True:
		print("Num Rule Two's: \t\t", numRuleTwo)
	for i,k in enumerate(numNakedStrategy):
		print("Num Rule Three's ( K =", k, "):\t", numNakedStrategy[k]
        	nRuleNakedK[i].append(numNakedStrategy[k]))

    	nBacktracks.append(numBacktracking)
    	nRuleOnes.append(numRuleOne)
    	nRuleTwos.append(numRuleTwo)
    	nFilled.append(numFilled)


easy = array(easy)
medium = array(medium)
hard = array(hard)
evil = array(evil)
IsSucc = array(IsSucc)

fill = array(nFilled)
r1 = array(nRuleOnes)
r2 = array(nRuleTwos)
n2 = array(nRuleNakedK[0]) if len(nRuleNakedK[0]) > 0 else array([0]*len(nRuleOnes))
n3 = array(nRuleNakedK[1]) if len(nRuleNakedK[1]) > 0 else array([0]*len(nRuleOnes))
bt = array(nBacktracks)

print("easy solved: %d / %d" % (dot(easy,IsSucc), sum(easy)))
print("medium solved: %d / %d" % (dot(medium,IsSucc), sum(medium)))
print("hard solved: %d / %d" % (dot(hard,IsSucc), sum(hard)))
print("evil solved: %d / %d" % (dot(evil,IsSucc), sum(evil)))

print("Average filled-in num: easy:%f, medium:%f, hard:%f, evil:%f" % (dot(fill,easy)/sum(easy), dot(fill,medium)/sum(medium), dot(fill,hard)/sum(hard), dot(fill,evil)/sum(evil)))

print("Average r1 num: easy:%f, medium:%f, hard:%f, evil:%f" % (dot(r1,easy)/sum(easy), dot(r1,medium)/sum(medium), dot(r1,hard)/sum(hard), dot(r1,evil)/sum(evil)))
print("Average r2 num: easy:%f, medium:%f, hard:%f, evil:%f" % (dot(r2,easy)/sum(easy), dot(r2,medium)/sum(medium), dot(r2,hard)/sum(hard), dot(r2,evil)/sum(evil)))
print("Average n2 num: easy:%f, medium:%f, hard:%f, evil:%f" % (dot(n2,easy)/sum(easy), dot(n2,medium)/sum(medium), dot(n2,hard)/sum(hard), dot(n2,evil)/sum(evil)))
print("Average bt num: easy:%f, medium:%f, hard:%f, evil:%f" % (dot(bt,easy)/sum(easy), dot(bt,medium)/sum(medium), dot(bt,hard)/sum(hard), dot(bt,evil)/sum(evil)))
print("Average n3 num: easy:%f, medium:%f, hard:%f, evil:%f" % (dot(n3,easy)/sum(easy), dot(n3,medium)/sum(medium), dot(n3,hard)/sum(hard), dot(n3,evil)/sum(evil)))

#plot = 0
plot = 1
if plot:
        plt.figure(101)
        plt.plot(range(len(nRuleOnes)), nRuleOnes, 'b.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        plt.ylabel("number of rule one's")
        plt.xlabel('game No.')
        plt.title('statistics of rule one')


        plt.figure(102)
        plt.plot(range(len(nRuleTwos)), nRuleTwos, 'g.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        plt.ylabel("number of rule two's")
        plt.xlabel('game No.')
        plt.title('statistics of rule two')


        for s in NakedStrategy:
        	if s == 2:
        		plt.figure(103)
        		plt.plot(range(len(nRuleNakedK[0])), nRuleNakedK[0], 'r.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        		plt.ylabel("number of naked doubles")
        		plt.xlabel('game No.')
                	plt.title('statistics of naked double')

        	if s == 3:
                	if len(NakedStrategy) > 1:
        			ns = nRuleNakedK[1]
                	else:
                    		ns = nRuleNakedK[0]
        		plt.figure(104)
        		plt.plot(range(len(ns)), ns, 'r.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        		plt.ylabel("number of naked triples")
        		plt.xlabel('game No.')
                	plt.title('statistics of naked triple')


        plt.figure(105)
        plt.plot(range(len(nBacktracks)), nBacktracks, 'y.', linewidth = 6.0, solid_capstyle = 'round', label = 'most constrained slot')
        plt.ylabel("number of backtrackings")
        plt.xlabel('game No.')
        plt.title('statistics of backtracking')

if 0:
        RandomUnassignedVariable = True

        nBacktracks = []
        nRuleOnes = []
        nRuleTwos = []
        nRuleNakedK = [[],[]]

        sudoku = Solver.Solver(noSearch, RandomUnassignedVariable, RuleTwo, NakedStrategy)
        for problem, comment in zip(problemSet, problemComments):
        	print "--------------------------------------------------"
        	print "Running: " + comment
		
		sudoku.start(problem)
		print "\nInitial board:"
        	sudoku.printBoard()

		print "solving....",
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
		for i,k in enumerate(numNakedStrategy):
			print "Num Rule Three's ( K =", k, "):\t", numNakedStrategy[k]
        		nRuleNakedK[i].append(numNakedStrategy[k])

    		nBacktracks.append(numBacktracking)
    		nRuleOnes.append(numRuleOne)
    		nRuleTwos.append(numRuleTwo)
    		
        import plt
        plt.figure(101)
        plt.plot(range(len(nRuleOnes)), nRuleOnes, 'bs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        plt.ylabel("number of rule one's")
        plt.xlabel('game No.')
        plt.title('statistics of rule one')


        plt.figure(102)
        plt.plot(range(len(nRuleTwos)), nRuleTwos, 'gs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        plt.ylabel("number of rule two's")
        plt.xlabel('game No.')
        plt.title('statistics of rule two')


        for s in NakedStrategy:
        	if s == 2:
        		plt.figure(103)
        		plt.plot(range(len(nRuleNakedK[0])), nRuleNakedK[0], 'rs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        		plt.ylabel("number of naked doubles")
        		plt.xlabel('game No.')
                	plt.title('statistics of naked double')

        	if s == 3:
                	if len(NakedStrategy) > 1:
        			ns = nRuleNakedK[1]
                	else:
                    		ns = nRuleNakedK[0]
        		plt.figure(104)
        		plt.plot(range(len(ns)), ns, 'rs', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        		plt.ylabel("number of naked triples")
        		plt.xlabel('game No.')
                	plt.title('statistics of naked triple')


        plt.figure(105)
        plt.plot(range(len(nBacktracks)), nBacktracks, 'ys', linewidth = 6.0, solid_capstyle = 'round', label = 'random slot')
        plt.ylabel("number of backtrackings")
        plt.xlabel('game No.')
        plt.title('statistics of backtracking')


if plot:
        plt.show()
