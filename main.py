import pygame
from pygame.locals import *
import graph
import esper
import random
import time
import math
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
        graph.init_window((self.map_x + 400), (self.map_y + 200), "Для Алии")
        self.bk = graph.draw_background()
        pygame.mouse.set_visible(True)
        self.screen = pygame.display.get_surface()

    def step(self):
        graph.screen_text('step: ' + str(self.step_number), 20, (self.map_y + 60))


class Roll:
    @staticmethod
    def dice_1000(c_probability):
        dice = random.randint(0, 1000)
        if dice <= c_probability:
            return True
        else:
            return False

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
        self.entity = 1000

class Search_aim(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("Search_aim")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            if(not aim.has_aim):
                min_distance = 1000
                found = False
                #print("user_entity")
                #print(user_entity)
                for block_entity, (block, block_position, stocked, busy) in self.world.get_components(Block, Position, Stocked, Busy):
                    if ((not stocked.is_true) and (not busy.is_true)):
                        found = True
                        distance = math.sqrt((block_position.x - position.x)**2 + (block_position.y - position.y)**2)
                        if (distance < min_distance):
                            min_distance = distance
                            near_x = block_position.x
                            near_y = block_position.y
                            near_entity = block_entity

                if (found):
                    #print("near_entity")
                    #print(near_entity)
                    aim.has_aim = True
                    aim.x = near_x
                    aim.y = near_y
                    aim.entity = near_entity
                    near_busy = self.world.component_for_entity(near_entity, Busy)
                    near_busy.is_true = True


class Move(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("move")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            if (aim.has_aim):
                if (position.x == aim.x and position.y == aim.y):
                    aim.has_aim = False
                    busy = self.world.component_for_entity(aim.entity, Busy)
                    busy.is_true = False
                    pass
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
        #print("haul")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            for block_entity, (block, block_position, stocked, busy) in self.world.get_components(Block, Position, Stocked, Busy):
                if (position.x == block_position.x and position.y == block_position.y and not stocked.is_true):
                    #aim.has_aim = False
                    #busy = self.world.component_for_entity(aim.entity, Busy)
                    #busy.is_true = False

                    min_distance = 1000
                    found = False
                    for stock_entity, (stock, stock_position, full) in self.world.get_components(Stock, Position, Full):
                        if (not full.is_true):
                            found = True
                            distance = math.sqrt((block_position.x - stock_position.x)**2 + (block_position.y - stock_position.y)**2)
                            if (distance < min_distance):
                                min_distance = distance
                                near_x = stock_position.x
                                near_y = stock_position.y

                    if (found):
                        if (block_position.x > near_x):
                            block_position.x-=1
                        elif (block_position.x < near_x):
                            block_position.x+=1
                        if (block_position.y > near_y):
                            block_position.y-=1
                        elif (block_position.y < near_y):
                            block_position.y+=1
                        


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
                        #print("!!!++++++!!!")


class Show(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (position, paint) in self.world.get_components(Position, Paint):
            graph.draw_rect(position.x, position.y, paint.color, paint.alfa)

class End(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        not_full = False
        for entity, (full, stock) in self.world.get_components(Full, Stock):
            if (not full.is_true):
                not_full = True
        if (not not_full):
            graph.screen_text("С днем святого Валентина, Алия! Я люблю тебя!", 310, 280, c_color = (200, 100, 50))

def main():
    inter = Interface()
    world = esper.World()
    random.seed()
    block = {}
    stock = {}
    user = {}

    for i in range (5):
        user[i] = world.create_entity(User(), Position(random.randint(50, 70), random.randint(20, 40)), Paint(125, 125, 125, 100), Aim())
    for i in range (28):
        block[i] = world.create_entity(Block(), Position(random.randint(50, 70), random.randint(20, 40)), Paint(250, 50, 50, 100), Stocked(), Busy())
    for y in range (len(stock_array)): 
        for x in range (len(stock_array[y])):
            if (stock_array[y][x] == 1):
                stock[i] = world.create_entity(Stock(), Position(x + 50, y + 20), Full())

    world.add_processor(Stock_check())
    world.add_processor(Move())
    world.add_processor(Haul())
    world.add_processor(Search_aim())
    world.add_processor(Show())
    world.add_processor(End())
    

    while 1:
        inter.step_number += 1
        inter.screen.blit(inter.bk, (0, 0))
        inter.step()
       
        time.sleep(0.1)
        world.process()
        pygame.display.flip()
    

if __name__ == "__main__":
    main()


