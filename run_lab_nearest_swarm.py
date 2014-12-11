"""
Shows swarm dynamics using couzin's equations.
"""
from pycouzin.nearest_agent import NearestAgent
from pycouzin.couzinboard import CouzinBoard


def init_agents(board):
    agents = []
    for i in range(board.n):
        agent = NearestAgent(board)
        agents.append(agent)
    return agents


if __name__ == '__main__':
    m = 10
    n = 100

    rr = 1
    ro = 2
    ra = 16
    k = 5

    board = CouzinBoard(n, m, init_agents, rr, ro, ra, k, t=300)
    board.run(saveloc='out/swarm_01')
    # board.run()

