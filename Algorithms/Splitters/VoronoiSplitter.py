from typing import Tuple, List

from Algorithms.Splitters.Splitter import Splitter
from DataStructures.Segments.LineSegment import LineSegment
from DataStructures.Tiles.VoronoiTile import VoronoiTile
from DataStructures.Point import Point

import foronoi
from foronoi.algorithm import Algorithm

from random import randint


class VoronoiSplitter(Splitter):
    name: str = "VoronoiSplitter"

    def __init__(self):
        super().__init__()

    @staticmethod
    def _calculate_centroid(vertices: List[foronoi.graph.Vertex]) -> tuple[float, float]:
        points = [Point(*vertex.xy) for vertex in vertices]
        p = Point(0, 0)
        for point in points:
            p += point
        p /= len(points)
        return int(p.coords()[0]), int(p.coords()[1])

    def split(self,
              h: int = 1000,
              w: int = 1000,
              num_points: int = 30,
              lloyds_iterations: int = 30,
              **kwargs) -> Tuple[List, List]:
        edges: List[LineSegment] = []
        tiles: List[VoronoiTile] = []
        tile_id = 0

        alg = Algorithm(bounding_poly=foronoi.Polygon([(0, 0), (w, 0), (w, h), (0, h)]))
        for _ in range(lloyds_iterations):
            points: List = []
            if not alg.sites:
                for i in range(num_points):
                    points.append((randint(0, w), randint(0, h)))
            else:
                for site in alg.sites:
                    points.append(self._calculate_centroid(site.vertices()))
            alg = Algorithm(bounding_poly=foronoi.Polygon([(0, 0), (w, 0), (w, h), (0, h)]))
            alg.create_diagram(points)

        for site in alg.sites:
            tiles.append(VoronoiTile(Point(site.x, site.y),
                                     site.area(),
                                     site.borders(),
                                     tile_id))
            tile_id += 1

        for tile in tiles:
            edges.extend(tile.get_edges())

        edges = list(set(edges))
        for edge in edges:
            edge.process_neighbours()

        return edges, tiles
