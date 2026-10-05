
from abc import ABC, abstractmethod

from agents.state import State
from agents.action import Action


class Problem(ABC):

    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.heuristic = None

    # Returns a list of valid actions for the given state
    @abstractmethod
    def get_actions(self, state: State) -> list:
        pass

    # Returns the successor state resulting from applying the given action to the given state
    @abstractmethod
    def get_successor(self, state: State, action: Action) -> State:
        pass

    # Returns True if the given state is a goal state, False otherwise
    @abstractmethod
    def is_goal(self, state: State) -> bool:
        pass

    # Returns the cost of a path, which is the sum of the costs of the actions in the path
    def compute_path_cost(self, path: list) -> int:
        cost = 0
        for action in path:
            cost += action.cost
        return cost
