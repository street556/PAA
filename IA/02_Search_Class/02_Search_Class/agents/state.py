
from abc import ABC, abstractmethod


class State(ABC):

    def __init__(self):
        self.action = None

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass
