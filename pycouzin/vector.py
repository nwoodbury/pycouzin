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

    def __add__(self, other):
        """
        Vector addition.

        Example
        -------
        v1 = Vector2D(2, 3)
        v2 = Vector2D(3, 4)
        v3 = v1 + v2

        v3.x == 5
        v3.y == 7
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Vector subtraction.
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """
        Scalar multiplication
        """
        return Vector2D(self.x * other, self.y * other)

    def __str__(self):
        return '[%.2f, %.2f]' % (self.x, self.y)

    def normalize(self):
        """
        Returns a copy of this vector, normalized.
        """
        zero = Vector2D(0, 0)
        l = float(zero.distance_to(self))
        return Vector2D(self.x / l, self.y / l)
