from typing import Tuple, List
import numpy as np
import shapely as sp
import pygame as pg

class GameObject:
    def __init__(self, title: str, border: List[Tuple[float, float]], color: Tuple[float, float, float] = (0, 0, 0), durability: float = np.inf):
        self.shape = sp.geometry.Polygon(border)
        self.durability = durability
        self.title = title
        self.color = color

    def is_collided(self, other_obj):
        pass

    def draw(self, surface):
        x, y = self.shape.exterior.xy
        pg.draw.polygon(surface, self.color, list(zip(x, y)))

class MoveableGameObject(GameObject):
    def __init__(self, title: str, border: List[Tuple[float, float]], durability: float = np.inf):
        super().__init__(title, border, durability=durability)        
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

    def move_rotate(self, dtheta):
        self.shape = sp.affinity.rotate(self.shape, angle=dtheta, origin='center')

    def move_ticks(self, dt = 1):
        self.vel_x += self.accel_x
        self.vel_y += self.accel_y
        self.vel_theta += self.accel_theta

        # Rotation
        self.move_rotate(self.vel_theta * dt)

        # Normal rectangular movement
        self.move_rectangular(self.vel_x * dt, self.vel_y * dt)

    def is_collided(self, other_obj):
        return self.shape.intersects(other_obj.shape)

    def action(self, event):
        scale = 0.1
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.accel_x = -scale

            if event.key == pg.K_RIGHT:
                self.accel_x = scale

            if event.key == pg.K_UP:
                self.accel_y = -scale

            if event.key == pg.K_DOWN:
                self.accel_y = scale
    
    def update(self):
        self.move_ticks()
    
def GravityObject(GameObject):
    def __init__(self, title:str, border: List[Tuple[float, float]], durability: float = np.inf, mass: float = 1):
        super().__init__(title, border, durability=durability)
        self.mass = mass
        self.broken = False
        self.gravity = 9.8

    def is_collided(self, other_obj):
        self_force = self.mass * [self.accel_x, self.accel_y]
        other_force = other_obj.mass * [other_obj.accel_x, other_obj.accel_y]
        total_force = self_force + other_force

        if total_force > self.durability:
            self.broken = True

        return super().is_collided(other_obj), total_force
