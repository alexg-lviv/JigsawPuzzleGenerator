from DataStructures.Segments.Segment import Segment
from DataStructures.Point import Point
from DataStructures.Tiles.Tile import Tile
from typing import List
from PIL import ImageDraw
from Algorithms.Bezier import Bezier
from math import sqrt

class BezierSegment(Segment):
    def __init__(self,
                 point_a: Point = None,
                 point_b: Point = None,
                 points:  List[Point] = None,
                 tiles:   List[Tile] = None,
                 tile:    Tile = None):
        self.point_a: Point = point_a
        self.point_b: Point = point_b
        if points:  self.points: List[Point] = points
        if tiles:   self.tiles:  List[Tile] = tiles
        elif tile:  self.tiles:  List[Tile] = [tile]
        else:       self.tiles:  List[Tile] = []

    def draw(self,
             draw: ImageDraw) -> None:
        Bezier.draw(draw,
                    self.points)

    def length(self):
        dx = (self.point_b.x - self.point_a.x) ** 2
        dy = (self.point_b.y - self.point_a.y) ** 2
        return sqrt(dx + dy)


if __name__ == "__main__":
    a = [1, 2, 3]
    c = []
    b = [5, *a, *c, 10]
    print(b)
