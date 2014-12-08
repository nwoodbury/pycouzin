from pycouzin.board import Board
import numpy as np
from pycouzin.metric import Metric
from pycouzin.vector import Vector2D


class DynBoard(Board):

    def __init__(self, n, m, agent_init, rep_rad, max_att_rad, min_att_rad, att_met=Metric.radius):
        Board.__init__(self, n, m, agent_init)
        self.rep_rad = rep_rad
        self.max_att_rad = max_att_rad
        self.min_att_rad = min_att_rad
        self.att_metric = att_met
        self.update_att_lap()
        self.update_rep_lap()

    def update(self):
        """
        updates the board according to the following dynamics:
        x_dot = -La*x + Lr*x + noise
        """
        dt = 0.1
        x, y = self.get_state_vectors()
        self.update_rep_lap()
        self.update_att_lap()
        noise = np.random.normal(0, 0.001, (self.n, 2))
        vec_x = np.matrix(x).getT()
        vec_y = np.matrix(y).getT()
        vec_noise_x = np.matrix(noise[:, 0]).getT()
        vec_noise_y = np.matrix(noise[:, 1]).getT()
        vec_x = ((self.rep_lap - self.att_lap)*vec_x + vec_noise_x) * dt + vec_x
        vec_y = ((self.rep_lap - self.att_lap)*vec_y + vec_noise_y) * dt + vec_y
        vec_x = vec_x.getT()
        vec_y = vec_y.getT()
        list_x = vec_x.tolist()[0]
        list_y = vec_y.tolist()[0]
        #self.print_update()
        self.set_agent_pos(list_x, list_y)

    def print_update(self):
        print '******************'
        for i in range(self.n):
            att_row_sum = 0
            rep_row_sum = 0
            for j in range(self.n):
                if i != j:
                    att_row_sum = att_row_sum + abs(self.att_lap[i][j])
                    rep_row_sum = rep_row_sum + abs(self.rep_lap[i][j])
            print 'Agent {}: {} in repulsion zone and {} in attraction zone'.format(i, att_row_sum, rep_row_sum)

    def update_rep_lap(self):
        adj = self.radius_adjacency(self.rep_rad)
        self.rep_lap = self.laplacian(adj)

    def update_att_lap(self):
        if self.att_metric == Metric.radius:
            adj = self.radius_adjacency(self.max_att_rad, self.min_att_rad)
            self.att_lap = self.laplacian(adj)
        else:
            adj = self.nearest_adjacency(self.max_att_rad, self.min_att_rad)
            self.att_lap = self.laplacian(adj)

    def get_fieds(self):
        return self.get_fied(self.rep_lap), self.get_fied(self.att_lap)

    def get_comb_fied(self):
        """
        Returns
        -------
         the Fiedler eigenvalue for Lr - La
        """
        return self.get_fied(self.rep_lap - self.att_lap)

    def get_avg_conn(self):
        """
        Returns
        -------
         the average connectivity for Lr - La, which corresponds to the
         average
        """
        l = self.rep_lap - self.att_lap
        tot = 0
        for i in range(self.n):
            for j in range(self.n):
                if i != j and l[i][j] != 0:
                    tot = tot + 1
        return tot/self.n

    def get_state_vectors(self):
        """
        returns x and y vectors indicating the position of each agent

        Returns
        -------
         x: a vector that contains the x-coordinate of each agent's position
         y: a vector that contains the y-coordinate of each agent's position
        """
        x = []
        y = []
        for agent in self.agents:
            pos = agent.p
            x.append(pos.x)
            y.append(pos.y)
        return x, y

    def set_agent_pos(self, x, y):
        """
        updates the agent positions based on the given x and y vectors

        Parameters
        ----------
        x: the x-coordinate of the new agent positions
        y: the y-coordinate of the new agent positions
        """
        for i in range(len(x)):
            agent = self.agents[i]
            agent.p = Vector2D(x[i], y[i])


