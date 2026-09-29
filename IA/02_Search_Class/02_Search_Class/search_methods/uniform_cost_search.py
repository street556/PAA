
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
        pass

    def __str__(self):
        return "Uniform cost search"
