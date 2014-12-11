from pycouzin.vector import Vector2D


class Agent:
    """
    Defines an agent.

    Parameters
    ----------
    board : Board
        A reference to the board containing this agent.
    p0 : Vector2D or None
        The initial position of this agent, or None if it should be randomly
        generated. Defaults to None.
    o0 : Vector2D or None
        The initial orientation of this agent, or None if it should be randomly
        generated. Defaults to None.

    Attributes
    ----------
    board : Board
        A reference to the board containing this agent.
    p : Vector2D
        The current position of this agent.
    o : Vector2D
        The current orientation of this agent.
    i : int
        The index of this agent in the board's agent list.
    """

    def __init__(self, board, p0=None, o0=None):
        self.board = board
        if p0 is None:
            self.p = self.board.get_random_point()
        else:
            self.p = p0

        if o0 is None:
            self.o = self.board.get_random_point().normalize()
        else:
            self.o = o0

        self.i = -1
        self.speed = 0.5 # 0.5
        self.thetamax = 0.05 # 0.2

    def find_nearest_neighbors(self, max_k, min_k):
        """
        Finds and stores the indices of the max_k nearest neighbors to this
        agent and excludes the min_k nearest neighbors at the current time
        step.

        Parameters
        ----------
        k : int
        """
        def distance(row):
            po = Vector2D(row['x'], row['y'])
            return self.p.distance_to(po)

        df = self.board.agent_df()
        df = df[df['i'] != self.i]  # Ignore present agent
        df['distances'] = df.apply(distance, axis=1)
        df = df.sort('distances', ascending=True)
        df = df.head(max_k)
        df = df.tail(max_k - min_k)

        self.nearest = df['i'].tolist()

    def update(self, a_r, a_o, a_a, a_k, agents):
        """
        Updates this agent's position. Must be overridden in a subclass.

        Parameters
        ----------
        a_r : numpy.array
            An nxn adjacency matrix for radius of repulsion.
        a_o : numpy.array
            An nxn adjacency matrix for radius of orientation.
        a_a : numpy.array
            An nxn adjacency matrix for radius of attraction.
        a_k : numpy.array
            An nxn adjacency matrix for k nearest neighbors.
        agents : list of Agent
            A list of agents which could be useful for other dynamics.
        """
        raise NotImplemented()

    def get_adjacent_agents(self, a, agents):
        """
        Returns a list of agents adjacent to this agent defined by adjacency
        matrix a.
        """
        adj_agents = []
        for j in range(len(agents)):
            if j == self.i:
                continue
            if a[j, self.i] == 1:
                adj_agents.append(agents[j])
        return adj_agents
