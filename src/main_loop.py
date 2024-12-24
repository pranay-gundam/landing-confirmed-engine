import pygame as pg
from typing import List, Tuple
from game_objects import *
import move_actions as ma


pg.init()

pg.display.set_caption('Quick Start')
window_surface = pg.display.set_mode((800, 600))

background = pg.Surface((800, 600))
background.fill(pg.Color('#FFFFFF'))

is_running = True

object_list = [GravAirForceMovableObject('bob', [(400, 300), (420, 300), (420, 350), (400, 350)])]

def handle_action(objs, events):
    
    keys = pg.key.get_pressed()
    
    is_left = keys[pg.K_LEFT]
    is_right = keys[pg.K_RIGHT]
    is_up = keys[pg.K_UP]
    
    if is_up: 
        for obj in objs:
            obj.action(ma.MoveAction.UP)
    
    if is_left ^ is_right: 
        for obj in objs:
            if is_left:
                obj.action(ma.MoveAction.LEFT)
            if is_right:
                obj.action(ma.MoveAction.RIGHT)
        

def update_objs(objs):
    for obj in objs:
        obj.update()

def main_loop(objs, surface, events):
    handle_action(objs, events)
    update_objs(objs)
    for obj in objs:
        obj.draw(surface)
    
while is_running:
    pg.time.delay(50)
    events = pg.event.get()
    if any(event.type == pg.QUIT for event in events):
        is_running = False

    window_surface.blit(background, (0, 0))
    main_loop(object_list, window_surface, events)

    pg.display.update()
