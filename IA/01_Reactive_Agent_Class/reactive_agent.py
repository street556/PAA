
import random

from action import Action
from cell import Cell
from perception import Perception


class ReactiveAgent:

    def __init__(self, cell: Cell):
        self.iteration = 0
        self.environment = None
        self.cell = cell
        cell.set_agent(self)

    def act(self, environment) -> None:
        perception = self.build_perception(environment)
        action = self.decide(perception)
        self.execute(action, environment)
        self.iteration += 1

    def set_cell(self, new_cell: Cell) -> None:
        self.cell.set_agent(None)
        self.cell = new_cell
        self.cell.set_agent(self)

    def build_perception(self, environment) -> Perception:
        return Perception(environment.get_north_cell(self.cell), environment.get_south_cell(self.cell),
                          environment.get_east_cell(self.cell), environment.get_west_cell(self.cell))

    def decide(self, perception: Perception) -> Action:
        return self.decide_a(perception)
        # return self.decide_b(perception)
        # return self.decide_c(perception)
        # return self.decide_d(perception)

    def execute(self, action: Action, environment) -> None:
        next_cell = None

        if action == Action.NORTH and environment.has_north_cell(self.cell):
            next_cell = environment.get_north_cell(self.cell)
        elif action == Action.SOUTH and environment.has_south_cell(self.cell):
            next_cell = environment.get_south_cell(self.cell)
        elif action == Action.EAST and environment.has_east_cell(self.cell):
            next_cell = environment.get_east_cell(self.cell)
        elif action == Action.WEST and environment.has_west_cell(self.cell):
            next_cell = environment.get_west_cell(self.cell)

        if next_cell is not None and not next_cell.has_wall and not next_cell.has_agent():
            self.set_cell(next_cell)

    def decide_a(self, perception: Perception):
        opposites = {
                    Action.NORTH: Action.SOUTH,
                    Action.SOUTH: Action.NORTH,
                    Action.EAST: Action.WEST,
                    Action.WEST: Action.EAST,
                }

        available_actions = [
                            action for action, cell in (
                                (Action.NORTH, perception.n),
                                (Action.SOUTH, perception.s),
                                (Action.EAST, perception.e),
                                (Action.WEST, perception.w),
                            )
                            if cell is not None and not cell.has_wall and not cell.has_agent()
                 ]               

                # Fallback caso não haja nenhuma ação disponível
        if not available_actions:
                    return Action.NORTH

                # Descobrir qual foi a última ação e qual é o seu oposto direto
        last_action = getattr(self, 'last_action', None)
        opposite_action = opposites.get(last_action) if last_action else None

                # Tentar filtrar ações que NÃO sejam voltar imediatamente para trás
        preferred_actions = [a for a in available_actions if a != opposite_action]

                # Se houver alternativas, escolhe a primeira; senão, permite recuar
        if preferred_actions:
                    chosen = preferred_actions[0]
        else:
                    chosen = available_actions[0]

                # Guardar a escolha para a próxima jogada
        self.last_action = chosen
        return chosen
        

    def decide_b(self, perception: Perception):

        # The agent should now be able to perceive dirt in adjacent
        # cells and use that information in its decision process.
        # This agent prefers to visit dirty cells first.

        return None

    def decide_c(self, perception: Perception):

        # Implement a memory mechanism that allows the agent to prefer
        # visiting cells that were visited the longest. Your goal is that
        # the agent visits as many cells as possible. This agent doesn’t
        # care about dirt. You may need to change the Cell class...

        return None

    def decide_d(self, perception: Perception):

        # Finally, implement a decision process in which the agent, besides
        # preferring to visit dirty cells first, it prefers to visit cells that
        # were visited the longest. It should consider the second criterium as a
        # tiebreaker, when more than one adjacent cell is dirty or if there are
        # no dirty adjacent cells.
        return None

