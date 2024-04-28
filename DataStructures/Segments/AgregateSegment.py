from typing import List

from PIL import ImageDraw

from DataStructures.Segments.Segment import Segment
from DataStructures.Tiles.Tile import Tile


class AggregateSegment(Segment):
    def __init__(self,
                 segments: List[Segment] = None,
                 tiles:    List[Tile] = None):
        self.segments = segments
        self.tiles: List[Tile] = tiles
        points = [(e.point_a, e.point_b) for e in [self.segments[0], self.segments[-1]]]
        r = []
        for p in points:
            r.extend(p)
        self.point_a = min(r)
        self.point_b = max(r)

    def set_tiles(self,
                  tiles: List[Tile] = None):
        self.tiles = tiles
        for segment in self.segments:
            segment.set_tiles(tiles)

    def draw(self,
             draw: ImageDraw):
        for segment in self.segments:
            segment.draw(draw)

    def length(self):
        return sum([segment.length() for segment in self.segments])
