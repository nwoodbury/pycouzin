from pycouzin.dyn_board import DynBoard
from pycouzin.agent import Agent
from pycouzin.metric import Metric
from pycouzin.vector import Vector2D


def init_agents(board):
    agents = []
    for i in range(board.n):
        agent = Agent(board)
        agents.append(agent)
    return agents

def test_agents(board):
    agents = []
    agent1 = Agent(board)
    agent1.p = Vector2D(0, 0)
    agents.append(agent1)
    agent2 = Agent(board)
    agent2.p = Vector2D(0.25, 0.25)
    agents.append(agent2)
    return agents

if __name__ == '__main__':
    n = 45
    m = 10
    reps = 100
    rep_dist = 5
    min_att_dist = 5.1
    max_att_dist = 8
    board = DynBoard(n, m, init_agents, rep_dist, max_att_dist, min_att_dist, Metric.radius)
    file = open('2_1_data.csv','w')
    for t in range(reps):
        fied = board.get_comb_fied()
        rep_fied, att_fied = board.get_fieds()
        avg_conn = board.get_avg_conn()
        x, y = board.get_state_vectors()
        file.write('{},{},{},{}\n'.format(fied, rep_fied, att_fied, avg_conn))

        board.update()

    """for i in range(len(x)):
            file.write('{},{}\n'.format(x[i], y[i]))"""
    file.close()
