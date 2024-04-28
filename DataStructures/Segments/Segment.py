from DataStructures.Point import Point
from DataStructures.Tiles import Tile

from typing import List, Self
from PIL import ImageDraw


class Segment:
    segments = dict()
    point_a: Point = None
    point_b: Point = None
    tiles: List[Tile] = []

    def dist_to_bounds(self, max_x, max_y) -> float:
        dists = []
        for point in [self.point_a, self.point_b]:
            dists.extend([point.x, max_x - point.x, point.y, max_y - point.y])
        return min(dists)

    def length(self):
        raise NotImplementedError("Length not implemented")

    def split(self,
              a: float,
              b: float,
              segments: List[Self] = None) -> Self:
        raise NotImplementedError("Split not implemented")

    def draw(self,
             draw: ImageDraw):
        raise NotImplementedError("Draw not implemented")

    def set_tiles(self,
                  tiles: List[Tile]):
        raise NotImplementedError("Set tiles not implemented")

    def process_neighbours(self) -> None:
        raise NotImplementedError("Process neighbours not implemented")
