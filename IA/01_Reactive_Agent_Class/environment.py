
import threading
import numpy as np
import random
import copy

from cell import Cell
from reactive_agent import ReactiveAgent


class Environment(threading.Thread):

    def __init__(self, rows, columns, num_iterations):
        super(Environment, self).__init__()

        self.agent = None
        self.rows = rows
        self.columns = columns
        self.num_iterations = num_iterations
        self.iteration = None
        self.listeners = []
        self.thread_running = False
        self.dirt_rate = 0.0001

        self.grid = np.empty((rows, columns), dtype=Cell)

        self.initialize()

    def initialize(self) -> None:
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j] = Cell(i, j)

        self.grid[2][2].has_wall = True
        self.grid[2][3].has_wall = True
        self.grid[2][4].has_wall = True
        self.grid[4][2].has_wall = True

        self.agent = ReactiveAgent(self.grid[6][3])

        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].agent is None and not self.grid[i][j].has_wall:
                    self.grid[i][j].dirty = True

    def stop(self) -> None:
        self.thread_running = False

    def run(self) -> None:
        self.thread_running = True
        self.iteration = 0
        self.environment_updated()
        while self.iteration < self.num_iterations and self.thread_running:
            # Students should uncomment next line in exercise e)
            # self.dirt_update()
            self.agent.act(self)
            self.iteration += 1
            self.environment_updated()
        self.simulation_stopped()

    def dirt_update(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].agent is None and not self.grid[i][j].has_wall and not self.grid[i][j].dirty:
                    iterations_since_last_visit = self.iteration - self.grid[i][j].last_iteration
                    dirt_probability = iterations_since_last_visit * self.dirt_rate
                    if random.random() < dirt_probability:
                        self.grid[i][j].dirty = True

    def get_north_cell(self, cell: Cell) -> Cell:
        return self.grid[cell.line - 1][cell.column] if cell.line > 0 else None

    def has_north_cell(self, cell: Cell) -> bool:
        return self.get_north_cell(cell) is not None

    def get_south_cell(self, cell: Cell) -> Cell:
        return self.grid[cell.line + 1][cell.column] if cell.line < self.rows - 1 else None

    def has_south_cell(self, cell: Cell) -> bool:
        return self.get_south_cell(cell) is not None

    def get_east_cell(self, cell: Cell) -> Cell:
        return self.grid[cell.line][cell.column + 1] if cell.column < self.columns - 1 else None

    def has_east_cell(self, cell: Cell) -> bool:
        return self.get_east_cell(cell) is not None

    def get_west_cell(self, cell: Cell) -> Cell:
        return self.grid[cell.line][cell.column - 1] if cell.column > 0 else None

    def has_west_cell(self, cell: Cell) -> bool:
        return self.get_west_cell(cell) is not None

    def get_cell(self, line: int, column: int) -> Cell:
        return self.grid[line][column] if 0 <= line < self.rows and 0 <= column < self.columns else None

    def __str__(self) -> str:
        return np.array2string(self.grid)

    # Listeners

    def add_listener(self, listener):
        self.listeners.append(listener)

    def environment_updated(self) -> None:
        for listener in self.listeners:
            listener.queue.put((copy.deepcopy(self.grid), self.iteration, False))  # False: still running

    def simulation_stopped(self) -> None:
        for listener in self.listeners:
            listener.queue.put((copy.deepcopy(self.grid), self.iteration, True))  # True: done
