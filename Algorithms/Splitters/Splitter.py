from typing import Tuple, List


class Splitter:
    name: str = "Splitter"
    def __init__(self):
        pass

    def split(self, **kwargs) -> Tuple[List, List]:
        raise NotImplementedError("Please implement this method")
