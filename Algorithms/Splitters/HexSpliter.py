from Algorithms.Splitters.Splitter import Splitter
from DataStructures.Tiles.HexTile import HexTile, RombTile
from DataStructures.Tiles.Tile import Tile
from DataStructures.Point import Point
from DataStructures.Segments.Segment import Segment

from math import sqrt
from typing import List


class HexSplitter(Splitter):
    name: str = "HexSplitter"

    def __init__(self):
        super().__init__()

    def create_perfect_tiling(self,
                              tiles: List[Tile],
                              edge_len: int,
                              h: int,
                              w: int) -> List[Tile]:
        tile_id = 0
        hex_h = int(sqrt((edge_len ** 2) * 3 / 4))
        for i in range(0, h + edge_len, hex_h * 2):
            for j in range(0, w + edge_len, edge_len * 3):
                tiles.append(HexTile(Point(j, i),
                                     edge_len,
                                     w, h,
                                     tile_id))
                tile_id += 1
        for i in range(hex_h, h + edge_len, hex_h * 2):
            for j in range(int(edge_len * 1.5), w + edge_len, edge_len * 3):
                tiles.append(HexTile(Point(j, i),
                                     edge_len,
                                     w, h,
                                     tile_id))
                tile_id += 1
        return tiles

    def create_offset_tiling(self,
                             tiles: List[Tile],
                             edge_len: int,
                             h: int,
                             w: int) -> List[Tile]:
        tile_id = 0
        hex_h = int(sqrt((edge_len ** 2) * 3 / 4))
        for i in range(0, h + edge_len, hex_h * 2):
            for j in range(0, w + edge_len, edge_len * 2):
                tiles.append(HexTile(Point(j, i),
                                     edge_len,
                                     w, h,
                                     tile_id))
                tile_id += 1
        for i in range(hex_h, h + edge_len, hex_h * 2):
            for j in range(edge_len, w + edge_len, edge_len * 2):
                tiles.append(RombTile(Point(j, i),
                                      edge_len,
                                      w, h,
                                      tile_id))
                tile_id += 1
        return tiles

    def split(self,
              h: int = 1000,
              w: int = 1000,
              edge_len: int = 150,
              rand: bool = False,
              perfect_tiling: bool = True,
              **kwargs) -> tuple[list, list]:
        edges: List[Segment] = []
        tiles: List[Tile] = []

        if perfect_tiling:
            tiles = self.create_perfect_tiling(tiles,
                                               edge_len=edge_len,
                                               h=h,
                                               w=w)
        else:
            tiles = self.create_offset_tiling(tiles,
                                              edge_len=edge_len,
                                              h=h,
                                              w=w)

        for tile in tiles:
            edges.extend(tile.get_edges())

        edges = list(set(edges))
        for edge in edges:
            edge.process_neighbours()

        return edges, tiles
