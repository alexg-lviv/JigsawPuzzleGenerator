from typing import List

from DataStructures.Tiles.Tile import Tile
from DataStructures.Segments.LineSegment import LineSegment
from DataStructures.Point import Point
from math import sqrt


class HexTile(Tile):
    def create_hex_edges(self,
                         center: Point,
                         edge_len: int,
                         max_x: int,
                         max_y: int,
                         ):
        xs = edge_len ** 2
        h = int(sqrt(xs * 3 / 4))
        x2 = edge_len / 2

        p1 = center + Point(-x2, -h)
        p2 = center + Point(x2, -h)
        p3 = center + Point(edge_len, 0)
        p4 = center + Point(x2, h)
        p5 = center + Point(-x2, h)
        p6 = center + Point(-edge_len, 0)

        return [
            LineSegment(p1, p2, self).clamp(max_x, max_y),
            LineSegment(p2, p3, self).clamp(max_x, max_y),
            LineSegment(p3, p4, self).clamp(max_x, max_y),
            LineSegment(p4, p5, self).clamp(max_x, max_y),
            LineSegment(p5, p6, self).clamp(max_x, max_y),
            LineSegment(p6, p1, self).clamp(max_x, max_y)
        ]

    def __init__(self,
                 center: Point,
                 edge_len: int,
                 max_x: int,
                 max_y: int,
                 id_: int = 0):
        self.id = id_
        self.edge_len = edge_len
        self.center = center

        self.max_x = max_x
        self.max_y = max_y

        self.edges = self.create_hex_edges(center,
                                           edge_len,
                                           max_x, max_y)
        self.neighbours: List[Tile] = []


class RombTile(Tile):
    def __init__(self,
                 center: Point,
                 edge_len: int,
                 max_x: int,
                 max_y: int,
                 id_: int = 0):
        self.id = id_
        self.center = center
        self.edge_len = edge_len

        xs = edge_len ** 2
        h = int(sqrt(xs * 3 / 4))

        points: List[Point] = [center + Point(-edge_len / 2, 0),
                               center + Point(0, -h),
                               center + Point(edge_len / 2, 0),
                               center + Point(0, h)]

        self.edges: List[LineSegment] = [LineSegment(points[0], points[1], self).clamp(max_x, max_y),
                                         LineSegment(points[1], points[2], self).clamp(max_x, max_y),
                                         LineSegment(points[2], points[3], self).clamp(max_x, max_y),
                                         LineSegment(points[0], points[3], self).clamp(max_x, max_y)]
        self.neighbours: List[Tile] = []
