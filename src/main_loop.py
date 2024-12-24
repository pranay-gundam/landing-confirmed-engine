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


def update_objs(objs):
    
    move_actions = set()
    if pg.key.get_pressed()[pg.K_UP]:
        move_actions.add(ma.MoveAction.UP)
    if pg.key.get_pressed()[pg.K_DOWN]:
        move_actions.add(ma.MoveAction.DOWN)
    if pg.key.get_pressed()[pg.K_LEFT]:
        move_actions.add(ma.MoveAction.LEFT)
    if pg.key.get_pressed()[pg.K_RIGHT]:
        move_actions.add(ma.MoveAction.RIGHT)
    
    for obj in objs:
        obj.update(move_actions)

def main_loop(objs, surface, events):
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
