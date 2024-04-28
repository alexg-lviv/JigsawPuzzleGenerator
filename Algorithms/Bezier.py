from typing import List
from DataStructures.Point import Point
from PIL import Image, ImageDraw
import numpy as np


class Bezier:
    @staticmethod
    def process(points: List[Point],
                t: float) -> Point:
        if len(points) == 1:
            return points[0]

        temp_points = []
        for i in range(0, len(points) - 1):
            x = (1 - t) * points[i].x + t * points[i + 1].x
            y = (1 - t) * points[i].y + t * points[i + 1].y

            temp_points.append(Point(x, y))

        return Bezier.process(temp_points,
                              t)

    @staticmethod
    def draw(draw: ImageDraw,
             points: List[Point]):
        for t in np.arange(0.0, 1.0, 0.001):
            draw.point([Bezier.process(points, t).coords()], fill="black")


def create_white_image(x, y):
    data = np.ones((y, x, 3), dtype=np.uint8) * 255
    img = Image.fromarray(data, 'RGB')

    return img


if __name__ == '__main__':
    p_start_x = 50
    p_start_y = 100
    p_end_x = 150
    p_end_y = 200

    end_x_d = -180
    end_y_d = 20

    p_start = Point(p_start_x, p_start_y)
    p_d1 = Point(p_start_x + 200, p_start_y - 25)
    p_d2 = Point(p_end_x + end_x_d, p_end_y + end_y_d)
    p_d = Point(p_end_x, p_end_y)

    p2_start = Point(p_end_x, p_end_y)
    p2_d1 = Point(p_end_x - end_x_d, p_end_y - end_y_d)
    p2_d2 = Point(150, 75)
    p2_d = Point(250, 100)

    points = [p_start, p_d1, p_d2, p_d]
    points_2 = [p2_start, p2_d1, p2_d2, p2_d]

    img = create_white_image(1000, 1000)
    Bezier.draw(ImageDraw.Draw(img),
                points)
    Bezier.draw(ImageDraw.Draw(img),
                points_2)

    img.show()
