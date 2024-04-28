from typing import List, Self, Any
from PIL import ImageDraw


class Tile:
    neighbours = []
    edges = []

    def add_neighbour(self, neighbour: Self):
        if neighbour is self: return
        if neighbour in self.neighbours: return
        self.neighbours.append(neighbour)

    def get_edges(self) -> List[Any]:
        return self.edges

    def add_neighbours(self, neighbours: List[Self]):
        for neighbour in neighbours:
            self.add_neighbour(neighbour)

    def draw(self, draw: ImageDraw):
        raise NotImplementedError("please implement draw")
