from Algorithms.HooksGenerators.HooksGenerator import HooksGenerator
from DataStructures.Segments.Segment import Segment
from DataStructures.Point import Point

import numpy as np
from random import uniform, randint
from typing import List


class RectHooksGenerator(HooksGenerator):
    name: str = "Rect Hooks Generator"

    def __init__(self):
        super().__init__()

    def generate_hook(self,
                      edge: Segment,
                      same_wings: bool = True,
                      hooks_base_point: float = 0.3,
                      first_segment_height: float = 0.1,
                      second_segment_height: float = 0.15,
                      wing_dist: float = 0.1,
                      **kwargs) -> Segment | None:
        if len(edge.tiles) != 2:
            return edge
        if edge.length() <= self.avg_len * self.min_generation_prop:
            return edge

        point_a, point_b = edge.point_a, edge.point_b

        d = point_b - point_a
        dist = edge.length()

        angle = np.arctan2(d.y, d.x)
        point_ar = point_a
        point_br = point_b.rotate(point_ar, -angle)
        points_d = point_br - point_ar
        a, b = (uniform(hooks_base_point - 0.05, hooks_base_point + 0.05),
                uniform(hooks_base_point - 0.05, hooks_base_point + 0.05))

        first_seg_h = dist * uniform(first_segment_height - 0.03, first_segment_height + 0.03)
        second_seg_h = dist * uniform(second_segment_height - 0.03, second_segment_height + 0.03)
        left_wing = dist * uniform(wing_dist, wing_dist + 0.05)
        right_wing = dist * uniform(wing_dist, wing_dist + 0.05)
        if same_wings:
            left_wing = right_wing

        p1, p8 = edge.get_points(a, b)
        p1 = p1.rotate(point_ar, -angle)
        p8 = p8.rotate(point_ar, -angle)
        p0 = point_ar
        p9 = point_br
        # p1 = p0 + points_d * a
        p2 = p1 + Point(0, first_seg_h)
        p3 = p2 + Point(-left_wing, 0)
        # p8 = p9 - points_d * b
        p7 = p8 + Point(0, first_seg_h)
        p6 = p7 + Point(right_wing, 0)
        p4 = p3 + Point(0, second_seg_h)
        p5 = p6 + Point(0, second_seg_h)
        points = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
        points = Point.rotate_multiple_points(points,
                                              point_ar,
                                              angle)
        m = point_a.mid_point(point_b)
        points, is_flipped = self.process_flipping(points, m)
        if is_flipped: a, b = b, a

        edge = self.construct_new_edge(points, edge)
        return edge
