
from utils.node_queue import NodeQueue
from search_methods.graph_search import GraphSearch
from search_methods.node import Node
from search_methods.solution import Solution
from agents.problem import Problem
from agents.state import State


class DepthFirstSearch(GraphSearch):

    def __init__(self):
        super().__init__()
        self._frontier = NodeQueue()

    def graph_search(self, problem: Problem) -> Solution:
        self._frontier.clear()
        self._frontier.append(Node(problem.initial_state))

        while len(self._frontier) != 0 and not self.stopped:
            node = self._frontier.pop()
            state = node.state

            if problem.is_goal(state):
                return Solution(problem, node)

            actions = problem.get_actions(state)
            for action in actions:
                successor = problem.get_successor(state, action)
                self.add_successor_to_frontier(successor, node)

            self.compute_statistics(len(actions))

    def add_successor_to_frontier(self, successor: State, parent: Node) -> None:
        if successor not in self._frontier:
            #  We are sure that parent is always not None
            if not parent.is_cycle(successor):
                self._frontier.insert_as_first(Node(successor, parent))

    def __str__(self):
        return "Depth first search"
