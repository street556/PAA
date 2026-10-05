
from search_methods.informed_search import InformedSearch
from search_methods.node import Node
from agents.state import State


class AStarSearch(InformedSearch):

    # In this version we don't assume that the heuristic is consistent.

    # TODO
    # f = g + h
    def add_successor_to_frontier(self, successor: State, parent: Node) -> None:
        pass

    def __str__(self):
        return "A* search"
