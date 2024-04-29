from typing import List, Tuple, Self

from DataStructures.Point import Point
from DataStructures.Tiles.Tile import Tile
from DataStructures.Segments.Segment import Segment
from DataStructures.Segments.AgregateSegment import AggregateSegment
from math import sqrt
from PIL import ImageDraw


class LineSegment(Segment):
    segments = dict()

    def __new__(cls,
                point_a: Point = None,
                point_b: Point = None,
                tile: Tile = None):
        if tile and LineSegment.segments.get((point_a, point_b)):
            instance: cls = LineSegment.segments[(point_a, point_b)]
            instance.add_tile(tile)
            return instance
        elif tile and LineSegment.segments.get((point_b, point_a)):
            instance: cls = LineSegment.segments[(point_b, point_a)]
            instance.add_tile(tile)
            return instance
        else:
            instance = super().__new__(cls)
            return instance

    @classmethod
    def clear_segments(cls):
        cls.segments = dict()

    def __init__(self,
                 point_a: Point = None,
                 point_b: Point = None,
                 tile: Tile = None):
        if tile and self._check_if_exists(point_a, point_b): return

        self.point_a, self.point_b = self._swap_points(point_a, point_b)
        self.tiles: List[Tile] = []
        self._add_first_tile(tile)

        if self.point_b.x - self.point_a.x != 0:
            self.slope = (self.point_b.y - self.point_a.y) / (self.point_b.x - self.point_a.x)
            self.is_vert = False
        else:
            self.slope = 1
            self.is_vert = True
        self.b = self.point_a.y - self.point_a.x * self.slope

    def set_tiles(self, tiles: List[Tile] = None):
        self.tiles = tiles

    def draw(self,
             draw: ImageDraw):
        draw.line([self.point_a.coords(),
                   self.point_b.coords()],
                  width=1,
                  fill="black")

    def length(self):
        dx = (self.point_b.x - self.point_a.x) ** 2
        dy = (self.point_b.y - self.point_a.y) ** 2
        return sqrt(dx + dy)

    def set_points(self,
                   point_a: Point = None,
                   point_b: Point = None):
        if point_a:
            self.point_a = point_a
        if point_b:
            self.point_b = point_b

    def get_points(self,
                   a: float,
                   b: float) -> Tuple[Point, Point]:
        d = self.point_b - self.point_a
        p1 = self.point_a + d * a
        p2 = self.point_b - d * b
        return p1, p2

    def split(self,
              a: float,
              b: float,
              segments: List[Segment] = None) -> AggregateSegment:
        d = self.point_b - self.point_a
        p1 = self.point_a + d * a
        p2 = self.point_b - d * b

        if segments is None: segments = []
        segments = [
            LineSegment(self.point_a, p1),
            *segments,
            LineSegment(p2, self.point_b)
        ]
        return AggregateSegment(segments)

    def intersection_horiz(self,
                           c: int,
                           px: int = 0) -> Point:
        if self.is_vert:
            return Point(px, c)
        return Point((c - self.b) / self.slope, c)

    def intersection_vert(self,
                          d: int) -> Point:
        return Point(d, d * self.slope + self.b)

    def clamp(self,
              x_max: int,
              y_max: int) -> Self:
        points = []
        for p in (self.point_a, self.point_b):
            if p.x < 0 and not self.is_vert:
                p = self.intersection_vert(0)
            if p.x > x_max and not self.is_vert:
                p = self.intersection_vert(x_max)
            if p.y < 0 and self.slope:
                p = self.intersection_horiz(0,
                                            p.x)
            if p.y > y_max and self.slope:
                p = self.intersection_horiz(y_max,
                                            p.x)
            points.append(p)
        self.point_a, self.point_b = points
        return self

    def process_neighbours(self) -> None:
        for tile in self.tiles:
            tile.add_neighbours(self.tiles)

    def add_tile(self,
                 tile: Tile) -> None:
        self.tiles.append(tile)

    @staticmethod
    def _is_valid_other(other) -> bool:
        return hasattr(other, 'point_a') and hasattr(other, 'point_b')

    def __eq__(self, other):
        return (self._is_valid_other(other)
                and ((other.point_a == self.point_a and other.point_b == self.point_b)
                     or other.point_a == self.point_b and other.point_b == self.point_a))

    def __hash__(self):
        return self.point_a.__hash__() + self.point_b.__hash__()

    def __str__(self):
        return f"{self.point_a} -> {self.point_b}"

    def __repr__(self):
        return f"{self.point_a} -> {self.point_b}"

    @staticmethod
    def _check_if_exists(point_a: Point,
                         point_b: Point) -> bool:
        return (LineSegment.segments.get((point_a, point_b))
                or LineSegment.segments.get((point_b, point_a)))

    @staticmethod
    def _swap_points(point_a: Point,
                     point_b: Point) -> Tuple[Point, Point]:
        return (point_a, point_b) if point_a < point_b else (point_b, point_a)

    def _add_first_tile(self,
                        tile: Tile = None):
        if tile:
            self.tiles.append(tile)
            LineSegment.segments[(self.point_a, self.point_b)] = self


if __name__ == "__main__":
    l1 = LineSegment(Point(0, 0), Point(10, 10))
    l2 = LineSegment(Point(0, 0), Point(10, 10))
    l3 = LineSegment(Point(1, 2), Point(10, 10))
    print(l1, l2, l3)
    print(Point(0, 0).__hash__() + Point(10, 10).__hash__())
    print(Point(10, 10).__hash__() + Point(0, 0).__hash__())
