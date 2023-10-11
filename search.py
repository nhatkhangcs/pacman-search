# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack

    fringe = Stack()                # Fringe to manage which states to expand
    fringe.push(problem.getStartState())

    visited = []                    # List to check whether state has already been visited

    path=[]                         # Final direction list

    pathToCurrent=Stack()           # Stack to maintaing path from start to a state

    currState = fringe.pop()

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)

            for child, direction, cost in successors:
                fringe.push(child)
                tempPath = path + [direction]
                pathToCurrent.push(tempPath)

        currState = fringe.pop()
        path = pathToCurrent.pop()

    return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    fringe = Queue()                        # Fringe to manage which states to expand

    fringe.push(problem.getStartState())

    visited = []                            # List to check whether state has already been visited
    tempPath=[]                             # Temp variable to get intermediate paths
    path=[]                                 # List to store final sequence of directions 
    pathToCurrent=Queue()                   # Queue to store direction to children (currState and pathToCurrent go hand in hand)
    
    currState = fringe.pop()

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)    
            successors = problem.getSuccessors(currState)

            for child, direction, cost in successors:
                fringe.push(child)
                tempPath = path + [direction]
                pathToCurrent.push(tempPath)

        currState = fringe.pop()
        path = pathToCurrent.pop()
        
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import Queue,PriorityQueue
    fringe = PriorityQueue()                    # Fringe to manage which states to expand
    
    fringe.push(problem.getStartState(),0)
    visited = []                                # List to check whether state has already been visited
    tempPath=[]                                 # Temp variable to get intermediate paths
    path=[]                                     # List to store final sequence of directions 
    
    pathToCurrent=PriorityQueue()               # Queue to store direction to children (currState and pathToCurrent go hand in hand)
    currState = fringe.pop()
    
    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            
            for child, direction, cost in successors:
                tempPath = path + [direction]
                costToGo = problem.getCostOfActions(tempPath)
                
                if child not in visited:
                    fringe.push(child,costToGo)
                    pathToCurrent.push(tempPath,costToGo)
        
        currState = fringe.pop()
        path = pathToCurrent.pop()    
    
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

from util import PriorityQueue

class myNewQueue(PriorityQueue):

    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer
        self.problem = problem

    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem,item,heuristic))


# Calculate f(n) = g(n) + h(n) #
def f(problem,state,heuristic):
    return problem.getCostOfActions(state[1]) + heuristic(state[0],problem)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # queueXY: ((x,y),[path]) #
    queueXY = myNewQueue(problem,f)

    path = [] # Every state keeps it's path from the starting state
    visited = [] # Visited states

    if problem.isGoalState(problem.getStartState()):
        return []

    # Add initial state. Path is an empty list #
    element = (problem.getStartState(),[])

    queueXY.push(element,heuristic)

    while(True):

        # Terminate condition: can't find solution #
        if queueXY.isEmpty():
            return []

        # Get informations of current state #
        xy,path = queueXY.pop() # Take position and path
        if xy in visited:
            continue

        visited.append(xy)

        # Terminate condition: reach goal #
        if problem.isGoalState(xy):
            return path

        # Get successors of current state #
        succ = problem.getSuccessors(xy)

        # Add new states in queue and fix their path #
        if succ:
            for item in succ:
                if item[0] not in visited:

                    newPath = path + [item[1]] # Fix new path
                    element = (item[0],newPath)
                    queueXY.push(element,heuristic)

bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch