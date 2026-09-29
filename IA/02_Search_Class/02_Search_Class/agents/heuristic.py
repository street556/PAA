
from abc import ABC, abstractmethod
from agents.state import State
from agents.problem import Problem


class Heuristic(ABC):

    def __init__(self):
        self._problem = None

    @abstractmethod
    def compute(self, state: State) -> float:
        pass

    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, problem: Problem):
        self._problem = problem
