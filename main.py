import pygame
from pygame.locals import *
import graph
import esper
import random
import time
import _pickle as cPickle

class Interface:
    bk = object
    screen = object
    water_show = True
    earth_show = True
    temperature_show = False
    unit_show = True
    grass_show = True
    ground_show = True
    step_number = 0

    def __init__(self):
        graph.SCALE = 10
        self.map_x = Map.AREA_X * graph.SCALE
        self.map_y = Map.AREA_Y * graph.SCALE
        graph.init_window((self.map_x + 400), (self.map_y + 200))
        self.bk = graph.draw_background()
        pygame.mouse.set_visible(True)
        self.screen = pygame.display.get_surface()

    def step(self):
        graph.screen_text('step: ' + str(self.step_number), 20, (self.map_y + 60))


class Map:
    AREA_X = 80
    AREA_Y = 60

    @staticmethod
    def tor(c_x, c_y):
        if c_x >= Map.AREA_X:
            c_x -= Map.AREA_X
        elif c_x < 0:
            c_x -= Map.AREA_X
        if c_y >= Map.AREA_Y:
            c_y -= Map.AREA_Y
        elif c_y < 0:
            c_y -= Map.AREA_Y
        return c_x, c_y

class User:
    def __init__(self):
        pass

class Block:
    def __init__(self):
        pass

class Stock:
    def __init__(self):
        pass

class Position:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

class Paint:
    def __init__(self, r_, g_, b_, alfa_):
        self.color = (r_, g_, b_)
        self. alfa = alfa_

class Haul(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pass

class Show(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (position, paint) in self.world.get_components(Position, Paint):
            x = entity    
            graph.draw_rect(position.x, position.y, paint.color, paint.alfa)



def main():
    inter = Interface()
    world = esper.World()
    random.seed()

    user = world.create_entity(User(), Position(10, 10), Paint(125, 125, 125, 200))
    block = world.create_entity(Block(), Position(20, 20), Paint(250, 50, 50, 200))
    stock = world.create_entity(Stock(), Position(20, 20))

    world.add_processor(Show())

    while 1:
        inter.step_number += 1
        inter.screen.blit(inter.bk, (0, 0))
        inter.step()
       
        world.process()
        time.sleep(1)
        pygame.display.flip()
    

if __name__ == "__main__":
    main()


