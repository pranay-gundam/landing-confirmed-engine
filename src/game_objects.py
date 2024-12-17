from typing import Tuple, List
import numpy as np
import shapely as sp
import pygame as pg

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
    
class GravAirForceMovableObject(AccelMoveableGameObject):
    def __init__(self, title:str, border: List[Tuple[float, float]], durability: float = np.inf, mass: float = 1):
        super().__init__(title, border, durability=durability)
        self.mass = mass
        self.broken = False
        
        self.drag_coeff = 0.0001
        self.air_density = 1.225
        self.x_area = max(border, key=lambda point: point[0])[0] - min(border, key=lambda point: point[0])[0]
        self.y_area = max(border, key=lambda point: point[1])[1] - min(border, key=lambda point: point[1])[1]
        

        # dictionary to store forces and their directions
        self.forces = {}
        self.forces["grav"] = (9.8/50, np.pi / 2)
        self.forces["air_resistance_x"] = (calc_air_resistance(self.vel_x, self.drag_coeff, 
                                                                self.air_density, self.x_area), np.pi)
        self.forces["air_resistance_y"] = (calc_air_resistance(self.vel_y, self.drag_coeff, 
                                                                self.air_density, self.y_area), 3 * np.pi / 2)

    def add_force(self, name, force, direction):
        self.forces[name] = (force, direction)

    def remove_forces(self, names):
        for name in names:
            if name in self.forces:
                del self.forces[name]

    def update(self):
        self.accel_x = 0
        self.accel_y = 0
        
        self.forces["air_resistance_x"] = (calc_air_resistance(self.vel_x, self.drag_coeff, 
                                                                self.air_density, self.x_area), np.pi)
        self.forces["air_resistance_y"] = (calc_air_resistance(self.vel_y, self.drag_coeff, 
                                                                self.air_density, self.y_area), 3 * np.pi / 2)
        
        

        for force, direction in self.forces.values():
            self.accel_x += force * np.cos(direction) / self.mass
            self.accel_y += force * np.sin(direction) / self.mass
        
        
        super().update()

    def action(self, event):
        scale = 0.6
        print(self.forces)
        self.remove_forces(['left', 'right', 'up', 'down'])
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.add_force('left', scale, np.pi)

            if event.key == pg.K_RIGHT:
                self.add_force('right', scale, 0)

            if event.key == pg.K_UP:
                self.add_force('up', scale, 3 * np.pi / 2)

            if event.key == pg.K_DOWN:
                self.add_force('down', scale, np.pi / 2)

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