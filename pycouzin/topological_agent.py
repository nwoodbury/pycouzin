from pycouzin.agent import Agent
from pycouzin.vector import Vector2D
from random import normalvariate
import math


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
        noise = normalvariate(0.0, 0.2)
        noise_vec = Vector2D(0, 0)
        noise_vec.set_angle(noise)
        in_repulsion = self.get_adjacent_agents(a_r, agents)
        if len(in_repulsion) > 0:
            # agents in zone of repulsion, ignore orientation and attraction
            d_r = Vector2D(0, 0)
            for agent in in_repulsion:
                rij = (agent.p - self.p).normalize()
                d_r -= rij
            d_r.normalize()
            d_i = d_r
        else:
            # if no agents in the zone of repulsion, orientation and attraction
            # dictate

            # orientation zone
            d_o = Vector2D(0, 0)
            in_orientation = self.get_adjacent_agents(a_o, agents)
            for agent in in_orientation:
                vj = agent.o.normalize()
                d_o += vj
            d_o.normalize()

            # attraction zone
            d_a = Vector2D(0, 0)
            in_attraction = self.get_adjacent_agents(a_a, agents)
            for agent in in_attraction:
                rij = (agent.p - self.p).normalize()
                d_a += rij
            d_a.normalize()
            d_i = (d_o + d_a) * 0.5

        return (d_i + noise_vec).normalize()

    def update(self, a_r, a_o, a_a, a_k, agents):
        """
        Updates this agent's position and orientation according to Couzin's
        dynamics.

        See `Agent.update()`
        """
        d = self.get_desired_direction(a_r, a_o, a_a, agents)
        d = self.reg_ang_v(d)
        self.o = d
        self.p += self.o * self.speed

    def reg_ang_v(self, d_i):
        """
        Regulates the angular velocity of the agent by making sure that
        the desired change in orientation is <= thetamax
        d_i: desired direction vector
        """
        ang_des = d_i.get_angle()
        ang_curr = self.o.get_angle()
        diff = ang_des - ang_curr

        if diff > math.pi:
            diff -= 2*math.pi
        elif diff < -math.pi:
            diff += 2*math.pi

        if diff > self.thetamax:
            diff = self.thetamax
        elif diff < -self.thetamax:
            diff = -self.thetamax
        else:
            return d_i

        ang_des = ang_curr + diff
        return Vector2D(math.cos(ang_des), math.sin(ang_des))
