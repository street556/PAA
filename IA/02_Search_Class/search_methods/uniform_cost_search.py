
from utils.node_priority_queue import NodePriorityQueue
from search_methods.graph_search import GraphSearch
from search_methods.node import Node
from agents.state import State


class UniformCostSearch(GraphSearch):

    def __init__(self):
        super().__init__()
        self._frontier = NodePriorityQueue()

    # TODO
    # f = g
    def add_successor_to_frontier(self, successor: State, parent: Node) -> None:
        g = parent.g + successor.action.cost
        if successor not in self._frontier:
            if successor not in self._explored:
                self._frontier.append(Node(successor, parent, g=g, f=g))
        elif g < self._frontier[successor].g:
            del self._frontier[successor]
            self._frontier.append(Node(successor, parent, g=g, f=g))

    def __str__(self):
        return "Uniform cost search"
