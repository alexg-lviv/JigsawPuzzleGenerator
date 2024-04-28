from DataStructures.Segments.Segment import Segment
from DataStructures.Tiles.Tile import Tile
from DataStructures.Point import Point
from PIL import Image, ImageDraw
from DataStructures.Segments.LineSegment import LineSegment


class Shape(Segment, Tile):
    def __init__(self,
                 center: Point,
                 image: Image,
                 avg_edge: int):
        self.image: Image = image
        self.center: Point = center
        self.resize(avg_edge)
        self.avg_edge = avg_edge

    def length(self):
        return self.avg_edge

    def resize(self,
               avg_edge: int):
        x, y = self.image.size[0], self.image.size[1]
        if x > y:
            aspect = avg_edge / x
        else:
            aspect = avg_edge / y

        self.image = self.image.resize((int(x * aspect),
                                        int(y * aspect)))

    def intersect(self,
                  x, y,
                  line: LineSegment) -> bool:
        if line.is_vert:
            return abs(line.point_a.x - x) < 2 and ((line.point_a.y <= y <= line.point_b.y)
                                                    or (line.point_b.y <= y <= line.point_a.y))
        y_on_line = line.slope * x + line.b
        return abs(y_on_line - y) < 10 and line.point_a <= Point(x, y) <= line.point_b

    def intersection(self,
                     point) -> Point | None:
        image_center = Point(self.image.size[0] / 2, self.image.size[1] / 2)
        point = point - self.center + image_center

        width, height = self.image.size
        seg = LineSegment(point, image_center)
        intersections = []
        for y in range(height):
            for x in range(width):
                # Get the pixel value at this position
                pixel = self.image.getpixel((x, y))
                if pixel[0] + pixel[1] > 200:
                    if self.intersect(x, y, seg):
                        intersections.append(Point(x, y))
        res = min(intersections, key=lambda x: point.dist(x), default=point)
        return res + self.center - image_center

    def draw(self,
             draw: Image):
        draw.paste(self.image,
                   (self.center - Point(self.image.size[0] / 2, self.image.size[1] / 2)).coords(True),
                   self.image)


if __name__ == '__main__':
    canvas = Image.open("../../data/cat.png")
    shape = Image.open("../../data/cat_shape.png")
    shape = Shape(Point(250, 250),
                  shape,
                  500)
    shape.draw(canvas)
    canvas.show()
