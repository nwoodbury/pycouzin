import numpy as np
import pandas as pd

from pycouzin.agent import Agent
from pycouzin.board import Board


def init_agents(board):
    agents = []
    for i in range(board.n):
        agent = Agent(board)
        agents.append(agent)
    return agents


def run_sim(r, n=50, m=10):
    board = Board(n, m, init_agents)
    A = board.radius_adjacency(r)
    L = board.laplacian(A)
    return board.is_connected(L)


if __name__ == '__main__':
    m = 10
    n = 30

    reps = 100
    step = 0.5
    radii = np.arange(0, 10 + step, step)
    data = {}
    for r in radii:
        rix = r / float(m)
        data[rix] = {}
        for rep in range(reps):
            rs = run_sim(r, n, m)
            x = 0
            if rs:
                x = 1
            data[rix][rep] = x
    data = pd.DataFrame(data).transpose()
    data['Summary'] = data.sum(axis=1)
    data['Summary'] = data['Summary'] * 100 / float(reps)
    print data['Summary']
    data.to_csv('1_1_results.csv')
