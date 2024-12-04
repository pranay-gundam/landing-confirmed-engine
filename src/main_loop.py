import pygame as pg
from typing import List, Tuple
from game_objects import *




pg.init()

pg.display.set_caption('Quick Start')
window_surface = pg.display.set_mode((800, 600))

background = pg.Surface((800, 600))
background.fill(pg.Color('#FFFFFF'))

is_running = True

object_list = [MoveableGameObject('bob', [(500, 500), (510, 500), (510, 510), (500, 510)])]

def handle_action(objs, events):
    for event in events:
        for obj in objs:
            obj.action(event)

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
