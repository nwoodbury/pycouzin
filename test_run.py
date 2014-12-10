from pycouzin.topological_agent import TopologicalAgent
from pycouzin.couzinboard import CouzinBoard
from pycouzin.vector import Vector2D


def agent_r(board):
    #tests repulsion zone

    #main agent
    agents = []
    p0 = Vector2D(0, 0)
    o0 = Vector2D(-0.951, -0.309)
    agent = TopologicalAgent(board, p0, o0)
    agents.append(agent)

    #agent in zor of main agent
    p0 = Vector2D(2, 2)
    o0 = Vector2D(-1, 1)
    agent = TopologicalAgent(board, p0, o0)
    agents.append(agent)

    #agent in zoo of main agent
    p0 = Vector2D(-5, 5)
    o0 = Vector2D(-1, 1)
    agent = TopologicalAgent(board, p0, o0)
    agents.append(agent)

    #agent in zoa of main agent
    p0 = Vector2D(8, -8)
    o0 = Vector2D(0, 1)
    agent = TopologicalAgent(board, p0, o0)
    agents.append(agent)

    return agents

if __name__ == '__main__':
    n = 4
    m = 10
    rr = 5
    ro = 10
    ra = 15
    k = 5

    board = CouzinBoard(n, m, agent_r, rr, ro, ra, k)
    agent = board.agents[0]
    d = agent.reg_ang_v(Vector2D(-0.951, 0.309))
    print "d: "
    print(d)
    board.update()
    assert agent.p == Vector2D(-0.1, -0.1)



