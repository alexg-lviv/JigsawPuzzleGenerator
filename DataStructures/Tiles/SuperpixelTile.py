from DataStructures.Tiles.Tile import Tile
from typing import List
from DataStructures.Segments.LineSegment import LineSegment
from DataStructures.Point import Point
import shapely.geometry as g


class SuperpixelTile(Tile):
    def __init__(self,
                 id_: int):
        self.edges: List[LineSegment] = []
        self.neighbours = []
        self.id = id_
        self.points: List[Point] = []

    def add_point(self,
                  point: Point):
        self.points.append(point)

    def create_polygon(self):
        c = [point.coords() for point in self.points]
        p = g.MultiPoint(c).convex_hull
        self.points = [Point(*pt) for pt in p.exterior.coords]
        for i in range(1, len(self.points)):
            self.edges.append(LineSegment(self.points[i - 1],
                                          self.points[i],
                                          self))
        self.edges.append(LineSegment(self.points[0],
                                      self.points[-1],
                                      self))
