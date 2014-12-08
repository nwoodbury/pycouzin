import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
from random import random

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
        fig = plt.figure(figsize=(24, 6))
        ax1 = plt.subplot2grid((1, 3), (0, 0), aspect='equal')
        ax2 = plt.subplot2grid((1, 3), (0, 1), colspan=2)
        time_text = ax1.text(0.02, 0.95, 'Initialization',
                             transform=ax1.transAxes)
        ax1.set_title('Agent Positions and Orientations')
        ax2.set_title('Average Fiedler Eigenvalue')

        ax1.tick_params(axis='x', labelbottom='off')
        ax1.tick_params(axis='y', labelleft='off')

        ax2.set_xlim((0, self.t))
        # ax2.set_ylim((0, 10))

        xs = [agent.p.x for agent in self.agents]
        ys = [agent.p.y for agent in self.agents]

        colors = [agent.color for agent in self.agents]

        scat = ax1.scatter(xs, ys, c=colors, s=50)

        plots = []
        for agent in self.agents:
            p = agent.p
            o = agent.o
            plot, = ax1.plot([p.x, p.x + o.x], [p.y, p.y + o.y], 'k')
            plots.append(plot)

        feigsx = []
        feigsy = []
        fplot, = ax2.plot(feigsx, feigsy)

        def update_fig(i):
            # Update time text
            time_text.set_text('t = %i' % (i + 1))

            # Update Agent positions
            self.update()
            xs = [agent.p.x for agent in self.agents]
            ys = [agent.p.y for agent in self.agents]
            data = np.array([xs, ys]).transpose()
            scat.set_offsets(data)

            # Update Agent Orientations
            for j in range(len(plots)):
                agent = self.agents[j]
                p = agent.p
                o = agent.o
                plot = plots[j]
                plot.set_data([p.x, p.x + o.x], [p.y, p.y + o.y])

            # Update axes
            minval = min(xs + ys) - 1
            maxval = max(xs + ys) + 1
            ax1.set_xlim((minval, maxval))
            ax1.set_ylim((minval, maxval))
            ax1.grid(True)

            # Update fiedler eigenvalues plot
            feigsx.append(i)
            feig = 1 + random()
            feigsy.append(feig)
            fplot.set_data(feigsx, feigsy)  # TODO
            ax2.set_ylim((0, max(feigsy)))
            ax2.grid(True)

            return ax1, ax2, scat, plots[0]

        ani = animation.FuncAnimation(fig, update_fig, frames=self.t,
                                      repeat=False, blit=True, interval=10)
        plt.show()
        # ani.save('test.mp4', fps=15)

        # for i in range(self.t):
        #    print i
        #    self.update()
