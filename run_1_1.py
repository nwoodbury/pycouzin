from pycouzin.agent import Agent
from pycouzin.board import Board


def init_agents(board):
    agents = []
    for i in range(board.n):
        agent = Agent(board)
        agents.append(agent)
    return agents


if __name__ == '__main__':
    board = Board(5, 10, init_agents)
    adjacency = board.radius_adjacency(10)
    print adjacency
    print board.laplacian(adjacency)
