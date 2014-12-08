import matplotlib.pyplot as plt

from pycouzin.board import Board


class CouzinBoard(Board):
    """
    Class defining a board that runs the couzin simulations.

    Parameters
    ----------
    n : int
        The number of agents
    m : number
        The agents will be placed between [-m, m] coordinates at initialization
    agent_init : function : self, list of Agent
        A function taking this board object as a parameter and returns a list
        of n agents. This function is used to initialize the agent list.
    rr : number
        The radius of repulsion for agents implementing topology dynamics.
    ro : number
        The radius of orientation for agents implementing topology dynamics.
    ra : number
        The radius of attraction for agents implementing topology dynamics.
    k : int
        The number of nearest neighbors for agents implementing nearest
        neighbor dynamics.
    t : int
        The number of time steps to simulate, default = 100.
    """
    def __init__(self, n, m, agent_init, rr, ro, ra, k, t=100):
        Board.__init__(self, n, m, agent_init)
        self.rr = rr
        self.ro = ro
        self.ra = ra
        self.k = k
        self.t = t

    def adjacency(self, condition, state_update=None):
        """
        We only care about bi-directional adjacency now. See documentation
        for `bidirectional_adjacency()` in the parent class.
        """
        return self.bidirectional_adjacency(condition, state_update)

    def update(self):
        """
        Updates the position of the agents on the board.
        """
        a_r = self.radius_adjacency(self.rr)
        a_o = self.radius_adjacency(self.ro, self.rr)
        a_a = self.radius_adjacency(self.ra, self.ro)
        a_k = self.nearest_adjacency(self.k)
        for agent in self.agents:
            agent.update(a_r, a_o, a_a, a_k, self.agents)

    def run(self):
        """
        Runs the simulation.
        """
        fig = plt.figure(figsize=(12, 12))

        xs = [agent.p.x for agent in self.agents]
        ys = [agent.p.y for agent in self.agents]

        colors = [agent.color for agent in self.agents]

        scat = plt.scatter(xs, ys, c=colors, s=50)

        plots = []
        for agent in self.agents:
            p = agent.p
            o = agent.o
            plot = plt.plot([p.x, p.x + o.x], [p.y, p.y + o.y], 'k')

        plt.show()

        # for i in range(self.t):
        #    print i
        #    self.update()
