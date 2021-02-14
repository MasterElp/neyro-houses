import pygame
from pygame.locals import *
import graph
import esper
import random
import time
import _pickle as cPickle

stock_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]

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

class Stocked:
    def __init__(self):
        self.is_true = False

class Full:
    def __init__(self):
        self.is_true = False

class Busy:
    def __init__(self):
        self.is_true = False

class Aim:
    def __init__(self):
        self.has_aim = False
        self.x = 0
        self.y = 0

class Search_aim(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("Search_aim")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            print("resorce_search")
            block_position = self.resorce_search()
            if (block_position != None):
                aim.has_aim = True
                aim.x = block_position.x
                aim.y = block_position.y

    def resorce_search(self):
        for block_entity, (block, position, stocked) in self.world.get_components(Block, Position, Stocked):
            if (not stocked.is_true):
                print(position)
                return position
        return None

    def haul_block(self):
        print("haul_block")


class Move(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("move")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            if (aim.has_aim):
                if (position.x == aim.x and position.y == aim.y):
                    aim.has_aim = False
                    print("!!!!!!!!")
                else:
                    if (position.x > aim.x):
                        position.x-=1
                    elif (position.x < aim.x):
                        position.x+=1
                    if (position.y > aim.y):
                        position.y-=1
                    elif (position.y < aim.y):
                        position.y+=1

class Haul(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("haul")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            for block_entity, (block, block_position, stocked) in self.world.get_components(Block, Position, Stocked):
                if (position.x == block_position.x and position.y == block_position.y and not stocked.is_true):
                    for stock_entity, (stock, stock_position, full) in self.world.get_components(Stock, Position, Full):
                        if (not full.is_true):
                            if (block_position.x > stock_position.x):
                                block_position.x-=1
                            elif (block_position.x < stock_position.x):
                                block_position.x+=1
                            if (block_position.y > stock_position.y):
                                block_position.y-=1
                            elif (block_position.y < stock_position.y):
                                block_position.y+=1
                            break


class Stock_check(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for block_entity, (block, block_position, stocked) in self.world.get_components(Block, Position, Stocked):
            for stock_entity, (stock, stock_position, full) in self.world.get_components(Stock, Position, Full):
                if (not full.is_true and not stocked.is_true):
                    if (block_position.x == stock_position.x and block_position.y == stock_position.y):
                        full.is_true = True
                        stocked.is_true = True
                        print("!!!++++++!!!")


class Show(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (position, paint) in self.world.get_components(Position, Paint):
            graph.draw_rect(position.x, position.y, paint.color, paint.alfa)


def main():
    inter = Interface()
    world = esper.World()
    random.seed()
    block = {}
    stock = {}
    user = {}

    for i in range (5):
        user[i] = world.create_entity(User(), Position(random.randint(0, 20), random.randint(0, 20)), Paint(125, 125, 125, 200), Aim())
    for i in range (28):
        block[i] = world.create_entity(Block(), Position(random.randint(0, 20), random.randint(0, 20)), Paint(250, 50, 50, 200), Stocked(), Busy())
    for y in range (len(stock_array)): 
        for x in range (len(stock_array[y])):
            if (stock_array[y][x] == 1):
                stock[i] = world.create_entity(Stock(), Position(x, y), Full())

    world.add_processor(Stock_check())
    world.add_processor(Show())
    world.add_processor(Search_aim())
    world.add_processor(Move())
    world.add_processor(Haul())

    while 1:
        inter.step_number += 1
        inter.screen.blit(inter.bk, (0, 0))
        inter.step()
       
        world.process()
        time.sleep(0.2)
        pygame.display.flip()
    

if __name__ == "__main__":
    main()


