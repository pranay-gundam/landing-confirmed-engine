from typing import Tuple, List

class GameObject:
    def __init__(self, border: List[Tuple[int, int]]):
        self.border = border


    def move(self, dx, dy):
        

    def draw(self):
        raise NotImplementedError