
from agents.problem import Problem
from search_methods.node import Node


class Solution:

    def __init__(self, problem: Problem, goal_node: Node):
        self.problem = problem
        node = goal_node
        self.actions = []
        while node.parent is not None:
            self.actions.insert(0, node.state.action)
            node = node.parent

    @property
    def cost(self) -> float:
        return self.problem.compute_path_cost(self.actions)
