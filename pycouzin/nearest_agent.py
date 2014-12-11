from pycouzin.topological_agent import TopologicalAgent


class NearestAgent (TopologicalAgent):

    def get_desired_direction(self, a_r, a_o, a_a, a_k, agents):
        """
        Computes the desired direction based on k nearest neighbors
        """
        in_repulsion = []
        in_orientation = []
        in_attraction = []
        j = self.i
        for agent in self.nearest:
            d = self.p.distance_to(agent.p)
            if d < self.board.rr:
                in_repulsion.append(agent)
            elif d < self.board.ro:
                in_orientation.append(agent)
            else:
                in_attraction.append(agent)

        return self.get_direction_from_zones(in_repulsion, in_orientation, in_attraction)
