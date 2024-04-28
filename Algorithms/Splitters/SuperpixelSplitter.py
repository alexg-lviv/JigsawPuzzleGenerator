from Algorithms.Splitters.Splitter import Splitter
from Algorithms.Superpixels import Superpixels
from PIL import Image
from DataStructures.Segments.MultipointSegment import MultipointSegment
from typing import List
from DataStructures.Point import Point


def leave_unique(points: list[Point]) -> list[Point]:
    res = []
    for p in points:
        e = False
        for p1 in res:
            if p == p1:
                e = True
                break
        if not e: res.append(p)
    return res


class SuperpixelSplitter(Splitter):
    name: str = "SuperpixelSplitter"

    def __init__(self):
        super().__init__()

    def split(self,
              h: int,
              w: int,
              img: Image,
              num_superpixels: int = 40,
              **kwargs):
        e_returned = Superpixels.get_superpixels(img, num_superpixels)
        edges: List[MultipointSegment] = []
        tiles = {}

        for i in e_returned.values():
            for j in i.values():
                edges.append(j)
        for edge in edges:
            edge.add_terminal_vertex()
            edge.vertices = leave_unique(edge.vertices)
            edge.sort_points()
            edge.set_term_points()

        return edges, tiles
