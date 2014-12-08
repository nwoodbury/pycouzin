from pycouzin import Board


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
    """

    def adjacency(self, condition, state_update=None):
        """
        We only care about bi-directional adjacency now. See documentation
        for `bidirectional_adjacency()` in the parent class.
        """
        return self.bidirectional_adjacency(condition, state_update)
