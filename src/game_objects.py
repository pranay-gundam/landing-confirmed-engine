from typing import Tuple, List
import numpy as np
import shapely as sp
import pygame as pg
import move_actions as ma


def sign(x):
    return -1 if x < 0 else 1

def calc_air_resistance(velocity, drag_coeff, air_density, area):
    return sign(velocity) * 0.5 * drag_coeff * air_density * area * velocity ** 2

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

class AccelMoveableGameObject(GameObject):
    def __init__(self, title: str, border: List[Tuple[float, float]], durability: float = np.inf, scale : float = .1):
        super().__init__(title, border, durability=durability)        
        self.accel_x = 0
        self.accel_y = 0
        self.accel_theta = 0

        self.vel_x = 0
        self.vel_y = 0
        self.vel_theta = 0
        self.scale = scale

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
    
    def add_action(self, move_action):
        
        match move_action:
            case ma.MoveAction.UP:
                self.accel_y = -self.scale
            case ma.MoveAction.DOWN:
                self.accel_y = self.scale
            case ma.MoveAction.LEFT:
                self.accel_x = -self.scale
            case ma.MoveAction.RIGHT:
                self.accel_x = self.scale

    def update(self, move_actions = set()):
        
        for move_action in move_actions:
            self.add_action(move_action)
            
        self.move_ticks()
    
class GravAirForceMovableObject(AccelMoveableGameObject):
    def __init__(self, title:str, border: List[Tuple[float, float]], durability: float = np.inf, mass: float = 1, scale : float = .6):
        super().__init__(title, border, durability=durability, scale = scale)
        self.mass = mass
        self.broken = False
        
        self.drag_coeff = 0.0001
        self.air_density = 1.225
        self.x_area = max(border, key=lambda point: point[0])[0] - min(border, key=lambda point: point[0])[0]
        self.y_area = max(border, key=lambda point: point[1])[1] - min(border, key=lambda point: point[1])[1]
        
        # forces that persist through updates. list of (magnitude, direction)
        self.persistent_forces = [
            (9.8/50, ma.get_dir(ma.MoveAction.DOWN)) # gravity
        ]
        
        # forces that are removed each updated. list of (magnitude, direction)
        self.temp_forces = []
        self._add_air_resist() 
        
    def _add_air_resist(self):
        # air resist x
        self.temp_forces.append((calc_air_resistance(self.vel_x, self.drag_coeff, 
                                                     self.air_density, self.x_area), ma.get_dir(ma.MoveAction.LEFT)))
        
        # air resist y 
        self.temp_forces.append((calc_air_resistance(self.vel_y, self.drag_coeff, 
                                                     self.air_density, self.y_area), ma.get_dir(ma.MoveAction.UP)))
    
    def _update_accel(self, forces): 
        for force, direction in forces:
            self.accel_x += force * np.cos(direction) / self.mass
            self.accel_y += force * np.sin(direction) / self.mass

    def update(self, move_actions = set()):
        self.accel_x = 0
        self.accel_y = 0
        self.temp_forces = []
        
        for action in move_actions: 
            self.add_action(action)
        
        self._add_air_resist()
        self._update_accel(self.persistent_forces + self.temp_forces)
        
        super().update()
        
    def add_action(self, move_action):
        self.temp_forces.append((self.scale, ma.get_dir(move_action)))
            
    def is_collided(self, other_obj):
        self_force = self.mass * [self.accel_x, self.accel_y]
        other_force = other_obj.mass * [other_obj.accel_x, other_obj.accel_y]
        total_force = self_force + other_force

        if total_force > self.durability:
            self.broken = True

        return super().is_collided(other_obj), total_force


    def draw(self, surface):
        if self.broken:
            self.color = (255, 0, 0)

        if self.accel_y < 0:
            thruster_bounds = [(self.shape.bounds[0] + 5, self.shape.bounds[3]), 
                                (self.shape.bounds[0] + 5, self.shape.bounds[3]+20), 
                                (self.shape.bounds[2] - 5, self.shape.bounds[3]+20),
                                (self.shape.bounds[2] - 5, self.shape.bounds[3])]
            pg.draw.polygon(surface, (200, 0, 0), thruster_bounds)
        
        #if self.accel_x > 0:
        #    self.color = (0, 0, 255)

        super().draw(surface)