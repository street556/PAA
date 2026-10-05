
from abc import abstractmethod

from search_methods.graph_search import GraphSearch
from utils.node_priority_queue import NodePriorityQueue
from agents.problem import Problem
from search_methods.solution import Solution
from agents.state import State
from search_methods.node import Node


class InformedSearch(GraphSearch):

    def __init__(self):
        super().__init__()
        self._frontier = NodePriorityQueue()
        self.heuristic = None

    def search(self, problem: Problem) -> Solution:
        self.reset()
        self.stopped = False
        self.heuristic = problem.heuristic
        return self.graph_search(problem)

    @abstractmethod
    def add_successor_to_frontier(self, successor: State, parent: Node) -> None:
        pass
