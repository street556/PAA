
from abc import ABC, abstractmethod
from agents.state import State


class Action(ABC):

    def __init__(self, cost):
        self.cost = cost

    @abstractmethod
    def execute(self, state: State) -> None:
        pass

    @abstractmethod
    def is_valid(self, state: State) -> bool:
        pass

