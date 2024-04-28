from DataStructures.Point import Point
from DataStructures.Segments.Segment import Segment
from typing import List
from math import sqrt
from PIL import ImageDraw
from typing import Tuple
from DataStructures.Segments.AgregateSegment import AggregateSegment


class MultipointSegment(Segment):
    def __init__(self,
                 tile1: int,
                 tile2: int,
                 max_x, max_y,
                 points=None,
                 vertices: List[Point] = None,
                 point_a: Point = None,
                 point_b: Point = None):
        self.tile1 = tile1
        self.tile2 = tile2
        self.points: List[Point] = points if points else []
        self.vertices: List[Point] = vertices if vertices else []
        self.max_x: int = max_x - 1
        self.max_y: int = max_y - 1
        self.point_a: Point = point_a
        self.point_b: Point = point_b

    def get_points(self,
                   a: float,
                   b: float) -> Tuple[Point, Point]:
        p1 = self.points[int(a * len(self.points))]
        p2 = self.points[int((1 - b) * len(self.points))]
        return p1, p2

    def split(self,
              a: float,
              b: float,
              segments: List[Segment] = None) -> AggregateSegment:
        p1, p2 = self.get_points(a, b)

        if segments is None: segments = []
        segments = [
            MultipointSegment(tile1=self.tile1, tile2=self.tile2,
                              max_x=self.max_x, max_y=self.max_y,
                              points=self.points[:int(a * len(self.points))],
                              point_a=self.points[int(a * len(self.points))],
                              point_b=self.point_a),
            *segments,
            MultipointSegment(tile1=self.tile1, tile2=self.tile2,
                              max_x=self.max_x, max_y=self.max_y,
                              points=self.points[int((1 - b) * len(self.points)):],
                              point_a=self.points[int((1 - b) * len(self.points))],
                              point_b=self.point_b)
        ]
        return AggregateSegment(segments)

    def length(self):
        dx = (self.point_b.x - self.point_a.x) ** 2
        dy = (self.point_b.y - self.point_a.y) ** 2
        return sqrt(dx + dy)

    def draw(self,
             draw: ImageDraw):
        for point in self.points:
            draw.point(point.coords(), fill="black")

    def set_term_points(self):
        pass
        # self.point_a = self.vertices[0]
        # self.point_b = self.vertices[1]
        # self.point_a, self.point_b = (self.point_a, self.point_b) if self.point_a < self.point_b else (
        #     self.point_b, self.point_a)

    def add_terminal_vertex(self):
        for point in self.points:
            if point.x == 0 or point.y == 0 or point.x == self.max_x or point.y == self.max_y:
                self.vertices.append(point)

    def add_point(self, x: int, y: int):
        self.points.append(Point(x, y))

    def add_vertex_point(self, x: int, y: int):
        self.vertices.append(Point(x, y))

    def sort_points(self):
        self.points.sort()
