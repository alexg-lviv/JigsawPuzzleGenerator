from DataStructures.Tiles.Tile import Tile
from DataStructures.Segments.LineSegment import LineSegment
from DataStructures.Point import Point


class RectTile(Tile):
    def __init__(self,
                 left_top: Point,
                 right_bottom: Point,
                 max_x, max_y,
                 id_: int = 0):
        self.id = id_
        self.left_top = left_top
        right_top = Point(right_bottom.x, left_top.y)
        left_bottom = Point(left_top.x, right_bottom.y)
        self.edges = [LineSegment(left_top, right_top, self).clamp(max_x, max_y),
                      LineSegment(right_top, right_bottom, self).clamp(max_x, max_y),
                      LineSegment(right_bottom, left_bottom, self).clamp(max_x, max_y),
                      LineSegment(left_top, left_bottom, self).clamp(max_x, max_y)]
        self.neighbours = []
