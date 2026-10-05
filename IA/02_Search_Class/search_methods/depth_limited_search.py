
from search_methods.depth_first_search import DepthFirstSearch
from search_methods.node import Node
from search_methods.solution import Solution
from agents.problem import Problem


class DepthLimitedSearch(DepthFirstSearch):

    def __init__(self, limit: int = 28):
        super().__init__()
        self.limit = limit

    def graph_search(self, problem: Problem) -> Solution:
        self._frontier.clear()
        self._frontier.append(Node(problem.initial_state))

        while len(self._frontier) != 0 and not self.stopped:
            node = self._frontier.pop()
            state = node.state

            if problem.is_goal(state):
                return Solution(problem, node)

            successors_size = 0
            if node.depth < self.limit:
                actions = problem.get_actions(state)
                successors_size = len(actions)
                for action in actions:
                    successor = problem.get_successor(state, action)
                    self.add_successor_to_frontier(successor, node)

            self.compute_statistics(successors_size)

    def __str__(self):
        return "Limited depth first search"
