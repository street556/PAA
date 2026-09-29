

class Cell:

    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column
        self.has_wall = False
        self.dirty = False
        self.agent = None

    @property
    def color(self) -> str:
        if self.has_agent():
            return 'red'
        if self.has_wall:
            return 'blue'
        if self.dirty:
            return 'gray'
        return 'white'

    def has_agent(self) -> bool:
        return self.agent is not None

    def set_agent(self, agent) -> None:
        self.agent = agent
        if self.has_agent():
            if self.dirty:
                self.dirty = False

    def __str__(self) -> str:
        if self.has_wall:
            return '#'
        elif self.has_agent():
            return 'X'
        elif self.dirty:
            return '-'
        else:
            '.'
