"""
Shows swarm dynamics using couzin's equations.
"""
from pycouzin.predprey_agent import PredatorAgent, PreyAgent
from pycouzin.couzinboard import CouzinBoard
import numpy as np
import math


def init_agents(board):
    # 4% predators
    num_preds = math.ceil(0.04 * board.n)

    agents = []
    for i in np.arange(0, num_preds):
        agent = PredatorAgent(board)
        agents.append(agent)

    for i in np.arange(num_preds, board.n):
        agent = PreyAgent(board)
        agents.append(agent)

    return agents


if __name__ == '__main__':
    m = 10
    n = 100

    rr = 1
    ro = 2
    ra = 23
    k = 5

    board = CouzinBoard(n, m, init_agents, rr, ro, ra, k, t=600)
    board.run(saveloc='out/predprey_01')
    # board.run()
