
from agents.heuristic import Heuristic
from eightpuzzle.eight_puzzle_state import EightPuzzleState


class HeuristicTilesOutOfPlace(Heuristic):

    def __init__(self):
        super().__init__()

    # TODO
    def compute(self, state: EightPuzzleState) -> float:
        pass

    def __str__(self):
        return "Tiles out of place"
