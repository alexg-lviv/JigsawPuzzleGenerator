from DataStructures.Tiles.Tile import Tile
from DataStructures.Point import Point
from DataStructures.Segments.LineSegment import LineSegment
from typing import List


class VoronoiTile(Tile):
    def __init__(self,
                 point: Point,
                 area: float,
                 borders: List,
                 id_: int):
        self.id = id_
        self.area = area
        self.point = point

        self.edges: List[LineSegment] = [LineSegment(Point(*border.origin.xy),
                                                        Point(*border.target.xy),
                                                        self)
                                            for border in borders]
