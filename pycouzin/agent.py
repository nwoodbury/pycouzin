

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
    """

    def __init__(self, board, p0=None, o0=None):
        self.board = board
        if p0 is None:
            self.p = self.board.get_random_point()
        else:
            self.p = p0

        # TODO implement orientation
