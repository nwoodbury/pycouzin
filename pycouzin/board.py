import random
from pycouzin.vector import Vector2D


class Board:
    """
    General class defining a board.

    Parameters
    ----------
    n : int
        The number of agents
    m : number
        Defines the size of the board. x & y will range from -m to m.
    agent_init : function : self -> list of Agent
        A function taking this board object as a parameter and returns a list
        of n agents. This function is used to initialize the agent list.
    """

    def __init__(self, n, m, agent_init):
        self.n = n
        self.m = m

        self.agents = agent_init(self)
        assert len(self.agents) == self.n

    def get_random_point(self):
        """
        Returns a random point on the board.

        Returns
        -------
        point : Vector2D
        """
        x = random.uniform(-self.m, self.m)
        y = random.uniform(-self.m, self.m)
        return Vector2D(x, y)
