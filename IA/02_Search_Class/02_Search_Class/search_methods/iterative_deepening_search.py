
from search_methods.depth_limited_search import DepthLimitedSearch
from search_methods.search_method import SearchMethod
from search_methods.node import Node
from search_methods.solution import Solution
from agents.problem import Problem


class IterativeDeepeningSearch(DepthLimitedSearch):

    def __init__(self):
        super().__init__()
        self.states_in_the_limit_level = None

    # We do not use the code from DepthLimitedSearch because we can optimize
    # so that the algorithm only verifies if a state is a goal if its depth is
    # equal to the limit. Note that given a limit X we are sure not to
    # encounter a solution below this limit because a (failed) limited depth
    # search has already been done. That's why we do not extend this class from
    # DepthLimitedSearch. We extend from DepthFirstSearch so that we don't need
    # to rewrite method insertSuccessorsInFrontier again.
    # After the class, please see a version of the search algorithm without
    # this optimization.

    def search(self, problem: Problem) -> Solution:
        self.reset()
        self.stopped = False
        self.limit = 0
        while True:
            self.states_in_the_limit_level = 0
            solution = self.graph_search(problem)
            if solution is not None or self.states_in_the_limit_level == 0:
                return solution
            self.limit += 1

    def graph_search(self, problem: Problem) -> Solution:
        self._frontier.clear()
        self._frontier.append(Node(problem.initial_state))
        self.num_generated_states += 1

        while len(self._frontier) != 0 and not self.stopped:
            node = self._frontier.pop()
            state = node.state

            if node.depth == self.limit:
                self.states_in_the_limit_level += 1
                if problem.is_goal(state):
                    return Solution(problem, node)

            num_successors_size = 0
            if node.depth < self.limit:
                actions = problem.get_actions(state)
                num_successors_size = len(actions)
                for action in actions:
                    successor = problem.get_successor(state, action)
                    self.add_successor_to_frontier(successor, node)

            self.compute_statistics(num_successors_size)

    def __str__(self):
        return "Iterative deepening search"


#########################################################


class NonOptimizedIterativeDeepeningSearch(SearchMethod):

    def search(self, problem: Problem) -> Solution:
        depth_limited_search = DepthLimitedSearch()
        i = 0
        while True:
            depth_limited_search.limit = i
            solution = depth_limited_search.search(problem)
            self.limit += 1
            if solution is not None:
                return solution
            i += 1
