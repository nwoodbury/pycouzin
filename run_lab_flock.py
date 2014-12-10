"""
Shows swarm dynamics using couzin's equations.
"""
from pycouzin.topological_agent import TopologicalAgent
from pycouzin.couzinboard import CouzinBoard


def init_agents(board):
    agents = []
    for i in range(board.n):
        agent = TopologicalAgent(board)
        agents.append(agent)
    return agents


if __name__ == '__main__':
    m = 10
    n = 50

    rr = 5
    ro = 10
    ra = 20
    k = 5

    board = CouzinBoard(n, m, init_agents, rr, ro, ra, k, t=300)
    board.run(saveloc='out/flock_01')
    # board.run()
