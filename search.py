#################################################################################
#################################################################################
###             PROJETO DE INTRODUCAO A INTELIGENCIA ARTIFICIAL               ###
###                                                                           ###
###             ALUNO: MATHEUS ARRUDA AGUIAR. MATRICULA: 18/0127659           ###
#################################################################################
#################################################################################

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

    #Esta funcao coloca nos nao visitados na pilha. Os nos sao exibidos um a um

    pais = {}
    visitado = {}
    stack = util.Stack()                #Tupla (no na lista, direcao, custo)
    solucao = []                        #Eh o passo a passo de instrucoes que o Pacman deve fazer para chegar ao goal state

    inicio = problem.getStartState()

    stack.push((inicio, 'Undefined', 0))
    visitado[inicio] = 'Undefined'       

    if problem.isGoalState(inicio):
        return solucao                  #Se o estado inicial eh o goal

    goal = False;

    while (stack.isEmpty() != True and goal != True):

        no = stack.pop()
        visitado[no[0]] = no[1]

        if problem.isGoalState(no[0]):
            no_soluc = no[0]
            goal = True
            break

        for elem in problem.getSuccessors(no[0]): #Expande no

            if elem[0] not in visitado.keys():
                pais[elem[0]] = no[0]
                stack.push(elem)

    while (no_soluc in pais.keys()):             #Encontra e guarda o caminho
        no_soluc_prev = pais[no_soluc]

        solucao.insert(0, visitado[no_soluc])

        no_soluc = no_soluc_prev

    return solucao

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    noInicial = problem.getStartState()

    minhaFila = util.Queue()
    nosVisitados = []

    minhaFila.push((noInicial, []))

    if problem.isGoalState(noInicial):    #Se o no inicial eh o goal
        return []

    while not minhaFila.isEmpty():          
        noAtual, acoes = minhaFila.pop()
        if noAtual not in nosVisitados:
            nosVisitados.append(noAtual)

            if problem.isGoalState(noAtual): #Se for um no goal, o loop para e a retorna acao como solucao
                return acoes

            for proximoNo, acao, custos in problem.getSuccessors(noAtual): #Expande no
                novaAcao = acoes + [acao]
                minhaFila.push((proximoNo, novaAcao))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    #Esta funcao coloca os nos na fila de prioridade.

    noInicial = problem.getStartState()

    nosVisitados = []
    fila = util.PriorityQueue()

    fila.push((noInicial, [], 0), 0)    #Tupla: (no, acao No atual, custoPrev), prioridade)

    if problem.isGoalState(noInicial):
        return []

    while not fila.isEmpty():

        noAtual, acoes, custosPrev = fila.pop()
        if noAtual not in nosVisitados:
            nosVisitados.append(noAtual)

            if problem.isGoalState(noAtual):
                return acoes

            for proximoNo, acao, custos in problem.getSuccessors(noAtual): #Expande no
                novaAcao = acoes + [acao]
                priority = custosPrev + custos
                fila.push((proximoNo, novaAcao, priority),priority)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    noInicial = problem.getStartState()

    nosVisitados = []

    fila = util.PriorityQueue()         
    fila.push((noInicial, [], 0), 0)    #Tupla: (no, acao No atual, custoPrev), prioridade)

    if problem.isGoalState(noInicial):
        return []

    while not fila.isEmpty():

        noAtual, acoes, custosPrev = fila.pop()

        if noAtual not in nosVisitados:
            nosVisitados.append(noAtual)

            if problem.isGoalState(noAtual):
                return acoes
            
            #Expande no
            for proximoNo, acao, custos in problem.getSuccessors(noAtual):
                novaAcao = acoes + [acao]
                novoCustoNo = custosPrev + custos
                custoHeurist = novoCustoNo + heuristic(proximoNo,problem)
                fila.push((proximoNo, novaAcao, novoCustoNo),custoHeurist)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
