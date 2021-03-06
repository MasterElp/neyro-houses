# Install pygame
import graph
import esper
import random
import time
import math
#import _pickle as cPickle
import keyboard


class Interface:
    step_number = 0
    pause = False

    def __init__(self):
        graph.SCALE = 10
        self.map_x = Map.AREA_X * graph.SCALE
        self.map_y = Map.AREA_Y * graph.SCALE
        graph.init_window((self.map_x + 400), (self.map_y + 200), "My own little world")

    def step(self):
        graph.blit()
        graph.screen_text('step: ' + str(self.step_number), 20, (self.map_y + 60))

    def pause_pressed(self, e):
        if (self.pause):        
            self.pause = False
            print ("start")
        else:
            self.pause = True
            print ("pause")


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

class Mind:
    def __init__(self):
        pass

class Position:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

class Paint:
    """Init entity color (r, g, b, alfa)"""
    def __init__(self, r_=50, g_=50, b_=50, alfa_=50):  
        self.color = (r_, g_, b_)
        self. alfa = alfa_

class Life:
    def __init__(self, age_=0):  
        self.age = age_

class Tree:
    def __init__(self, bear_age_=10):
        self.bear_age = bear_age_

class Show(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (position, paint) in self.world.get_components(Position, Paint):
            graph.draw_rect(position.x, position.y, paint.color, paint.alfa)

class Grow(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (life) in self.world.get_component(Life):
            life.age += 1

class Move(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (position, mind) in self.world.get_components(Position, Mind):
            position.x += random.randint(-1, 1)
            position.y += random.randint(-1, 1)

class Bear_Fruit(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (position, tree, life) in self.world.get_components(Position, Tree, Life):
            if (life.age > tree.bear_age and Roll.dice_1000(50)):
                x = position.x + random.randint(-2, 2)
                y = position.y + random.randint(-2, 2)
                fruit = self.world.create_entity(Position(x, y), Paint(200, 100, 150, 100))

def main():
    inter = Interface()
    world = esper.World()
    random.seed()
    creature = {}
    tree = {}

    for i in range (15):
        creature[i] = world.create_entity(Life(), Mind(), Position(random.randint(40, 80), random.randint(10, 50)), Paint(125, 125, 125, 100))
        tree[i] = world.create_entity(Life(), Tree(20), Position(random.randint(40, 80), random.randint(10, 50)), Paint(50, 150, 50, 100))


    world.add_processor(Show())
    world.add_processor(Move())
    world.add_processor(Grow())
    world.add_processor(Bear_Fruit())

    

    #keyboard.add_hotkey('r', print, args=[world.component_for_entity(user, Relations).relations2others])
    keyboard.on_release_key('enter', inter.pause_pressed)
        

    # A dummy main loop:
    try:
        while True:
            inter.step_number += 1
            inter.step()
        
            time.sleep(0.1)
            world.process()
            graph.flip()
            
            
            while (inter.pause):
                pass

    except KeyboardInterrupt:
        return
    

if __name__ == "__main__":
    main()