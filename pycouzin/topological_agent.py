from pycouzin.agent import Agent


class TopologicalAgent(Agent):
    """
    An agent whose dynamics are defined by radii of repulsion, orientation,
    and attraction.

    See `Agent` for initialization.
    """

    color = 'b'

    def update(self, a_r, a_o, a_a, a_k, agents):
        """
        Updates this agent's position and orientation according to Couzin's
        dynamics.

        See `Agent.update()`
        """
        self.p.x += 0.5
        self.p.y += 0.4
