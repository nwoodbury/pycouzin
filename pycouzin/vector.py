import math


class Vector2D:
    """
    Represents a 2D vector.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        """
        Computes the distance between this vector and `other` vector.

        Parameters
        ----------
        other : Vector2D

        Returns
        -------
        distance : number
        """
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
