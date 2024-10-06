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
        self.accel_x = 0
        self.accel_y = 0
        self.accel_theta = 0

        self.vel_x = 0
        self.vel_y = 0
        self.vel_theta = 0

    def move_rectangular(self, dx, dy):
        self.shape = sp.affinity.translate(self.shape, xoff=dx, yoff=dy)
        
    def move_polar(self, dr, dtheta):
        self.shape = sp.affinity.translate(self.shape, xoff=dr * np.cos(dtheta), yoff= dr * np.sin(dtheta))

    def move_ticks(self, dt = 1):
        self.vel_x += self.accel_x
        self.vel_y += self.accel_y
        self.vel_theta += self.accel_theta

        # Need to do the angular movement as well
        

        # Normal rectangular movement
        self.move_rectangular(self.vel_x * dt, self.vel_y * dt)

    def draw(self):
        raise NotImplementedError