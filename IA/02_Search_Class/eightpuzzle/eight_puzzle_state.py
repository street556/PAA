
import numpy as np
from numpy import ndarray
from agents.state import State


class EightPuzzleState(State):

    def __init__(self, matrix: ndarray):
        super().__init__()
        self.rows = matrix.shape[0]
        self.columns = matrix.shape[1]
        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)

        self._line_blank = None
        self._column_blank = None

        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = matrix[i][j]
                if self.matrix[i][j] == 0:
                    self._line_blank = i
                    self._column_blank = j

    def can_move_up(self) -> bool:
        return self._line_blank != 0

    def can_move_right(self) -> bool:
        return self._column_blank != self.columns - 1

    def can_move_down(self) -> bool:
        return self._line_blank != self.rows - 1

    def can_move_left(self) -> bool:
        return self._column_blank != 0

    def move_up(self) -> None:
        self.matrix[self._line_blank][self._column_blank] = self.matrix[self._line_blank - 1][self._column_blank]
        self._line_blank -= 1
        self.matrix[self._line_blank][self._column_blank] = 0

    def move_right(self) -> None:
        self.matrix[self._line_blank][self._column_blank] = self.matrix[self._line_blank][self._column_blank + 1]
        self._column_blank += 1
        self.matrix[self._line_blank][self._column_blank] = 0

    def move_down(self) -> None:
        self.matrix[self._line_blank][self._column_blank] = self.matrix[self._line_blank + 1][self._column_blank]
        self._line_blank += 1
        self.matrix[self._line_blank][self._column_blank] = 0

    def move_left(self) -> None:
        self.matrix[self._line_blank][self._column_blank] = self.matrix[self._line_blank][self._column_blank - 1]
        self._column_blank -= 1
        self.matrix[self._line_blank][self._column_blank] = 0

    def get_tile_value(self, row: int, column: int) -> int:
        if not self.is_valid_position(row, column):
            raise IndexError("ERROR: invalid position!")
        return self.matrix[row][column]

    def is_valid_position(self, row: int, column: int) -> bool:
        return 0 <= row < self.rows and 0 <= column < self.columns

    def __str__(self):
        return np.array2string(self.matrix)

    def __eq__(self, other):
        if isinstance(other, EightPuzzleState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tobytes())


def read_state_from_txt_file(filename: str) -> EightPuzzleState:
    float_puzzle = np.genfromtxt(filename, delimiter=' ')
    int_puzzle = np.int_(float_puzzle)
    return EightPuzzleState(int_puzzle)

# Alternative
# def read_puzzle_from_txt_file(filename: str) -> ndarray:
#    matrix = []
#    with open(filename, 'r') as file:
#        for line in file:
#            matrix.append([int(x) for x in line.split()])
#
#    # Convert the matrix to a numpy ndarray
#   return np.array(matrix)
