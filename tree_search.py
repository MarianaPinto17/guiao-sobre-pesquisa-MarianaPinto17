# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,depth,cost,heuristic): 
        self.state = state
        self.parent = parent
        #profundidade do nó
        self.depth = depth
        #custo de cada nó até à raiz
        self.cost=cost
        self.heuristic = heuristic

    # faz com que não haja ciclos -> se a ação seguinte for parent do nó corrente está a andar para trás
    # logo está a criar ciclos
    def in_parent(self,state):
        if self.state == state:
            return True
        if self.parent == None:
            return False
        return self.parent.in_parent(state)

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:
    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        self.depth = 0 #no root
        root = SearchNode(problem.initial, None,0,0, self.problem.domain.heuristic(problem.initial, problem.goal))
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 1
        self.non_terminals = 0

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)
    
    # comprimento solução sempre que um nó é percorrido
    @property
    def length(self):
        return self.solution.depth

    @property
    def cost(self):
        return self.solution.cost

    # factor de ramificação média é dado pelo ratio entre o número de nós filhos
    # (ou seja, todos os nós com excepção da raiz da árvore) e o número de nós pais (nós não
    # terminais)
    @property
    def avg_branching(self):
        return round((self.terminals + self.non_terminals-1)/self.non_terminals, 2)

    # procurar a solucao
    def search(self, limit = None):
        #enquanto a fila não está vazia
        while self.open_nodes != []:
            # remover cabeça da fila
            node = self.open_nodes.pop(0)
            #se o nó satisfaz o objetivo
            if self.problem.goal_test(node.state):
                self.terminals = len(self.open_nodes)+1
                self.solution = node 
                #retorna a solução -> o caminho
                return self.get_path(node)
            self.non_terminals += 1
            #lista dos novos nós que resultam da expansão dos nós que saíram da fila
            lnewnodes = []
            #spara cada ação possível executada no estado atual (node.state -> nó que saiu da fila)
            for a in self.problem.domain.actions(node.state):
                #calculamos o novo estado 
                newstate = self.problem.domain.result(node.state,a)
                #criar um novo nó que tem como pai o nó que estamos a expandir
                newnode = SearchNode(newstate,node, node.depth+1, node.cost + self.problem.domain.cost(node.state,a),self.problem.domain.heuristic(newstate, self.problem.goal))
                #se a ação seguinte não é parente do nó corrente e
                #se a profundidade do nó não ultrapassa o limite definido antes de adicionar a lista de nós abertos. (profundidade com limite)
                if not node.in_parent(newstate) and (limit is None or newnode.depth <= limit) :
                    #adicionar o novo nó à fila dos novos nós
                    lnewnodes.append(newnode)
            #acrescentar os novos nós à fila dos nós abertos
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.cost)
        #escolha o caminho que aproxima mais para o objetivo
        elif self.strategy == 'greedy':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.heuristic)
        #ordenamos pelo custo e heuristica (meio termo entre uniform e greedy) -> em media a* tem melhores resultados para todos
        elif self.strategy == 'a*':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.cost + node.heuristic )
