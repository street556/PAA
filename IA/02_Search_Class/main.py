
import numpy as np

from gui import Window
from eightpuzzle.actions import *

from eightpuzzle.eight_puzzle_state import read_state_from_txt_file


if __name__ == '__main__':
    gui = Window()
    gui.mainloop()

    # action_up = ActionUp()
    # action_right = ActionRight()
    # action_down = ActionDown()
    # action_left = ActionLeft()

    # puzzle = read_puzzle_from_txt_file("states/initial_state_3.txt")
    # eight_puzzle = EightPuzzleState(puzzle)
    # print(eight_puzzle)

    # action_up.execute(eight_puzzle)
    # action_left.execute(eight_puzzle)
    # action_left.execute(eight_puzzle)
    # print(eight_puzzle)
    # print(eight_puzzle.get_action())
