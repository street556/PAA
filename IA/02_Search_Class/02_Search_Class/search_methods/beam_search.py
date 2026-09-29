
from search_methods.astar_search import AStarSearch
from search_methods.node import Node
from search_methods.solution import Solution
from agents.problem import Problem


class BeamSearch(AStarSearch):

    def __init__(self, beam_size: int = 100):
        super().__init__()
        self.beam_size = beam_size

    def graph_search(self, problem: Problem) -> Solution:
        self._frontier.clear()
        self._explored.clear()
        self._frontier.append(Node(problem.initial_state))

        while len(self._frontier) != 0 and not self.stopped:
            node = self._frontier.pop()
            state = node.state
            if problem.is_goal(state):
                return Solution(problem, node)

            self._explored.add(state)
            actions = problem.get_actions(state)
            for action in actions:
                successor = problem.get_successor(state, action)
                self.add_successor_to_frontier(successor, node)

            self.manage_frontier_size()
            self.compute_statistics(len(actions))

    def manage_frontier_size(self) -> None:
        while len(self._frontier) > self.beam_size:
            self._frontier.remove_last()

    def __str__(self):
        return "Beam search"
