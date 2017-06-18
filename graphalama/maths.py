# -*- coding: utf-8 -*-
from math import sqrt


class V2(list):
    """ Represent a vector or a point in dimention 2. Support basic operations. """

    def __init__(self, x, y):

        super(V2, self).__init__([x, y])

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    def to_int(self):
        return V2(int(self.x), int(self.y))

    @property
    def norm(self):
        """
        Returns the norm of the vector.
        """
        return sqrt(self.squared_norm)

    @property
    def squared_norm(self):
        """
        Returns the squared norm of the vector.

        This could be useful to not calculate the norm, indeed, the sqrt of the square of coordinates,
            Ex : circle inequalities
        """
        return self.x ** 2 + self.y ** 2

    def __add__(self, other):
        return V2(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        return V2(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        if isinstance(other, (list, tuple)):
            if len(other) == 2:
                return V2(other[0] - self.x, other[1] - self.y)
            else:
                raise ValueError
        else:
            raise TypeError

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        return V2(self.x * other, self.y * other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return V2(self.x * other, self.y * other)
        else:
            raise TypeError

    def __imul__(self, other):
        return self * other

    def __truediv__(self, other):
        return V2(self.x / other, self.y / other)

    def __rdiv__(self, other):
        return self.__div__(other)

    def __idiv__(self, other):
        return self.__div__(other)


class Matrix22(list):
    def __init__(self, x1, x2, y1, y2):
        super(Matrix22, self).__init__([[x1, x2], [y1, y2]])

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            a = self.a * other
            b = self.b * other
            c = self.c * other
            d = self.d * other
            return Matrix22(a, b, c, d)
        elif isinstance(other, V2):
            return V2(self.a * other.x + self.b * other.y,
                      self.c * other.x + self.d * other.y)
        elif isinstance(other, Matrix22):
            raise NotImplementedError
        else:
            return other.__radd__(self)

    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            return self * other
        else:
            raise NotImplementedError

    def __div__(self, other):
        a = self.a / other
        b = self.b /other
        c = self.c / other
        d = self.d / other
        return Matrix22(a, b, c, d)

    @property
    def a(self):
        return self[0][0]

    @a.setter
    def a(self, value):
        self[0][0] = value

    @property
    def b(self):
        return self[0][1]

    @b.setter
    def b(self, value):
        self[0][1] = value

    @property
    def c(self):
        return self[1][0]

    @c.setter
    def c(self, value):
        self[1][0] = value

    @property
    def d(self):
        return self[1][1]

    @d.setter
    def d(self, value):
        self[1][1] = value

    @property
    def inverse(self):
        A = Matrix22(self.d, -self.b, -self.c, self.a)
        A *= 1/(self.a*self.d - self.b*self.c)
        return A

    @property
    def determinant(self):
        return self.a*self.d - self.b*self.c


class Matrix(list):
    """Not actually working"""
    def __init__(self, *args):
        """
        Matrix(list1, list2, list3...) --> Matrix
        all listX are a list of constant len. They are lines of the matrix
        """
        super(Matrix, self).__init__(*args)

    def __getitem__(self, col=None, lig=None):
        if col is None:  # select a line
            return list.__getitem__(self, lig)
        if lig is None:  # select a col
            return [self[col, x] for x in range(len(self))]
        return list.__getitem__(self, lig)[col]

    def __setitem__(self, col, lig, value):
        pass
