import functools
from math import cos, sin, sqrt
from typing import Any, Self, List
from numpy import pi
from PIL import ImageDraw


@functools.total_ordering
class Point:
    def __init__(self,
                 x: float,
                 y: float):
        self.x = x
        self.y = y

    def draw(self,
             draw: ImageDraw):
        draw.ellipse((self.coords(),
                      (self + Point(10, 10)).coords()),
                     fill="red")

    def dist(self, other: Self):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def coords(self, toint = False) -> tuple[float, float]:
        if toint:
            return int(self.x), int(self.y)
        return self.x, self.y

    @staticmethod
    def _is_valid_other(other) -> bool:
        return (hasattr(other, 'x')
                and hasattr(other, 'y'))

    def rotate(self, offset, angle) -> Self:
        p = self - offset
        res = Point(int(p.x * cos(angle) - p.y * sin(angle)),
                    int(p.x * sin(angle) + p.y * cos(angle)))
        res += offset
        return res

    @staticmethod
    def float_eq(first, second):
        return True if abs(first - second) < 4 else False

    def mid_point(self,
                  other: Self) -> Self:
        return (other - self) / 2.0 + self

    def __eq__(self, other) -> bool:
        return (Point._is_valid_other(other)
                and (self.float_eq(self.x, other.x) and self.float_eq(self.y, other.y)))

    def __lt__(self, other) -> bool:
        if not Point._is_valid_other(other): return NotImplemented
        if self.x < other.x: return True
        if self.x == other.x and self.y < other.y: return True
        return False

    def __hash__(self):
        x = int(self.x)
        y = int(self.y)
        return ((x + y) * int((x + y + 1) / 2)) + y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def __mul__(self, other) -> Self:
        if type(other) is float:
            return Point(self.x * other, self.y * other)
        return NotImplemented

    def __truediv__(self, other: Any) -> Self:
        if type(other) is float or type(other) is int:
            return Point(self.x / other, self.y / other)
        return NotImplemented

    def __sub__(self, other) -> Self:
        if not Point._is_valid_other(other): return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other) -> Self:
        if not Point._is_valid_other(other): return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    @classmethod
    def rotate_multiple_points(cls,
                               points: List[Self],
                               offset: Self,
                               angle: float) -> List[Self]:
        return [point.rotate(offset, angle) for point in points]

    @classmethod
    def rotate_multiple_curves(cls,
                               curves: List[List[Self]],
                               offset: Self,
                               angle: float) -> List[List[Self]]:
        return [cls.rotate_multiple_points(points, offset, angle) for points in curves]

    @classmethod
    def flip_points_180(cls,
                        points: List[Self],
                        offset: Self):
        return cls.rotate_multiple_points(points, offset, pi)

    @classmethod
    def set_boundaries(cls,
                       left_top: Self,
                       right_bottom: Self):
        cls.min_x, cls.min_y = left_top.coords()
        cls.max_x, cls.max_y = right_bottom.coords()


class ApproxPoint(Point):
    points = []

    @classmethod
    def _check_exists(cls,
                      x: float,
                      y: float,
                      tolerance: float = 5) -> Self:
        for p in cls.points:
            if abs(x - p.x) < tolerance and abs(y - p.y) < tolerance:
                return p
        return None

    def __new__(cls,
                x: float,
                y: float,
                tolerance: float = 20):
        instance = cls._check_exists(x, y, tolerance)
        if instance:
            return instance
        else:
            instance = super().__new__(cls)
            return instance

    def __init__(self,
                 x: float,
                 y: float,
                 tolerance: float = 20):
        if self._check_exists(x, y, tolerance): return
        super().__init__(x, y)
        self.points.append(self)
