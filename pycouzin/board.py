import random
import numpy as np
import copy
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

    def adjacency(self, condition, state_update=None):
        """
        Returns an adjacency matrix based on the given condition.

        Parameters
        ----------
        condition : function : agent, agent -> boolean
            A function that takes two agents and returns True if they are to
            be considered adjacent, false otherwise.
        state_update : function : agent -> None, or None
            If None (default), does nothing. Otherwise, calls a function to
            update the state of the given agent (e.g. find and store its
            nearest neighbors).

        Returns
        -------
        A : numpy.ndarray
            A matrix where a_ij = a_ji = 1 if and only if agents i and j are
            adjacent.
        """
        a = np.zeros((self.n, self.n))
        for i in range(self.n):
            if state_update is not None:
                state_update(self.agents[i])
            for j in range(i + 1, self.n):
                if condition(self.agents[i], self.agents[j]):
                    a[i, j] = 1
                    a[j, i] = 1
        return a

    def radius_adjacency(self, max_radius, min_radius=0):
        """
        Returns an adjacency matrix where agents i and j are considered to be
        adjacent if the distance d is between min_radius (inclusive)
        and max_radius (exclusive).

        Parameters
        ----------
        max_radius : number
            All adjacent agents must be within this distance of each other.
        min_radius : number
            All adjacent agents must be outside this distance of each other,
            defaults to 0.

        Returns
        -------
        A : numpy.ndarray
            See `self.adjacency()`
        """
        def condition(a1, a2):
            d = a1.p.distance_to(a2.p)
            if d < max_radius and d >= min_radius:
                return True
            else:
                return False

        return self.adjacency(condition)

    def laplacian(self, adjacency):
        """
        Computes and returns the laplacian of the adjacency matrix.

        Parameters
        ----------
        adjacency : numpy.ndarray

        Returns
        -------
        laplacian : numpy.ndarray
        """
        l = copy.deepcopy(adjacency)
        s = sum(adjacency)
        l = l * -1
        for i in range(self.n):
            l[i, i] = s[i]
        return l
