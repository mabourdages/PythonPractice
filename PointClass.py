class Point(object):
    """ A representation of 2-dimensional points """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Point(self.x * other, self.y * other)

    def distance(self, coord):
        """ Not using Math Module for exercise """
        return ((self.x - coord.x)**2 + (self.y - coord.y)**2)**0.5

a=Point(3,4)
b=Point(2,7)

print a.distance(Point(0,0))
print round(a.distance(b),5)
