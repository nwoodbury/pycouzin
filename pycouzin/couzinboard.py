import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
from random import random
import os

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

    def run(self, saveloc=None):
        """
        Runs the simulation.

        Parameters
        ----------
        saveloc : str
            The video will be saved in <saveloc>/animation.mp4 (directory
            created as needed), and the first and last frame will be saved
            in <saveloc>/first.png and <saveloc>/last.png respectively.
        """
        fig = plt.figure(figsize=(24, 6))
        ax1 = plt.subplot2grid((1, 3), (0, 0), aspect='equal')
        ax2 = plt.subplot2grid((1, 3), (0, 1), colspan=2)
        time_text = ax1.text(0.02, 0.95, 'Initialization',
                             transform=ax1.transAxes)
        ax1.set_title('Agent Positions and Orientations')
        ax2.set_title('Fiedler Eigenvalues')

        ax1.tick_params(axis='x', labelbottom='off')
        ax1.tick_params(axis='y', labelleft='off')

        ax2.set_xlim((1, self.t))
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

        # Setup plots for fiedler eigenvalues and their averages
        feigsx = []
        feigsy = []
        favx = []
        favy = []
        fplot, = ax2.plot(feigsx, feigsy, label='Fiedler Eigenvalues')
        favplot, = ax2.plot(favx, favy, label='Average Fiedler Eigenvalue')

        if saveloc is not None and not os.path.exists(saveloc):
            os.makedirs(saveloc)

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
            minxs = min(xs) - 1
            minys = min(ys) - 1
            maxxs = max(xs) + 1
            maxys = max(ys) + 1
            xlen = maxxs - minxs
            ylen = maxys - minys
            length = max(xlen, ylen)
            ax1.set_xlim((minxs, minxs + length))
            ax1.set_ylim((minys, minys + length))
            ax1.grid(True)

            # Update fiedler eigenvalues plot
            feigsx.append(i + 1)
            favx.append(i + 1)
            feig = 1 + random()
            feigsy.append(feig)
            favy = sum(feigsy) / float(len(feigsy))
            fplot.set_data(feigsx, feigsy)  # TODO
            favplot.set_data(favx, favy)
            favplot.set_label('Average Fiedler Eigenvalue (%.2f)' % favy)
            ax2.legend(loc=3)

            ax2.set_ylim((0, max(feigsy)))
            ax2.grid(True)

            if saveloc:
                if i == 0:
                    plt.savefig('%s/first.png' % saveloc)
                if i == self.t - 1:
                    plt.savefig('%s/last.png' % saveloc)
            return ax1, ax2, scat, plots[0]

        ani = animation.FuncAnimation(fig, update_fig, frames=self.t,
                                      repeat=False, blit=True, interval=10)
        if saveloc:
            writer = animation.FFMpegWriter(fps=15, bitrate=2048)
            ani.save('%s/animation.mp4' % saveloc, writer=writer)
            plt.close()
        else:
            plt.show()
