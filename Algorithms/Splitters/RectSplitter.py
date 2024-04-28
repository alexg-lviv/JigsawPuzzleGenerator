from Algorithms.Splitters.Splitter import Splitter
from DataStructures.Tiles.RectTile import RectTile
from DataStructures.Point import Point
from DataStructures.Segments.LineSegment import LineSegment

from typing import Tuple, List


class RectSplitter(Splitter):
    name: str = "RectSplitter"

    def __init__(self):
        super().__init__()

    def split(self,
              h: int = 1000,
              w: int = 1000,
              tile_h: int = 500,
              tile_w: int = 500,
              **kwargs) -> Tuple[List, List]:
        edges: List[LineSegment] = []
        tiles: List[RectTile] = []

        tile_id = 0

        for i in range(tile_h, h + tile_h, tile_h):
            for j in range(tile_w, w + tile_w, tile_w):
                tiles.append(RectTile(Point(j - tile_w, i - tile_h),
                                      Point(j, i),
                                      w, h,
                                      tile_id))
                tile_id += 1

        for tile in tiles:
            edges.extend(tile.get_edges())

        edges = list(set(edges))
        for edge in edges:
            edge.process_neighbours()

        return edges, tiles
