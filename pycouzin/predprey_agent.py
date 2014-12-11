from pycouzin.topological_agent import TopologicalAgent
from pycouzin.vector import Vector2D


class PredatorAgent(TopologicalAgent):

    color = 'r'

    desist_num = 3
    desist_r = 5
    pred_r = 3

    def get_desired_direction(self, a_r, a_o, a_a, agents):
        """
        Chases the nearest prey, ignoring everything else on the board.

        It's speed is twice the prey's, angular velocity is 4x
        """
        self.speed = 1.0
        self.thetamax = 0.20
        nearest_prey = None
        nearest_dist = float('Inf')

        in_desist_r = 0
        prey_count = 0
        d_p = Vector2D(0, 0)
        d_o = Vector2D(0, 0)
        for agent in agents:
            distance = self.p.distance_to(agent.p)
            if isinstance(agent, PreyAgent):
                prey_count += 1
                rp = (agent.p - self.p).normalize()
                d_p += rp
                if distance <= self.desist_r:
                    in_desist_r += 1
                if distance < nearest_dist:
                    nearest_dist = distance
                    nearest_prey = agent
            if isinstance(agent, PredatorAgent):
                # Avoid other predators that are too close
                if distance <= self.pred_r:
                    ro = (agent.p - self.p).normalize()
                    d_o -= ro

        if nearest_prey is None:
            # All prey dead. Stop
            self.speed = 0
            self.thetamax = 0
            return d_o.normalize()
        elif in_desist_r < self.desist_num and prey_count > self.desist_num:
            # Too few prey nearby with many surviving, turn back to main body
            return (d_p.normalize() + d_o.normalize()).normalize()
        else:
            d = (nearest_prey.p - self.p).normalize()
            return (d + d_o.normalize()).normalize()


class PreyAgent(TopologicalAgent):

    color = 'c'
    pred_repulsion = 5
    dead_repulsion = 7
    pred_kill = 0.75

    def get_desired_direction(self, a_r, a_o, a_a, agents):
        base_speed = 0.5
        self.speed = base_speed
        self.thetamax = 0.05

        # Check to see if predators or dead agents are nearby
        d_p = Vector2D(0, 0)
        d_d = Vector2D(0, 0)
        run = False    # should run from predator
        evade = False  # should evade the dead
        for agent in agents:
            distance = self.p.distance_to(agent.p)
            if isinstance(agent, PredatorAgent):
                if distance <= self.pred_kill:
                    # Kill, too close to predator
                    dead = DeadAgent(self.board, self.p, self.o)
                    dead.i = self.i
                    self.replace_with = dead
                    return Vector2D(0, 0)
                if distance <= self.pred_repulsion:
                    # Adreneline rush, run from predator at 3x speed
                    run = True
                    self.speed = base_speed * 3
                    pij = (agent.p - self.p).normalize()
                    d_p -= pij
            elif isinstance(agent, DeadAgent) and\
                    distance <= self.dead_repulsion:
                evade = True
                rd = (agent.p - self.p).normalize()
                d_d -= rd

        base = TopologicalAgent.get_desired_direction(
            self, a_r, a_o, a_a, agents)
        if run:
            return (d_p.normalize() + base).normalize()
        elif evade:
            return (d_d.normalize() + base).normalize()
        else:
            return base

    def get_adjacent_agents(self, a, agents):
        """
        Only consider other Prey as adjacent, other types are taken into
        special consideration.
        """
        all_adj = TopologicalAgent.get_adjacent_agents(self, a, agents)
        adj_agents = []
        for agent in all_adj:
            if isinstance(agent, PreyAgent):
                adj_agents.append(agent)
        return adj_agents


class DeadAgent(TopologicalAgent):

    color = 'k'

    def __init__(self, board, p0=None, o0=None):
        TopologicalAgent.__init__(self, board, p0, o0)
        self.speed = 0
        self.thetamax = 0
