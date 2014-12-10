from pycouzin.agent import Agent
from pycouzin.vector import Vector2D
from random import random


class TopologicalAgent(Agent):
    """
    An agent whose dynamics are defined by radii of repulsion, orientation,
    and attraction.

    See `Agent` for initialization.
    """

    color = 'b'

    def get_desired_direction(self, a_r, a_o, a_a, agents):
        """
        Computes the desired direction.
        """
        in_repulsion = self.get_adjacent_agents(a_r, agents)
        if len(in_repulsion) > 0:
            # agents in zone of repulsion, ignore orientation and attraction
            d_r = Vector2D(0, 0)
            for agent in in_repulsion:
                rij = (agent.p - self.p).normalize()
                d_r -= rij
            d_r.normalize()
            print d_r
        else:
            return 0

    def update(self, a_r, a_o, a_a, a_k, agents):
        """
        Updates this agent's position and orientation according to Couzin's
        dynamics.

        See `Agent.update()`
        """
        # d = self.get_desired_direction(a_r, a_o, a_a, agents)
        self.p += self.o * self.speed
