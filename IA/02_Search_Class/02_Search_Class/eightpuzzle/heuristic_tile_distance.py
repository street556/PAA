
import numpy as np

from agents.heuristic import Heuristic
from eightpuzzle.eight_puzzle_problem import EightPuzzleProblem
from eightpuzzle.eight_puzzle_state import EightPuzzleState


class HeuristicTileDistance(Heuristic):

    def __init__(self):
        super().__init__()
        self._goal_matrix_positions = None

    def compute(self, state: EightPuzzleState) -> float:
        h = 0
        for i in range(state.rows):
            for j in range(state.columns):
                tile = state.matrix[i][j]
                # Blank is ignored so that the heuristic is admissible
                if tile != 0:
                    tile_goal_line, tile_goal_column = self._goal_matrix_positions[tile]
                    h += abs(i - tile_goal_line) + abs(j - tile_goal_column)
        return h

    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, problem: EightPuzzleProblem):
        self._problem = problem
        self.build_aux_arrays()

    def __str__(self):
        return "Tiles distance to final position"

    def build_aux_arrays(self) -> None:
        goal_matrix = self._problem.goal_state.matrix
        goal_matrix_positions = []
        for i in range(9):
            position = np.where(goal_matrix == i)
            goal_matrix_positions.append(position)
        self._goal_matrix_positions = np.array(goal_matrix_positions)
