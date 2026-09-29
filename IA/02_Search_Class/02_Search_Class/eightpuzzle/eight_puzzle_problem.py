
import copy

from agents.problem import Problem
from eightpuzzle.actions import *


class EightPuzzleProblem(Problem):

    def __init__(self, initial_state: EightPuzzleState, goal_state: EightPuzzleState):
        super().__init__(initial_state)
        self.actions = [ActionDown(), ActionUp(), ActionRight(), ActionLeft()]
        self.goal_state = goal_state

    # Returns a list of valid actions for the given state
    def get_actions(self, state: EightPuzzleState) -> list:
        valid_actions = []
        for action in self.actions:
            if action.is_valid(state):
                valid_actions.append(action)
        return valid_actions

    # Returns the successor state resulting from applying the given action to the given state
    def get_successor(self, state: EightPuzzleState, action: Action) -> EightPuzzleState:
        successor = copy.deepcopy(state)
        action.execute(successor)
        return successor

    # Returns True if the given state is a goal state, False otherwise
    def is_goal(self, state: EightPuzzleState) -> bool:
        return self.goal_state == state


    # Returns the cost of a path, which, in the Eight Puzzle, is the number actions in the path
    def compute_path_cost(self, path: list) -> int:
        return len(path)

    # This method assumes that the tiles in the goal state are ordered from top to bottom, from left to right.
    # The blank tile can be anywhere.
    def is_solvable(self) -> bool:
        matrix_list = self.initial_state.matrix.tolist()
        num_inversions = self.count_inversions([j for line in matrix_list for j in line])
        return num_inversions % 2 == 0

    def count_inversions(self, tiles: list) -> int:
        num_inversions = 0
        blank = 0
        puzzle_size = len(tiles)
        for i in range(puzzle_size):
            for j in range(i + 1, puzzle_size):
                if tiles[j] != blank and tiles[i] != blank and tiles[i] > tiles[j]:
                    num_inversions += 1
        return num_inversions
