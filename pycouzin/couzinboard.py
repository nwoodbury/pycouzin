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

        # ax1.tick_params(axis='x', labelbottom='off')
        # ax1.tick_params(axis='y', labelleft='off')

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
        aplot = FiedlerPlot(ax2, 'Attraction', 'g')
        oplot = FiedlerPlot(ax2, 'Orientation', 'b')
        rplot = FiedlerPlot(ax2, 'Repulsion', 'r')
        lplot = FiedlerPlot(ax2, 'Attr + Or + Rep', 'c')
        kplot = FiedlerPlot(ax2, 'K Nearest', 'm')

        if saveloc is not None and not os.path.exists(saveloc):
            os.makedirs(saveloc)

        def update_fig(i):
            # Update time text
            print 'Running frame ', i
            time_text.set_text('t = %i' % (i + 1))

            # Update Agent positions
            fa, fo, fr, fk, fl = self.update()
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

            if length < 20:
                ticksize = 2
            elif length < 50:
                ticksize = 5
            else:
                ticksize = 10

            ax1.set_xticks(np.arange(math.ceil(minxs),
                                     math.ceil(minxs + length), ticksize))
            ax1.set_yticks(np.arange(math.ceil(minys),
                                     math.ceil(minys + length), ticksize))
            ax1.grid(True)

            # Update fiedler eigenvalues plot
            ma = aplot.update(i, fa)
            mo = oplot.update(i, fo)
            mr = rplot.update(i, fr)
            ml = lplot.update(i, fl)
            mk = kplot.update(i, fk)
            ax2.legend(loc=3, ncol=1, bbox_to_anchor=(1.05, 0))

            maxy = max(ma, mo, mr, ml, mk)
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
                                      repeat=False, interval=10)

        if saveloc:
            writer = animation.FFMpegWriter(fps=15, bitrate=4096)
            ani.save('%s/animation.mp4' % saveloc, writer=writer)
            plt.close()
        else:
            plt.show()


class FiedlerPlot:
    """
    Utility class to aid in plotting fiedler eigenvalues.
    """

    fied_name_fmt = '%s: Fiedler Eigenvalues'
    av_name_fmt = '%s: Average Fiedler Eigenvalue (%.2f)'

    def __init__(self, ax, prefix, color):
        self.prefix = prefix
        self.ex = []  # x values for fiedler eigenvalue plot
        self.ey = []  # y values for fiedler eigenvalue plot
        self.ax = []  # x values for average fiedler eigenvalue plot
        self.eplot, = ax.plot(self.ex, self.ey, color=color, marker='+',
                              label=self.fied_name_fmt % self.prefix)
        self.aplot, = ax.plot(self.ax, [], color=color,
                              label=self.av_name_fmt % (self.prefix, 0))

    def update(self, i, feig):
        """
        Updates this fiedler plot for a time step.

        Parameters
        ----------
        i : int
            The current timestep, 0 indexed.
        feig : number
            The current fiedler eigen value to plot.

        Returns
        -------
        mx : number
            The current maximum.
        """

        self.ex.append(i + 1)
        self.ax.append(i + 1)
        self.ey.append(feig)
        av = sum(self.ey) / float(len(self.ey))
        self.eplot.set_data(self.ex, self.ey)
        self.aplot.set_data(self.ax, av)
        self.aplot.set_label(self.av_name_fmt % (self.prefix, av))

        return max(self.ey)
