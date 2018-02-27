# Tower of Corvallis

## REQUIRES PYTHON 3.3 or greater

towerMain.py - runs full test

Corvallis.py - holds main subclass for this problem.  Will run a single simulation if run on it's own with no command line arguments. To change run details, edit testStr variable in source.

Class Corvallis takes initial condition, beam width (1 = Astar),  and admissible (default = True).

To run class Corvallis, call .takeTurn in a loop until it returns a list.  This list is the solution path.

Corvallis is currently set to run a tower with beam search, width
