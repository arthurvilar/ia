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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    """

    stack = util.Stack()    # pilha para o backtracking
    start = problem.getStartState() # estado inicial do pacman
    visited = set()         # nós visitados
    stack.push((start, 0, []))      # coloca o estado, custo e caminho na pilha

    while not stack.isEmpty():
        currState, cost, path = stack.pop()

        # se o nó é a resposta
        if problem.isGoalState(currState):
            return path

        # se o nó ainda não foi visitado
        if currState not in visited:
            visited.add(currState)  # marca o nó como visitado
            
            # empilha o sucessor do nó atual na pilha
            for new_state, new_action, new_cost in problem.getSuccessors(currState):
                stack.push((new_state, new_cost + cost, path + [new_action]))

    return path


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """

    queue = util.Queue()    # fila para o backtracking
    start = problem.getStartState() # estado inicial do pacman
    visited = set()         # nós visitados
    queue.push((start, 0, []))      # coloca o estado, custo e caminho na fila

    while not queue.isEmpty():
        currState, cost, path = queue.pop()

        # se o nó é a resposta
        if problem.isGoalState(currState):
            return path

        # se o nó ainda não foi visitado
        if currState not in visited:
            visited.add(currState)  # marca o nó como visitado
            
            # coloca o sucessor do nó atual na fila
            for new_state, new_action, new_cost in problem.getSuccessors(currState):
                queue.push((new_state, new_cost + cost, path + [new_action]))

    return path


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""

    queue = util.PriorityQueue()    # fila para o backtracking
    start = problem.getStartState() # estado inicial do pacman
    visited = set()         # nós visitados
    queue.push((start, 0, []), 0)      # coloca o estado, custo e caminho na fila

    while not queue.isEmpty():
        currState, currCost, currPath = queue.pop()

        # se o nó é a resposta
        if problem.isGoalState(currState):
            return currPath

        # se o nó ainda não foi visitado
        if currState not in visited:
            visited.add(currState)  # marca o nó como visitado
            
            # coloca o sucessor do nó atual na fila
            for new_state, new_action, new_cost in problem.getSuccessors(currState):
                cost = new_cost + currCost
                queue.push((new_state, cost, currPath + [new_action]), cost)

    return currPath
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    queue = util.PriorityQueue()    # fila para o backtracking
    start = problem.getStartState() # estado inicial do pacman
    visited = []         # nós visitados
    queue.push((start, 0, []), heuristic(start, problem))      # coloca o estado, custo e caminho na fila

    while not queue.isEmpty():
        currState, currCost, currPath = queue.pop()

        # se o nó é a resposta
        if problem.isGoalState(currState):
            return currPath

        # se o nó ainda não foi visitado
        if currState not in visited:
            visited.append(currState)  # marca o nó como visitado
            
            # coloca o sucessor do nó atual na fila
            for new_state, new_action, new_cost in problem.getSuccessors(currState):
                gCost = new_cost + currCost             # g(n) - custo do inicio até atual
                hCost = heuristic(new_state, problem)   # h(n) - custo do atual até final
                fCost = gCost + hCost                   # f(n) - custo da solução 
                queue.push((new_state, gCost, currPath + [new_action]), fCost)

    return currPath 


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
