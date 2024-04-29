from typing import List

from Algorithms.HooksGenerators.HooksGenerator import HooksGenerator

from DataStructures.Segments.Segment import Segment
from DataStructures.Segments.AgregateSegment import AggregateSegment
from DataStructures.Segments.MultipointSegment import MultipointSegment
from DataStructures.Segments.BezierSegment import BezierSegment
from DataStructures.Point import Point

import numpy as np

from random import randint, uniform


class BezierHooksGenerator(HooksGenerator):
    name: str = "Bezier Hooks Generator"

    def __init__(self):
        super().__init__()
        self.smooth_transition = True

    @staticmethod
    def process_flipping_bez(points: List[Point],
                             points2: List[Point],
                             m: Point):
        if not randint(0, 1): return points, points2, False
        return (Point.flip_points_180(points, m),
                Point.flip_points_180(points2, m),
                True)

    @classmethod
    def get_control_point(cls,
                          segment: BezierSegment,
                          end: bool = False) -> Point:
        if end:
            control_point = segment.points[-2] - segment.points[-1]
        else:
            control_point = segment.points[1] - segment.points[0]
        return control_point * -0.2

    def process_transition(self,
                           edge: AggregateSegment,
                           is_flipped: bool):
        segments: List[Segment | BezierSegment] = edge.segments
        beg = segments[0]
        beg_relative = segments[1]
        beg_control: Point = self.get_control_point(beg_relative, False)

        end = segments[-1]
        end_relative = segments[-2]
        end_control: Point = self.get_control_point(end_relative, True)

        if is_flipped:
            beg_control, end_control = end_control, beg_control

        beg_control += beg.point_b
        end_control += end.point_a

        new_beg = BezierSegment(beg.point_a,
                                beg.point_b,
                                [beg.point_a, beg_control, beg.point_b])
        new_end = BezierSegment(end.point_a,
                                end.point_b,
                                [end.point_a, end_control, end.point_b])
        edge.segments[0] = new_beg
        edge.segments[-1] = new_end

    def generate_hook(self,
                      edge: Segment,
                      hook_base_point: float = 0.3,
                      side_control_points_range: float = 0.4,
                      hook_wideness_range: float = 0.55,
                      **kwargs) -> Segment | None:
        if len(edge.tiles) != 2 and type(edge) is not MultipointSegment:
            return edge
        if edge.length() <= self.avg_len * self.min_generation_prop:
            return edge

        point_a, point_b = edge.point_a, edge.point_b
        m = point_a.mid_point(point_b)

        d = point_b - point_a
        dist = edge.length()
        actual_dist = edge.length()
        angle = np.arctan2(d.y, d.x)
        point_ar = point_a
        point_br = point_b.rotate(point_ar, -angle)

        top_control = Point(uniform(dist * hook_wideness_range - 0.05,
                                    dist * hook_wideness_range + 0.05),
                            0)
        left_control = Point(uniform(dist * (side_control_points_range - 0.1),
                                     dist * (side_control_points_range + 0.1)),
                             uniform(-dist / 10, dist / 10))
        right_control = Point(uniform(-dist * (side_control_points_range - 0.1),
                                      -dist * (side_control_points_range + 0.1)),
                              uniform(-dist / 10, dist / 10))
        a, b = uniform(hook_base_point - 0.05, hook_base_point + 0.05), uniform(hook_base_point - 0.05,
                                                                                hook_base_point + 0.05)

        d = point_br - point_ar
        hook_start = point_ar + d * a
        hook_end = point_br - d * b
        # hook_start = hook_start.rotate(point_ar, -angle)
        # hook_end = hook_end.rotate(point_ar, -angle)

        hook_1_start_d = hook_start + left_control * uniform(0.85, 1.15)
        hook_1_end = point_ar + Point(actual_dist * 0.5,
                                      actual_dist * 0.2)
        hook_1_end_d = hook_1_end - top_control * uniform(0.85, 1.15)
        points = [hook_start, hook_1_start_d, hook_1_end_d, hook_1_end]

        hook2_start = hook_1_end
        hook2_start_d = hook2_start + top_control * uniform(0.85, 1.15)
        hook2_end_d = hook_end + right_control * uniform(0.85, 1.15)

        points2 = [hook2_start, hook2_start_d, hook2_end_d, hook_end]

        points, points2 = Point.rotate_multiple_curves([points, points2],
                                                       point_ar,
                                                       angle)

        points, points2, is_flipped = self.process_flipping_bez(points,
                                                                points2,
                                                                m)

        seg1 = BezierSegment(point_a=points[0],
                             point_b=points[-1],
                             points=points,
                             tiles=edge.tiles)
        seg2 = BezierSegment(point_a=points2[0],
                             point_b=points2[-1],
                             points=points2,
                             tiles=edge.tiles)

        if is_flipped: a, b = b, a

        res: AggregateSegment | Segment = edge.split(a, b, [seg1, seg2])

        if self.smooth_transition:
            self.process_transition(res,
                                    is_flipped)

        return res


if __name__ == '__main__':
    p1 = Point(10, 10)
    p2 = Point(15, 15)

    v = p2 - p1

    print(np.linalg.norm([v.x, v.y]))
    print(np.arctan2(0, 10))

    p2 = p2.rotate(p1, np.arctan2(v.x, v.y))
    print(p2)
