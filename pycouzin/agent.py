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

        self.i = -1

        # TODO implement orientation

    def find_nearest_neighbors(self, k):
        """
        Finds and stores the indices of the k nearest neighbors to this agent
        at the current time step.

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
        df = df.head(k)

        self.nearest = df['i'].tolist()
