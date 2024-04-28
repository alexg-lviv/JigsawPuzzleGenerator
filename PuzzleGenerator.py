import random
from typing import List

from PIL import Image, ImageDraw
from Algorithms.Splitters.Splitter import Splitter
from Algorithms.HooksGenerators.HooksGenerator import HooksGenerator
from DataStructures.Point import Point
from DataStructures.Tiles import Tile
from DataStructures.Segments.Segment import Segment
from DataStructures.Segments.LineSegment import LineSegment
from loguru import logger

from DataStructures.Tiles.Shape import Shape


class PuzzleGenerator:
    def __init__(self,
                 image: Image,
                 splitter: Splitter = None,
                 hooks_generator: HooksGenerator = None,
                 holds_drop_rate: float = 0.0):
        self.img: Image = image
        self.tiles: List[Tile] = []
        self.edges: List[Segment] = []
        self.connections = None
        self.splitter: Splitter = splitter
        self.hooks_generator: HooksGenerator = hooks_generator
        self.w, self.h = self.img.size
        self.holds_drop_rate = holds_drop_rate
        self.average_len = 0

    def set_image(self, image: Image):
        self.img = image

    def generate_splitting(self,
                           tile_h: int = 0,
                           tile_w: int = 0,
                           edge_size: int = 0,
                           perfect_tiling: bool = True,
                           lloyds_iter: int = 20,
                           num_tiles: int = 20,
                           num_superpixels:int =20):
        logger.info(f"generating splitting on image using {self.splitter.name}")
        self.edges, self.tiles = self.splitter.split(h=self.h,
                                                     w=self.w,
                                                     tile_h=tile_h,
                                                     tile_w=tile_w,
                                                     img=self.img,
                                                     edge_len=edge_size,
                                                     perfect_tiling=perfect_tiling,
                                                     lloyds_iterations=lloyds_iter,
                                                     num_points=num_tiles,
                                                     num_superpixels=num_superpixels)
        logger.info(f"Generated {len(self.edges)} edges and {len(self.tiles)} tiles")
        return self

    def generate_hooks(self,
                       hooks_base: float = 0.0,
                       first_h: float = 0.0,
                       second_h: float = 0.0,
                       wings_dist: float = 0.0,
                       same_wings: bool = True,
                       drop_holds: float = 0.0,
                       hook_base_point: float = 0.0,
                       side_control_points_range: float = 0.0,
                       hook_wideness_range: float = 0.0):
        logger.info(f"hooks_base: {hooks_base}, first_h: {first_h}, second_h: {second_h}, wings_dist: {wings_dist}, same_wings: {same_wings}, drop_holds: {drop_holds}")
        if self.splitter.name == "SuperpixelSplitter": return self
        edges: List[Segment] = []
        logger.info(f"generating hooks for {len(self.edges)} edges using {self.hooks_generator.name}")
        self.hooks_generator.edges_info(self.edges)
        for edge in self.edges:
            if random.uniform(0, 1) < drop_holds:
                new_edge = edge
            else:
                new_edge = self.hooks_generator.generate_hook(edge,
                                                              same_wings=same_wings,
                                                              hooks_base_point=hooks_base,
                                                              first_segment_height=first_h,
                                                              second_segment_height=second_h,
                                                              wing_dist=wings_dist,
                                                              hook_base_point=hook_base_point,
                                                              side_control_points_range=side_control_points_range,
                                                              hook_wideness_range=hook_wideness_range)
            edges += [new_edge] if new_edge else [edge]
        self.edges = edges
        return self

    def embedd_shapes(self,
                      shapes: List):
        avg_edge = self.calculate_avg_edge(self.edges)
        self.average_len = avg_edge
        for i in range(len(shapes)):
            edge = self.get_random_far_edge()
            point = edge.point_a
            edges = self.find_edges_with_point(point)
            other_points = []
            for edge in edges:
                other_points.append(edge.point_a if edge.point_a != point else edge.point_b)

            shape = Shape(point,
                          Image.open(shapes[i]),
                          int(avg_edge))
            intersection_points = [shape.intersection(point) for point in other_points]
            for point_a, point_b, edge in zip(other_points, intersection_points, edges):
                e = LineSegment(point_a, point_b)
                e.set_tiles(edge.tiles)
                self.edges.append(e)
                self.edges.remove(edge)

            self.edges.append(shape)

        return self

    def get_random_far_edge(self) -> Segment:
        i = 0
        while True:
            edge = random.choice(self.edges)
            dist = edge.dist_to_bounds(self.w, self.h)
            if dist > 0.5 * self.average_len:
                return edge
            i += 1
            if i >= 50: return edge

    def find_edges_with_point(self, point: Point):
        res = []
        for edge in self.edges:
            if edge.point_a == point or edge.point_b == point:
                res.append(edge)
        return res

    def ensure_hooks_in_bounds(self):
        for edge in self.edges:
            pass
        return self

    def draw_splitting(self):
        draw = ImageDraw.Draw(self.img)
        logger.info(f"drawing splitting, {len(self.edges)} edges")
        for edge in self.edges:
            if type(edge) is Shape:
                edge.draw(self.img)
            else:
                edge.draw(draw)
        return self

    def set_splitter(self,
                     splitter: Splitter):
        self.splitter = splitter
        logger.info(f"splitter was set to {self.splitter.name}")
        return self

    def set_hooks_generator(self,
                            hooks_generator: HooksGenerator):
        self.hooks_generator = hooks_generator
        logger.info(f"hooks generator was set to {self.hooks_generator.name}")
        return self

    @staticmethod
    def calculate_avg_edge(edges: List[Segment]):
        total: float = 0.
        for edge in edges:
            total += edge.length()
        total /= len(edges)
        return total
