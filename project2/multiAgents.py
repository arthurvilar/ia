# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import sys

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # distancia da comida mais perto
        newFood = newFood.asList()
        if newFood:
            aux = []
            for food in newFood:
                aux.append(manhattanDistance(newPos, food))
            score = min(aux)
        else:
            score = 1

        return successorGameState.getScore() + 1/score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        "*** YOUR CODE HERE ***"
        max_value, next_action = self.minimaxDecision(gameState, 0, self.depth)
        return next_action

    def minimaxDecision(self, gameState, agentIndex, depth):

        # coloca os scores nas folhas da arvore
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # se agente for pacman usa maxValue, se for fantasma usa minValue
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.minValue(gameState, agentIndex, depth)

    def minValue(self, gameState, agentIndex, depth):

        minScore = float("inf")
        minAction = None

        # se o agente for o último fantasma, o prox agente é o pacman
        # se não o prox agente é o prox fantasma
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth

        # acha a melhor opção entre todas as ações possíveis
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            newScore, newAction = self.minimaxDecision(successorGameState, nextAgent, nextDepth)

            if newScore < minScore:
                minScore = newScore
                minAction = action

        return minScore, minAction

    def maxValue(self, gameState, agentIndex, depth):

        maxScore = float("-inf")
        maxAction = None

        # se o agente for o último fantasma, o prox agente é o pacman
        # se não o prox agente é o prox fantasma
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth

        # acha a melhor opção entre todas as ações possíveis
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            newScore, newAction = self.minimaxDecision(successorGameState, nextAgent, nextDepth)

            if newScore > maxScore:
                maxScore = newScore
                maxAction = action

        return maxScore, maxAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        "*** YOUR CODE HERE ***"

        max_value, next_action = self.alphaBetaDecision(gameState, 0, self.depth, float("-inf"), float("inf"))
        return next_action

    def alphaBetaDecision(self, gameState, agentIndex, depth, alpha, beta):

        # coloca os scores nas folhas da arvore
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # se agente for pacman usa alphaValue, se for fantasma usa betaValue
        if agentIndex == 0:
            return self.alphaValue(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.betaValue(gameState, agentIndex, depth, alpha, beta)

    def alphaValue(self, gameState, agentIndex, depth, alpha, beta):

        maxScore = float("-inf")
        maxAction = None

        # se o agente for o último fantasma, o prox agente é o pacman
        # se não o prox agente é o prox fantasma
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth

        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            newScore, aux = self.alphaBetaDecision(successorGameState, nextAgent, nextDepth, alpha, beta)

            if newScore > maxScore:
                maxScore = newScore
                maxAction = action

            if newScore > beta:
                return newScore, action

            alpha = max(alpha, maxScore)

        return maxScore, maxAction

    def betaValue(self, gameState, agentIndex, depth, alpha, beta):

        minScore = float("inf")
        minAction = None

        # se o agente for o último fantasma, o prox agente é o pacman
        # se não o prox agente é o prox fantasma
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth

        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            newScore, aux = self.alphaBetaDecision(successorGameState, nextAgent, nextDepth, alpha, beta)

            if newScore < minScore:
                minScore = newScore
                minAction = action
            
            if newScore < alpha:
                return newScore, action
            
            beta = min(beta, minScore)

        return minScore, minAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        max_value, next_action = self.expectimaxDecision(gameState, 0, self.depth)
        return next_action

    def expectimaxDecision(self, gameState, agentIndex, depth):

        # coloca os scores nas folhas da arvore
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # se agente for pacman usa maxValue, se for fantasma usa expectationValue
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.expectationValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):

        maxScore = float("-inf")
        maxAction = None

        # se o agente for o último fantasma, o prox agente é o pacman
        # se não o prox agente é o prox fantasma
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth

        # acha a melhor opção entre todas as ações possíveis
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            newScore, newAction = self.expectimaxDecision(successorGameState, nextAgent, nextDepth)

            if newScore > maxScore:
                maxScore = newScore
                maxAction = action

        return maxScore, maxAction

    def expectationValue(self, gameState, agentIndex, depth):

        score = 0
        action = None
        actions = gameState.getLegalActions(agentIndex)

        # se o agente for o último fantasma, o prox agente é o pacman
        # se não o prox agente é o prox fantasma
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth

        # acha a melhor opção entre todas as ações possíveis
        for action in actions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            newScore, newAction = self.expectimaxDecision(successorGameState, nextAgent, nextDepth)
            score += newScore

        score = score/len(actions)

        return score, action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    pacManState = currentGameState.getPacmanState()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    scaredTime = min(newScaredTimes)

    # distancia do fantasma mais perto
    aux = []
    for ghostState in newGhostStates:
        aux.append(manhattanDistance(newPos, ghostState.getPosition()))
    closestGhostDistance = min(aux)

    # distancia da comida mais perto
    newFood = newFood.asList()
    if newFood:
        aux = []
        for food in newFood:
            aux.append(manhattanDistance(newPos, food))
        closestFoodDistance = min(aux)
    else:
        return 0
        
    # quanto mais perto do fantasma, menor o score (a nao ser que o fantama esteja comestivel)
    if scaredTime == 0:
        ghostScore = -4 / (closestGhostDistance + 1)  
    else:
        ghostScore = 1 / (closestGhostDistance + 1)

    # quanto mais comida sobrando, menor o score
    remainingFoodScore = -len(newFood)
    
    # quanto mais longe da comida, menor o score
    foodScore = 2 / (closestFoodDistance + 1)
    
    # Power pellets are good, but not that good
    powerScore = scaredTime * 0.5

    directionScore = 0
    if pacManState.getDirection() == "Stop":
        directionScore = -0.5
    else:
        directionScore = 1

    #gameScore = currentGameState.getScore() 

    return remainingFoodScore + ghostScore + foodScore + powerScore + directionScore

# Abbreviation
better = betterEvaluationFunction
