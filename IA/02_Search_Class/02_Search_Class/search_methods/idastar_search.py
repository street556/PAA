
import sys

from search_methods.iterative_deepening_search import IterativeDeepeningSearch
from search_methods.node import Node
from search_methods.solution import Solution
from agents.problem import Problem
from agents.state import State


class IDAStarSearch(IterativeDeepeningSearch):

    # This algorithm is a hybrid: it is an informed algorithm, but it is based on the
    # Iterative Deepening Algorithm(IDA).
    # That's why we make it a subclass of IterativeDeepeningSearch class instead of the InformedSearch one:
    # it uses a NodeQueue instead of a NodePriorityQueue.
    # Despite the fact that it is based on IDA, we don't reuse any code of it because all methods
    # (search, search_graph and add_successor_to_frontier) have their particularities.
    # Note that, on each  iteration, the search is done in a depth first search way.

    def __init__(self):
        super().__init__()
        self.heuristic = None
        self.new_limit = 0

    def search(self, problem: Problem) -> Solution:
        self.reset()
        self.stopped = False
        self.heuristic = problem.heuristic
        self.limit = self.heuristic.compute(problem.initial_state)
        while True:
            solution = self.graph_search(problem)
            if solution is not None or self.limit == sys.float_info.max:
                return solution

    def graph_search(self, problem: Problem) -> Solution:
        self.new_limit = sys.float_info.max
        self._frontier.clear()
        self._frontier.append(Node(problem.initial_state))
        self.num_generated_states += 1

        while len(self._frontier) != 0 and not self.stopped:
            node = self._frontier.pop()
            state = node.state

            if problem.is_goal(state) and node.f <= self.limit:
                return Solution(problem, node)

            actions = problem.get_actions(state)
            for action in actions:
                successor = problem.get_successor(state, action)
                self.add_successor_to_frontier(successor, node)

            self.compute_statistics(len(actions))

        self.limit = self.new_limit

    def add_successor_to_frontier(self, successor: State, parent: Node) -> None:
        if successor not in self._frontier:
            g = parent.g + successor.action.cost
            f = g + self.heuristic.compute(successor)
            if f <= self.limit:
                if not parent.is_cycle(successor):
                    self._frontier.insert_as_first(Node(successor, parent, g=g, f=f))
            else:
                self.new_limit = min(self.new_limit, f)

    def __str__(self):
        return "IDA Star search"
