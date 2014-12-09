import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import math

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
        def fied_adj(a):
            return self.get_fied(self.laplacian(a))
        a_r = self.radius_adjacency(self.rr)
        a_o = self.radius_adjacency(self.ro, self.rr)
        a_a = self.radius_adjacency(self.ra, self.ro)
        a_k = self.nearest_adjacency(self.k)
        for agent in self.agents:
            agent.update(a_r, a_o, a_a, a_k, self.agents)
        return fied_adj(a_a), fied_adj(a_o), fied_adj(a_r), fied_adj(a_k), \
            fied_adj(a_a + a_o + a_r)

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
        fig = plt.figure(figsize=(32, 6))
        ax1 = plt.subplot2grid((1, 4), (0, 0), aspect='equal')
        ax2 = plt.subplot2grid((1, 4), (0, 1), colspan=2)
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
        fplot, = ax2.plot(feigsx, feigsy, color='g', marker='+',
                          label='Attraction: Fiedler Eigenvalues')
        favplot, = ax2.plot(favx, favy, color='g',
                            label='Attraction: Average Fiedler Eigenvalue')
        feigox = []
        feigoy = []
        favox = []
        favoy = []
        foplot, = ax2.plot(feigox, feigoy, color='b', marker='+',
                           label='Orientation: Fiedler Eigenvalues')
        favoplot, = ax2.plot(favox, favoy, color='b',
                             label='Orientation: Average Fiedler Eigenvalues')

        feigrx = []
        feigry = []
        favrx = []
        favry = []
        frplot, = ax2.plot(feigrx, feigry, color='r', marker='+',
                           label='Repulsion: Fiedler Eigenvalues')
        favrplot, = ax2.plot(favrx, favry, color='r',
                             label='Repulsion: Average Fiedler Eigenvalues')

        feignx = []
        feigny = []
        favnx = []
        favny = []
        flplot, = ax2.plot(feignx, feigny, color='c', marker='+',
                           label='All Zones: Fiedler Eigenvalues')
        favlplot, = ax2.plot(favnx, favny, color='c',
                             label='All Zones: Average Fiedler Eigenvalues')

        feignx = []
        feigny = []
        favnx = []
        favny = []
        fkplot, = ax2.plot(feignx, feigny, color='m', marker='+',
                           label='K Nearest: Fiedler Eigenvalues')
        favkplot, = ax2.plot(favnx, favny, color='m',
                             label='K Nearest: Average Fiedler Eigenvalues')

        if saveloc is not None and not os.path.exists(saveloc):
            os.makedirs(saveloc)

        def update_fig(i):
            # Update time text
            time_text.set_text('t = %i' % (i + 1))

            # Update Agent positions
            fa, fo, fr, fa, fall = self.update()
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
            feigsy.append(fa)
            favy = sum(feigsy) / float(len(feigsy))
            fplot.set_data(feigsx, feigsy)
            favplot.set_data(favx, favy)
            favplot.set_label('Attraction: Average Fiedler Eigenvalue (%.2f)'
                              % favy)
            ax2.legend(loc=3, ncol=1, bbox_to_anchor=(1.05, 0))

            feigsoy = [1, 2]
            maxy = max(max(feigsy), max(feigsoy))
            maxyc = math.ceil(maxy)
            if maxyc - maxy < 0.2:
                maxyc += 1
            ax2.set_ylim((0, maxyc))
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


class FiedlerPlot:
    """
    Utility class to aid in plotting fiedler eigenvalues.
    """

    def __init__():
        pass
