
from agents.problem import Problem
from agents.heuristic import Heuristic
from search_methods.breadth_first_search import BreadthFirstSearch
from search_methods.uniform_cost_search import UniformCostSearch
from search_methods.depth_first_search import DepthFirstSearch
from search_methods.depth_limited_search import DepthLimitedSearch
from search_methods.iterative_deepening_search import IterativeDeepeningSearch
from search_methods.greedy_best_first_search import GreedyBestFirstSearch
from search_methods.astar_search import AStarSearch
from search_methods.beam_search import BeamSearch
from search_methods.idastar_search import IDAStarSearch
from search_methods.solution import Solution


class Agent:

    def __init__(self):
        self.environment = None
        self.search_methods = [
            BreadthFirstSearch(),
            UniformCostSearch(),
            DepthFirstSearch(),
            DepthLimitedSearch(),
            IterativeDeepeningSearch(),
            GreedyBestFirstSearch(),
            AStarSearch(),
            BeamSearch(),
            IDAStarSearch()
        ]
        self.search_method = self.search_methods[0]
        self.heuristics = []
        self.heuristic = None
        self.solution = None

    def solve_problem(self, problem: Problem) -> Solution:
        self.environment = problem.initial_state
        if self.heuristic is not None:
            problem.heuristic = self.heuristic
            self.heuristic.problem = problem
        self.solution = self.search_method.search(problem)
        return self.solution

    def execute_solution(self) -> None:
        if self.solution:
            print(self.environment)
            for action in self.solution.actions:
                action.execute(self.environment)
                print(action)
                print(self.environment)
            print('Solution cost: ', self.solution.cost)
        else:
            print('No solution to be executed')

    def stop(self) -> None:
        self.search_method.stop()

    def has_been_stopped(self) -> bool:
        return self.search_method.stopped

    def set_search_method(self, search_method_index: int):
        if 0 <= search_method_index < len(self.search_methods):
            self.search_method = self.search_methods[search_method_index]
        else:
            raise IndexError('ERROR: index out of bounds.')

    def add_heuristic(self, heuristic: Heuristic) -> None:
        self.heuristics.append(heuristic)
