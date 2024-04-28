from DataStructures.Segments.Segment import Segment
from DataStructures.Segments.LineSegment import LineSegment
from DataStructures.Segments.AgregateSegment import AggregateSegment
from DataStructures.Point import Point
from typing import List
from random import randint


class HooksGenerator:
    name: str = "Hooks Generator"

    def __init__(self):
        self.avg_len = 0
        self.min_generation_prop = 0.4
        self.uniform_size = True

    def edges_info(self,
                   edges: List[Segment]):
        total: float = 0.
        for edge in edges:
            total += edge.length()
        total /= len(edges)
        self.avg_len = total

    @staticmethod
    def generate_hook(edge: Segment, **kwargs) -> Segment:
        raise NotImplementedError("implement generate hooks")

    @staticmethod
    def process_flipping(points: List[Point],
                         m: Point):
        if not randint(0, 1): return points, False
        return (Point.flip_points_180(points, m),
                True)

    @staticmethod
    def construct_new_edge(points: List[Point],
                           edge: Segment) -> AggregateSegment:
        segments: List[LineSegment] = []
        for i in range(1, len(points)):
            seg = LineSegment(points[i - 1], points[i], edge.tiles[0])
            seg.set_tiles(edge.tiles)

            segments.append(seg)

        return AggregateSegment(segments, edge.tiles)
