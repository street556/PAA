
from abc import ABC, abstractmethod

from agents.problem import Problem
from search_methods.solution import Solution


class SearchMethod(ABC):

    def __init__(self):
        self.num_expanded_nodes = 0
        self.num_generated_states = 0
        self.max_frontier_size = 0
        self.stopped = False

    @abstractmethod
    def search(self, problem: Problem) -> Solution:
        pass

    def reset(self):
        self.num_expanded_nodes = 0
        self.num_generated_states = 0
        self.max_frontier_size = 0

    def stop(self) -> None:
        self.stopped = True
