
from search_methods.informed_search import InformedSearch
from search_methods.node import Node
from agents.state import State


class GreedyBestFirstSearch(InformedSearch):

    # TODO
    # f = h
    def add_successor_to_frontier(self, successor: State, parent: Node) -> None:
        g = parent.g + successor.action.cost
        if successor not in self._frontier:
            if successor not in self._explored:
                f = self.heuristic.compute(successor)
                self._frontier.append(Node(successor, parent, g, f))
        elif g < self._frontier[successor].g:
            del self._frontier[successor]
            f = self.heuristic.compute(successor)
            self._frontier.append(Node(successor, parent, g, f))
    
    def __str__(self):
        return "Greedy best first search"
