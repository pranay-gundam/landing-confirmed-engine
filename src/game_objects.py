from typing import Tuple, List
import numpy as np
import shapely as sp

class GameObject:
    def __init__(self, border: List[Tuple[float, float]], durability: float = np.inf):
        self.shape = sp.geometry.Polygon(border)
        self.durability = durability

    def is_collided(self, other_obj):
        pass

    def draw(self):
        raise NotImplementedError
    

class MoveableGameObject(GameObject):
    def __init__(self, border: List[Tuple[float, float]], durability: float = np.inf):
        super().__init__(border, durability=durability)        

    def move_rectangular(self, dx, dy):
        self.shape = sp.affinity.translate(self.shape, xoff=dx, yoff=dy)
        
    def move_polar(self, dr, dtheta):
        self.shape = sp.affinity.translate(self.shape, xoff=dr * np.cos(dtheta), yoff= dr * np.sin(dtheta))

    def draw(self):
        raise NotImplementedError