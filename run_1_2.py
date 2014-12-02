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


def run_sim(k, n=50, m=10):
    board = Board(n, m, init_agents)
    A = board.nearest_adjacency(k)
    L = board.laplacian(A)
    return board.is_connected(L)


if __name__ == '__main__':
    m = 10
    n = 30
    reps = 100
    ks = np.arange(1, n + 1)
    data = {}
    for k in ks:
        data[k] = {}
        print k
        for rep in range(reps):
            rs = run_sim(k, n, m)
            x = 0
            if rs:
                x = 1
            data[k][rep] = x
    data = pd.DataFrame(data).transpose()
    data['Summary'] = data.sum(axis=1)
    data['Summary'] = data['Summary'] * 100 / float(reps)
    print data['Summary']
    data.to_csv('1_2_results.csv')
