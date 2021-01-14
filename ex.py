import random
import pygame
from pygame.locals import *
import sys
import os
import Graph
import _pickle as cPickle
import math
import time


class HotKeys:
    scale = 1
    gen_visible = True
    put = True
    sub_dir = "main"
    order_dig = False

    def input_event(self, events):
        self.save = False
        self.load = False
        self.plus = False
        self.minus = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.do = False

        Graph.screen_text('MAIN: [c]-console    [s]-show    [a]-action    [RETURN]-hit', 20, inter.map_y + 20)
        if self.sub_dir == "show":
            Graph.screen_text('SHOW: [w]-water  [e]-earth  [t]-temperature  [u]-unit  [r]-grass  [n]-ground  [g]-gen', 20, inter.map_y + 40)

        for event in events:
            if self.sub_dir == "show":
                if event.type == KEYUP and event.key == K_w:
                    inter.water_show = not inter.water_show
                elif event.type == KEYUP and event.key == K_e:
                    inter.earth_show = not inter.earth_show
                elif event.type == KEYUP and event.key == K_t:
                    inter.temperature_show = not inter.temperature_show
                elif event.type == KEYUP and event.key == K_u:
                    inter.unit_show = not inter.unit_show
                elif event.type == KEYUP and event.key == K_r:
                    inter.grass_show = not inter.grass_show
                elif event.type == KEYUP and event.key == K_n:
                    inter.ground_show = not inter.ground_show
            elif self.sub_dir == "action":
                pass

            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                inter.exit = True
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.left = True
                # elif event.type == KEYUP and event.key == K_LEFT:
                # self.left = False
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.right = True
            elif event.type == KEYDOWN and event.key == K_UP:
                self.up = True
            elif event.type == KEYDOWN and event.key == K_DOWN:
                self.down = True
            elif event.type == KEYDOWN and event.key == K_RETURN:
                self.do = True
            elif event.type == KEYDOWN and event.key == K_KP_PLUS:
                self.scale *= 2
            elif event.type == KEYDOWN and event.key == K_KP_MINUS:
                if self.scale < 1:
                    self.scale = 1
            elif event.type == KEYDOWN and event.key == K_a:
                self.sub_dir = "action"
            elif event.type == KEYUP and event.key == K_s:
                self.sub_dir = "show"
            elif event.type == KEYUP and event.key == K_p:
                inter.pause = not inter.pause
            elif event.type == KEYUP and event.key == K_c:
                inter.console = not inter.console
            elif pygame.key.get_mods() & KMOD_CTRL:
                if event.type == KEYDOWN and event.key == K_s:
                    self.save = True
                elif event.type == KEYDOWN and event.key == K_l:
                    self.load = True

    input_event = classmethod(input_event)


class Interface:
    bk = object
    screen = object
    water_show = True
    earth_show = True
    temperature_show = False
    unit_show = True
    grass_show = True
    ground_show = True

    def __init__(self):
        Graph.SCALE = 10
        self.map_x = Map.AREA_X * Graph.SCALE
        self.map_y = Map.AREA_Y * Graph.SCALE
        Graph.init_window((self.map_x + 400), (self.map_y + 200))
        self.bk = Graph.draw_background()
        pygame.mouse.set_visible(True)
        self.screen = pygame.display.get_surface()
        self.console = False
        self.pause = False
        self.exit = False
        self.select_place = False
        main_menu = Menu()
        build_menu = Menu()
        main_menu.add_menu('build', build_menu)
        main_menu.add_action('next', self.step)
        build_menu.add_build('wall', Wall)
        self.menu = main_menu

    def step(self):
        Graph.screen_text('step: ' + str(step_number), 20, (self.map_y + 60))
        #Graph.show_sprites(self.menu.buttons)
        cursor.step()
        #self.menu.button_focus()

        HotKeys.input_event(pygame.event.get())
        if self.console:
            command = raw_input('>')
            if command == 'big_boom':
                Layer.big_boom(1)
        elif self.exit:
            pygame.quit()
            sys.exit(0)

        if pygame.mouse.get_pressed()[0]:
            if self.menu.focused_button:
                if self.menu.focused_button is not None:
                    self.menu.focused_button.do()
                    time.sleep(0.5)
            else:
                xy = cursor.get_xy()
                if self.select_place:
                    self.menu.focused_button.place_object.place_mark()
                else:
                    self.show_object_info(xy)

    def place_mark(self):
        self.select_place = True

    def show_object_info(self, c_xy):
        unitmap.element_list[c_xy].show_info()


class Menu:
    def __init__(self):
        self.buttons = []
        self.focused_button = None

    def button_focus(self):
        self.focused_button = None
        for element in self.buttons:
            x, y = pygame.mouse.get_pos()
            if element.rect.collidepoint(x, y):
                self.focused_button = element
                element.image, element.rect = Graph.load_image(element.image_focus_file, -1)
            else:
                element.image, element.rect = Graph.load_image(element.image_file, -1)

    def add(self):
        pass

    def add_action(self, c_button_name, c_button_action):
        y = len(self.buttons)*2
        button = Button((Map.AREA_X + 1, y), c_button_name)
        self.buttons.append(button)
        button.do = c_button_action

    def add_build(self, c_button_name, c_object):
        y = len(self.buttons)*2
        button = Button((Map.AREA_X + 1, y), c_button_name)
        self.buttons.append(button)
        button.place_object = c_object
        button.do = Interface.place_mark

    def add_menu(self, c_button_name, c_menu):
        y = len(self.buttons)*2
        button = Button((Map.AREA_X + 1, y), c_button_name)
        self.buttons.append(button)
        button.menu = c_menu
        button.do = button.change_menu


class Button(pygame.sprite.Sprite):
    def __init__(self, xy, c_sprite_name):
        pygame.sprite.Sprite.__init__(self)
        #self.image_file = c_sprite_name + '.gif'
        #self.image_focus_file = c_sprite_name + '_focus.gif'
        #self.image, self.rect = Graph.load_image(self.image_file, -1)
        self.x = xy[0]
        self.y = xy[1]
        self.do = None
        self.menu = None
        self.place_object = object

    def change_menu(self):
        inter.menu = self.menu


class Cursor:
    def __init__(self):
        self.x = 10
        self.y = 10

    def get_xy(self):
        return self.x, self.y

    def step(self):
        x, y = pygame.mouse.get_pos()
        self.x = x / Graph.SCALE
        self.y = y / Graph.SCALE
        self.show()

    def show(self):
        if self.x >= Map.AREA_X:
            self.x = Map.AREA_X - 1
        if self.y >= Map.AREA_Y:
            self.y = Map.AREA_Y - 1
        if inter.select_place:
            Graph.draw_cursor(self.x, self.y, (200, 0, 0))
        else:
            Graph.draw_cursor(self.x, self.y, (0, 0, 200))


class Roll:
    @staticmethod
    def dice_100(c_probability):
        dice = random.randint(0, 100)
        if dice <= c_probability:
            return True
        else:
            return False

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

    @staticmethod
    def flat(c_x, c_y):
        if c_x >= Map.AREA_X:
            c_x = Map.AREA_X - 1
        elif c_x < 0:
            c_x = 0
        if c_y >= Map.AREA_Y:
            c_y = Map.AREA_Y - 1
        elif c_y < 0:
            c_y = 0
        return c_x, c_y


class LevelMap:
    def __init__(self):
        self.place_random_full(50)

    def place_random_full(self, c_max):
        for x in range(0, Map.AREA_X):
            for y in range(0, Map.AREA_Y):
                self.element_list[(x, y)] = random.randint(0, c_max)

    def inc_level(self, c_xy, c_level=1):
        self.element_list[c_xy] += c_level

    def dec_level(self, c_xy, c_level=1):
        if self.element_list[c_xy] >= c_level:
            self.element_list[c_xy] -= c_level
            return True
        elif self.element_list[c_xy] > 0:
            self.element_list[c_xy] = 0
            return True
        return False

    def get_level(self, c_xy):
        return self.element_list[c_xy]

    def flow(self, c_from_xy, c_to_xy):
        if self.element_list[c_from_xy] >= 1:
            self.element_list[c_from_xy] -= 1
            self.element_list[c_to_xy] += 1

    def show(self):
        for xy, level in self.element_list.items():
            self.show_cell(xy, level)


class Earth(LevelMap):
    element_list = {}

    def __init__(self):
        self.place_vectr(10)

    def place_vectr(self, c_max):
        c_max = c_max / 2
        height = random.randint(0, c_max)
        last_vect = random.randint(-1, 1)
        # line_last_height = {}
        line_last_vect = {}
        line_vect = {}
        line_r_height = {}
        line_height = {}
        for x in range(0, Map.AREA_X):
            for y in range(0, Map.AREA_Y):
                if y > 0:
                    vect = random.randint(-1, 2)
                    if vect == 2:
                        vect = last_vect
                        last_vect = random.randint(-1, 1)
                    else:
                        last_vect = vect
                    r_height = random.randint(-1, 2)
                    if r_height == 2:
                        r_height = vect
                    height = int(self.element_list[(x, y - 1)] / 2.00) + r_height
                    if height > c_max:
                        height = c_max
                    if height < 0:
                        height = 0
                if x == 0:
                    line_height[y] = random.randint(0, c_max)
                    line_last_vect[y] = random.randint(-1, 1)
                else:
                    line_vect[y] = random.randint(-1, 2)
                    if line_vect[y] == 2:
                        line_vect[y] = line_last_vect[y]
                        line_last_vect[y] = random.randint(-1, 1)
                    else:
                        line_last_vect[y] = line_vect[y]
                    line_r_height[y] = random.randint(-1, 2)
                    if line_r_height[y] == 2:
                        line_r_height[y] = line_vect[y]
                    line_height[y] = int(self.element_list[(x - 1, y)] / 2.00 + 0.5) + line_r_height[y]
                    if line_height[y] > c_max:
                        line_height[y] = c_max
                    if line_height[y] < 0:
                        line_height[y] = 0
                self.element_list[(x, y)] = int(height + line_height[y])

    def color(self, c_value):
        r1 = c_value * 20 + 10
        g1 = c_value * 20 + 40
        b1 = c_value * 20
        return Graph.color_norm(r1, g1, b1)

    def show(self):
        if inter.earth_show:
            for xy, value in self.element_list.items():
                x = xy[0]
                y = xy[1]
                Graph.draw_rect(x, y, (self.color(value)))


class Water(LevelMap):
    in_air = 700
    element_list = {}
    washout_probability = 30
    evaporation_probability = 10
    evaporation_cooling = 2
    boiling_temperature = 250
    rain_probability = 1

    def __init__(self):
        self.place_random_full(0)
        self.rain()

    def down(self, c_xy, c_level=1):
        self.element_list[(c_xy)] += c_level

    def up(self, c_xy, c_level=1):
        if (self.element_list[(c_xy)] >= c_level):
            self.element_list[(c_xy)] -= c_level
            return True
        elif (self.element_list[(c_xy)] > 0):
            self.element_list[(c_xy)] = 0
            return True
        return False

    def rain(self):
        for i in range(self.in_air):
            xy = random.randint(0, Map.AREA_X - 1), random.randint(0, Map.AREA_Y - 1)
            self.down(xy, 1)

    def level_lower(self, c_xy, c_level):
        sum_level = earth.get_level(c_xy) + c_level
        x = c_xy[0]
        y = c_xy[1]
        for rx in range(-1, 2):
            for ry in range(1, -2, -1):
                neighbor_xy = Map.flat(x + rx, y + ry)
                neighbor_level = earth.get_level(neighbor_xy) + self.element_list[neighbor_xy]
                if self.element_list[neighbor_xy] == 0:  # suhoi
                    if neighbor_level <= sum_level - 2:
                        return neighbor_xy
                elif self.element_list[neighbor_xy] > 0:  # mokrii
                    if neighbor_level <= sum_level - 1:
                        return neighbor_xy
        return False

    def step(self):
        if Roll.dice_1000(self.rain_probability):
            self.rain()

        for xy, level in self.element_list.items():
            if temperature.get_level(xy) > self.boiling_temperature:
                if self.up(xy, 0.02):
                    temperature.dec_level(xy, 2)
            if Roll.dice_1000(self.evaporation_probability):
                self.up(xy)
                temperature.dec_level(xy, self.evaporation_cooling)
            flow = True
            while level > 0 and flow is True: #if level > 0:
                min_xy = self.level_lower(xy, level)
                if min_xy:
                    self.flow(xy, min_xy)
                    if Roll.dice_1000(self.washout_probability) \
                            and earth.get_level(min_xy) < earth.get_level(xy):
                        earth.dec_level(xy)
                        earth.inc_level(min_xy)
                        # if self.element_list[xy] == 0:
                        # earth.inc_level(xy)
                    temperature.dec_level(xy, 2)
                    level -= 1
                else:
                    flow = False
            self.show_cell(xy, level)


    def color(self, c_value):
        r1 = 100 - c_value * 1
        g1 = 100 - c_value * 1
        b1 = 200 - c_value * 1
        return Graph.color_norm(r1, g1, b1)

    def show_cell(self, c_xy, c_level):
        if inter.water_show:
            if c_level > 0:
                    Graph.draw_rect(c_xy[0], c_xy[1], (self.color(c_level)), 200)


class Temperature(LevelMap):
    element_list = {}

    def __init__(self):
        self.place_random_full(50)

    def step(self):
        for xy, level in self.element_list.items():
            flow = True
            if level > 0: #while level > 0 and flow is True:
                x = xy[0]
                y = xy[1]
                lower_xy = []
                for rx in range(-1, 2):
                    for ry in range(-1, 2):
                        neighbor_xy = Map.flat(x + rx, y + ry)
                        neighbor_level = self.element_list[neighbor_xy]
                        if neighbor_level <= level - 1:
                            lower_xy.append(neighbor_xy)
                if len(lower_xy) > 0:
                    # min_xy = random.choice(lower_xy)
                    min_xy = xy
                    for coord in lower_xy:
                        if self.element_list[coord] < self.element_list[min_xy]:
                            min_xy = coord
                else:
                    flow = False

                if flow:
                    self.flow(xy, min_xy)
                    #level -= 1
            self.show_cell(xy, level)

    def color(self, c_value):
        r1 = c_value * 1
        g1 = 0
        b1 = 0
        return Graph.color_norm(r1, g1, b1)

    def show_cell(self, c_xy, c_level):
        if inter.temperature_show:
            if c_level >= 0:
                Graph.draw_rect(c_xy[0], c_xy[1], (self.color(c_level)), 250)


class Action: 
    def __init__(self, c_owner):
        self.step_count = 0
        self.finished = False
        self.finishable = True
        self.owner = c_owner
        self.aim_xy = None
        self.path = []
        self.aim_find = False
        self.aim_achieved = False
        self.step_number = 0

    def step(self):
        pass

    def search(self):
        pass

    def search_near(self):
        pass

    def time(self):
        self.step_number += 1
        if self.step_number >= self.step_count:
            return True
        else:
            return False

    def random_near(self):
        rx = random.randint(-1, 2)
        ry = random.randint(-1, 2)
        x = self.aim_xy[0] + rx
        y = self.aim_xy[1] + ry
        return Map.flat(x, y)

    def activate(self):
        if self.owner.movable:
            self.search()
        else:
            self.search_near()
        if self.aim_xy is not None:
            self.path = self.owner.layer.build_path(self.owner.xy, self.aim_xy)
            self.aim_find = True

    def path_move(self):
        if len(self.path) > 0:
            xy = self.path.pop(0)
            if not self.owner.layer.move(self.owner.xy, xy):
                if self.aim_xy is not None:
                    self.path = self.owner.layer.build_path(self.owner.xy, self.aim_xy)
        else:
            self.aim_achieved = True


class Empty(Action):
    pass


class Eat(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 5

    def step(self):
        if self.time():
            if self.aim_xy in self.owner.layer.element_list.keys():
                if self.owner.layer.element_list[self.aim_xy].eatable is True:
                    if not self.owner.layer.element_list[self.aim_xy].dec_count():
                        self.owner.layer.delete(self.aim_xy)
                    self.owner.necessity_line.element_list["satiety"].value += 20
                    self.finished = True
            if not self.finished:
                self.finishable = False

    def search(self):
        items = list(filter(lambda x: x[1].eatable is True, self.owner.layer.element_list.items()))
        if len(items) > 0:
            min_distance_element = min(items, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.aim_xy = min_distance_element[0]


class Drink(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 2

    def step(self):
        if self.time():
            if water.get_level(self.aim_xy) > 1:
                water.dec_level(self.aim_xy, 0.1)
                self.owner.necessity_line.element_list["thirst"].value += 20
                self.finished = True
            if not self.finished:
                self.finishable = False

    def search(self):
        deep_water_list = list(filter(lambda x: x[1] > 1, water.element_list.items()))
        if len(deep_water_list) > 0:
            min_distance_element = min(deep_water_list, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.aim_xy = min_distance_element[0]

    def search_near(self):
        deep_water_list = list(filter(lambda x: x[1] > 1, water.element_list.items()))
        if len(deep_water_list) > 0:
            near_element_list = list(filter(lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2) <= 1, deep_water_list))
            if len(near_element_list) > 0:
                near_element = random.choice(near_element_list)
                self.aim_xy = near_element[0]


class Harvest(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 20

    def step(self):
        if self.time():
            if self.aim_xy in self.owner.layer.element_list.keys():
                if self.owner.layer.element_list[self.aim_xy].fruit is True:
                    if self.owner.layer.element_list[self.aim_xy].__class__ == AppleTree:
                        xy = self.random_near()
                        if self.owner.layer.cell_empty(xy):
                            self.owner.layer.element_list[self.aim_xy].harvest()
                            self.owner.layer.element_list[xy] = Apple(self.owner.layer, 5)
                            self.owner.layer.element_list[xy].count = 5
                            self.finished = True
            if not self.finished:
                self.finishable = False

    def search(self):
        items = list(filter(lambda x: x[1].fruit is True, self.owner.layer.element_list.items()))
        if len(items) > 0:
            min_distance_element = min(items, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.aim_xy = min_distance_element[0]


class Plant(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 20

    def step(self):
        if self.time():
            xy = self.random_near()
            if self.owner.layer.cell_empty(xy):
                self.owner.layer.element_list[xy] = AppleTree(self.owner.layer)
                self.finished = True
            if not self.finished:
                self.finishable = False

    def search(self):
        water_cells = list(filter(lambda x: x[1] > 1, water.element_list.items()))
        cells = list(filter(lambda x: self.owner.layer.cell_empty(x[0]) is True, water_cells))
        if len(cells) > 0:
            min_distance_element = min(cells, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.aim_xy = min_distance_element[0]


class Haul(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 1
        self.stock_xy = None
        self.resource_xy = None
        self.object = None
        self.resource_types = []
        #self.resource_type = None
        
    def step(self):
        if self.object is None:
            if self.time():
                if self.aim_xy in self.owner.layer.element_list.keys():
                    if self.owner.layer.element_list[self.aim_xy].resource_type in self.resource_types:
                        self.object = self.owner.layer.element_list[self.aim_xy]
                        if not self.owner.layer.element_list[self.aim_xy].dec_count():
                            self.owner.layer.delete(self.aim_xy)
                        self.aim_xy = self.stock_xy
                        self.aim_achieved = False
                        self.path = self.owner.layer.build_path(self.owner.xy, self.aim_xy)      
                        return;
                    elif self.owner.layer.element_list[self.aim_xy].stock is True:
                        for resource in self.owner.layer.element_list[self.aim_xy].resources:
                            if resource.resource_type in self.resource_types:
                                index = self.owner.layer.element_list[self.aim_xy].resources.index(resource)
                                self.object = self.owner.layer.element_list[self.aim_xy].resources[index]
                                self.owner.layer.element_list[self.aim_xy].unstocking(resource)
                                self.aim_xy = self.stock_xy
                                self.aim_achieved = False
                                self.path = self.owner.layer.build_path(self.owner.xy, self.aim_xy)      
                                return;
            if self.object is None:
                self.finishable = False
                
        else:
            if self.time():
                if self.aim_xy in self.owner.layer.element_list.keys():
                    if self.owner.layer.element_list[self.aim_xy].stock is True:
                        #print 'stocking...'
                        self.owner.layer.element_list[self.aim_xy].stocking(self.object)
                        self.finished = True
                        self.object = None
                        return;
            if not self.finished:
                xy = self.random_near()
                if self.owner.layer.cell_empty(xy):
                    self.owner.layer.element_list[xy] = self.object.__class__(self.owner.layer)
                self.finishable = False

    
    def search(self):
        #print 'search'
        if self.stock_search():
            self.resorce_search()
            
    def stock_search(self):
        items = list(filter(lambda x: x[1].stock is True, self.owner.layer.element_list.items()))
        if len(items) > 0:
            #print 'stock search'
            min_distance_element = min(items, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.stock_xy = min_distance_element[0]
            self.resource_types = min_distance_element[1].stock_resource_types
            self.haul_from_stock = min_distance_element[1].haul_from_stock
            return True
        return False
    
    def resorce_search(self):
        items_sum =[]
        for resource_type in self.resource_types:
            items = list(filter(lambda x: x[1].resource_type == resource_type, self.owner.layer.element_list.items()))
            items_sum.extend(items)
            
            if self.haul_from_stock:
                stocks = list(filter(lambda x: x[1].stock is True, self.owner.layer.element_list.items()))
                for stock in stocks:
                    index = stocks.index(stock)
                    for resource in stock[1].resources:
                        if resource.resource_type == resource_type:
                            items_sum.append(stocks[index])
        if len(items_sum) > 0:
            #print 'resource search'
            #print (items_sum)
            min_distance_element = min(items_sum, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.resource_xy = min_distance_element[0]
            self.aim_xy = self.resource_xy


class Build(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 20

    def step(self):
        if self.time():
            if self.aim_xy in self.owner.layer.element_list.keys():
                if self.owner.layer.element_list[self.aim_xy].building_mark is True and len(self.owner.layer.element_list[self.aim_xy].resources) > 0:
                    #print 'building...'
                    self.owner.layer.element_list[self.aim_xy].build()
                    self.finished = True
            if not self.finished:
                self.finishable = False

    def search(self):
        items = list(filter(lambda x: x[1].building_mark is True and len(x[1].resources) > 0, self.owner.layer.element_list.items()))
        if len(items) > 0:
            min_distance_element = min(items, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.aim_xy = min_distance_element[0]


class Build_Mark(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 20
        self.build_object = Wall
        
    def step(self):
        if self.time():
            xy = self.random_near()
            if self.owner.layer.cell_empty(xy):
                self.owner.layer.element_list[xy] = Home(self.owner.layer)
                self.finished = True
            if not self.finished:
                self.finishable = False
    
    def search(self):
        unwater_cells = list(filter(lambda x: x[1] < 1, water.element_list.items()))
        cells = list(filter(lambda x: unitmap.cell_empty(x[0]) is True, unwater_cells))
        if len(cells) > 0:
            min_distance_element = min(cells, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.aim_xy = min_distance_element[0]
    

class Duplicate(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 50

    def step(self):
        if self.time():
            xy = self.random_near()
            if self.owner.layer.cell_empty(xy):
                self.owner.layer.element_list[xy] = self.owner.__class__(self.owner.layer)
                self.finished = True
            if not self.finished:
                self.finishable = False

    def search_near(self):
        self.aim_xy = self.owner.xy


class Sleep(Action):
    def __init__(self, c_owner):
        Action.__init__(self, c_owner)
        self.step_count = 80

    def step(self):
        if self.time():
            self.owner.necessity_line.element_list["tiredness"].value += 100
            self.finished = True

    def search(self):
        water_cells = list(filter(lambda x: x[1] <= 0, water.element_list.items()))
        cells = list(filter(lambda x: self.owner.layer.cell_empty(x[0]) is True, water_cells))
        if len(cells) > 0:
            min_distance_element = min(cells, key=lambda element: math.sqrt((element[0][0] - self.owner.xy[0]) ** 2 + (element[0][1] - self.owner.xy[1]) ** 2))
            self.aim_xy = min_distance_element[0]


class TaskLine:
    def __init__(self, c_owner):
        self.empty_task = Task(c_owner, Empty, 1000)
        self.active_task = self.empty_task
        self.owner = c_owner
        self.element_list = []

    def add(self, c_action, c_rate):
        if c_action != self.active_task.action.__class__:
            contains = False
            for element in self.element_list:
                if element.action.__class__ == c_action:
                    contains = True
                    break
            index = 0
            if not contains:
                for element in self.element_list:
                    if element.rate > c_rate:
                        index = self.element_list.index(element)
                        break
                task = Task(self.owner, c_action, c_rate)
                if index > 0:
                    self.element_list.insert(index - 1, task)
                else:
                    self.element_list.append(task)

    def step(self):
        if self.active_task.action.__class__ is Empty:
            self.owner.activity_line.step()
            if len(self.element_list) > 0:
                self.element_list[0].action.activate()
                if self.element_list[0].action.aim_find:
                    self.active_task = self.element_list.pop(0)
                else:
                    self.element_list.pop(0)
                    self.step()
        else:
            self.active_task.step()
            if self.active_task.finished:
                self.active_task = self.empty_task


class Task:
    def __init__(self, c_owner, c_action, c_rate):
        self.rate = c_rate
        self.owner = c_owner
        self.finished = False
        self.action = c_action(self.owner)

    def step(self):
        self.action.path_move()
        if self.action.aim_achieved:
            self.action.step()
            if self.action.finished:
                self.finished = True
            if not self.action.finishable:
                self.finished = True


class NecessityLine:
    def __init__(self, c_owner):
        self.owner = c_owner
        self.element_list = {}

    def add(self, c_name, c_task=None, c_value=50, c_rate=5, c_critical=20, c_max=100):
        self.element_list[c_name] = Necessity(c_task, c_value, c_rate, c_critical, c_max)

    def step(self):
        for necessity in self.element_list.values():
            necessity.step()
            if necessity.alarm and necessity.task is not None:
                self.owner.task_line.add(necessity.task, necessity.rate)


class Necessity:
    def __init__(self, c_task, c_value, c_rate, c_critical, c_max):
        self.rate = c_rate
        self.value = c_value
        self.critical_value = c_critical
        self.max_value = c_max
        self.alarm = False
        self.task = c_task
        self.enabled = True

    def step(self):
        self.value -= 1
        if self.value <= self.critical_value:
            self.alarm = True
        else:
            self.alarm = False


class ActivityLine:
    def __init__(self, c_owner):
        self.owner = c_owner
        self.element_list = {}

    def add(self, c_name, c_action, c_probability=500, c_rate=5):
        self.element_list[c_name] = Activity(c_action, c_probability, c_rate)

    def step(self):
        for activity in self.element_list.values():
            if activity.choice():
                self.owner.task_line.add(activity.action, activity.rate)


class Activity:
    def __init__(self, c_action, c_probability, c_rate):
        self.probability = c_probability
        self.action = c_action
        self.rate = c_rate
        self.enabled = True

    def choice(self):
        if Roll.dice_1000(self.probability):
            return True
        else:
            return False


class Layer:
    def __init__(self):
        self.element_list = {}
        
    def show(self):
        if inter.unit_show:
            for key, element in self.element_list.items():
                element.show(key)
                
    def delete(self, c_key):
        if self.element_list.has_key(c_key):
            self.element_list.pop(c_key)

    def cell_empty(self, c_xy):
        if c_xy in self.element_list.keys():
            return False
        else:
            return True
        
    def random_near(self, c_xy):
        rx = random.randint(-1, 2)
        ry = random.randint(-1, 2)
        x = c_xy[0] + rx
        y = c_xy[1] + ry
        return Map.flat(x, y)
    

class MarkLayer(Layer):  
    pass


class UnitLayer(Layer):
    def place_random(self, c_place_count, c_class, c_count=None):
        for i in range(0, c_place_count):
            x = random.randint(0, Map.AREA_X - 1)
            y = random.randint(0, Map.AREA_Y - 1)
            if c_count is not None:
                self.element_list[(x, y)] = c_class(self, c_count)
            else:
                self.element_list[(x, y)] = c_class(self)

    def step(self):
        for key, element in self.element_list.items():
            element.step(key)
        self.show()

    def build_path(self, c_key, c_aim):
            path_list = []
            x = c_key[0]
            y = c_key[1]
            while x != c_aim[0] or y != c_aim[1]:
                if x < c_aim[0]:
                    x += 1
                elif x > c_aim[0]:
                    x -= 1
                if y < c_aim[1]:
                    y += 1
                elif y > c_aim[1]:
                    y -= 1
                if self.cell_empty((x, y)):
                    path_list.append((x, y))
            return path_list

    def move(self, from_xy, to_xy):
            if to_xy not in self.element_list.keys() and from_xy in self.element_list.keys():
                self.element_list[to_xy] = self.element_list.pop(from_xy)
                return True
            return False


class UnitMap(UnitLayer):
    def __init__(self):
        self.element_list = {}
        self.place_random(5, WaterSource)
        self.place_random(5, WaterHole)
        self.place_random(6, Human)
        self.place_random(2, Home)
        self.place_random(10, Apple, 5)
        self.place_random(5, AppleTree)
        self.place_random(5, Log, 3)


class Soil(UnitLayer):
    def __init__(self):
        self.element_list = {}
        self.place_random(100, Dirt)
        
    def tread(self, c_key):
        if self.cell_empty(c_key):
            self.element_list[c_key] = Dirt(self)
        else:
            self.element_list[c_key].tread()
        #self.show()
            

class SomeObject:
    def __init__(self, c_layer):
        self.xy = (0, 0)
        self.layer = c_layer
        self.movable = False
        self.building_mark = False
        self.fruit = False
        self.eatable = False
        #self.resource = False
        self.stock = False
        self.haul_from_stock = False
        
    def step(self, c_key):
        self.xy = c_key
        
    def show(self, c_key):
        x = c_key[0]
        y = c_key[1]
        Graph.draw_rect(x, y, Graph.color_norm(self.red, self.green, self.blue), self.alpha)
        
class PhysicalObject(SomeObject):
    def __init__(self, c_layer):
        SomeObject.__init__(self, c_layer)
        self.stock_resource_type = "not stock"
        self.resource_type = "not use"  
        self.hp = 100
        
    def new(self):
        pass
    
    def step(self, c_key):
        SomeObject.step(self, c_key)
        if not self.building_mark:
            soil.tread(self.xy)
        

class StockObject(PhysicalObject):
    def __init__(self, c_layer):
        PhysicalObject.__init__(self, c_layer)
        self.resources = []
        self.stock = True
        self.stock_resource_types = []
        self.resources_count = 0
        self.alpha = 50
        
    def stocking(self, c_resource):
        self.resources_count += 1
        contains = False
        #print self.resources
        for element in self.resources:
            if element.__class__ == c_resource.__class__:
                index = self.resources.index(element)
                if self.resources[index].count < self.resources[index].max_count:
                    self.resources[index].inc_count()
                    contains = True
                    break;
        if not contains:           
            self.resources.append(c_resource.__class__(self.resources))

        #for element in self.resources:
            #print element
            #print "count: ", element.count
        if self.resources_count >= self.resources_need:
            self.stock = False
        #print "self.resources_need ", self.resources_need
        #print "self.resources_count ", self.resources_count
        #print self.stock
        
    def unstocking(self, c_resource):
        self.resources_count -= 1
        index = self.resources.index(c_resource)
        self.resources[index].dec_count()
        if self.resources[index].count == 0:
            self.resources.pop(index)


class Building(StockObject):
    def __init__(self, c_layer):
        StockObject.__init__(self, c_layer)
        self.building_mark = True
        self.stock_resource_types = ["build"]
        self.haul_from_stock = True
        self.alpha = 150
           
    def build(self):  
        #self.xy = c_key
        self.hp += self.resources[-1].build_resource_hp
        self.resources_need -= 1
        self.resources_count -= 1 
        self.resources[-1].dec_count()       
        if self.resources[-1].count == 0:
            self.resources.pop(-1)       
        #print self.resources
        #for element in self.resources:
            #print element
            #print "count: ", element.count
        if self.resources_need <= 0:
            self.building_mark = False
            self.alpha = 250
            self.build_finish()
            
    def build_finish(self):
        pass         
        

class Wall(Building): 
    def __init__(self, c_layer):
        Building.__init__(self, c_layer)
        self.resources_need = 1
        self.red = 200
        self.green = 100
        self.blue = 50

class Home(Building):
    def __init__(self, c_layer):
        Building.__init__(self, c_layer)
        self.resources_need = 3
        self.red = 200
        self.green = 50
        self.blue = 50
    
    def build_finish(self):     
        self.stock = True
        self.stock_resource_types = ["any", "build"]
        self.resources_need = 15
        self.haul_from_stock = False

      
class Grass(PhysicalObject):
    duplicate_probability = 800
    duplicate_age = 5
    
    def __init__(self, c_layer):
        PhysicalObject.__init__(self, c_layer)
        self.activity_line = ActivityLine(self)
        self.task_line = TaskLine(self)
        self.activity_line.add("duplicate", Duplicate, self.duplicate_probability)
        self.red = 150
        self.green = 250
        self.blue = 50
        self.alpha = 50
        
    
    def step(self, c_key):
        PhysicalObject.step(self, c_key)
        self.task_line.step()
        self.activity_line.step()
        
        
class Dirt(SomeObject):
    appear_probability = 500
    disappear_probability = 10
    
    def __init__(self, c_layer):
        SomeObject.__init__(self, c_layer)
        self.enabled = False
        self.step_need = 3
        self.step_count = 0
        self.red = 200
        self.green = 150
        self.blue = 150
        self.alpha = 0
               
    def tread(self): 
        if not self.enabled:
            if Roll.dice_1000(self.appear_probability):
                self.step_count += 1
            if self.step_count >= self.step_need:
                self.enabled = True
                self.alpha = 100
            
    def disappear(self):
        self.step_count -= 1
        if self.step_count <= 0:
            self.enabled = False
            self.alpha = 0
        
    def step(self, c_key):
        SomeObject.step(self, c_key)
        if self.enabled:
            if Roll.dice_1000(self.disappear_probability):
                xy = self.layer.random_near(self.xy)
                if self.layer.cell_empty(xy) or self.layer.element_list[xy].enabled == False:
                    self.disappear()
 


class LifeObject(PhysicalObject):
    def __init__(self, c_layer):
        PhysicalObject.__init__(self, c_layer)
        self.necessity_line = NecessityLine(self)
        self.activity_line = ActivityLine(self)
        self.task_line = TaskLine(self)


    def step(self, c_key):
        PhysicalObject.step(self, c_key)
        self.task_line.step()
        self.necessity_line.step()
        # self.activity_line.step()


class Human(LifeObject):
    def __init__(self, c_layer):
        LifeObject.__init__(self, c_layer)
        self.movable = True
        self.red = 250
        self.green = 150
        self.blue = 150
        self.alpha = 250
        self.necessity_line.add("satiety", Eat, 30, 2)
        self.necessity_line.add("thirst", Drink, 25, 3)
        self.necessity_line.add("tiredness", Sleep, 125, 1)
        self.activity_line.add("build", Build, 80)
        self.activity_line.add("mark_build", Build_Mark, 10)
        self.activity_line.add("carry", Haul, 80)
        self.activity_line.add("plant", Plant, 20)
        self.activity_line.add("harvest", Harvest, 20)
        self.activity_line.add("eat", Eat, 20)
        self.activity_line.add("drink", Drink, 20)
        self.activity_line.add("sleep", Sleep, 10)


class Herb(LifeObject):
    critical_thirst = 20
    max_thirst = 200
    duplicate_probability = 80

    def __init__(self, c_layer):
        LifeObject.__init__(self, c_layer)  
        self.activity_line.add("duplicate", Duplicate, self.duplicate_probability)
        self.activity_line.element_list["duplicate"].enabled = False
        self.necessity_line.add("thirst", Drink, 125, 2, self.critical_thirst, self.max_thirst)
        self.age = 0
        self.red = 150
        self.green = 250
        self.blue = 50
        self.alpha = 50

    def step(self, c_key):
        LifeObject.step(self, c_key)
        self.age += 1
        if self.necessity_line.element_list["thirst"].value < 0:
            self.layer.delete(c_key)
        if self.age >= self.duplicate_age:
            self.activity_line.element_list["duplicate"].enabled = True


class AppleTree(Herb):
    critical_thirst = 20
    max_thirst = 200
    duplicate_probability = 8
    duplicate_age = 100

    def __init__(self, c_layer):
        Herb.__init__(self, c_layer)
        self.alpha = 250

    def step(self, c_key):
        Herb.step(self, c_key)
        if (self.age % self.duplicate_age) == 0:
            self.fruit = True
            self.color()

    def harvest(self):
        self.fruit = False
        self.color()

    def color(self):
        if self.fruit is True:
            self.red = 150
            self.green = 250
        else:
            self.red = 50
            self.green = 150





class CountableObject(PhysicalObject):
    def __init__(self, c_layer, c_count):
        PhysicalObject.__init__(self, c_layer)
        self.count = c_count
        self.max_count = 10

    def dec_count(self, c_count=1):
        if self.count >= c_count:
            self.count -= c_count
            return True
        else:
            self.count = 0
            return False
            
    def inc_count(self, c_count=1):
        self.count += c_count


class Food(CountableObject):
    def __init__(self, c_layer, c_count=1):
        CountableObject.__init__(self, c_layer, c_count)
        self.eatable = True
        self.resource_type = "any"


class Apple(Food):
    def __init__(self, c_layer, c_count=1):
        Food.__init__(self, c_layer, c_count)
        self.red = 250
        self.green = 150
        self.blue = 50
        self.alpha = 250
        
class Log(CountableObject):
    def __init__(self, c_layer, c_count=1):
        CountableObject.__init__(self, c_layer, c_count)
        self.resource_type = "build"
        self.build_resource_hp = 20 
        self.red = 200
        self.green = 130
        self.blue = 70
        self.alpha = 250


class WaterSource(PhysicalObject):
    def __init__(self, c_layer):
        PhysicalObject.__init__(self, c_layer)
        self.red = 50
        self.green = 150
        self.blue = 250
        self.alpha = 250

    def step(self, c_key):
        water.inc_level(c_key, 1)


class WaterHole(PhysicalObject):
    def __init__(self, c_layer):
        PhysicalObject.__init__(self, c_layer)
        self.red = 0
        self.green = 50
        self.blue = 100
        self.alpha = 250

    def step(self, c_key):
        water.dec_level(c_key, 1)


def main():
    for i in range(0, landscape_evolution_steps):
        inter.screen.blit(inter.bk, (0, 0))
        earth.show()
        water.step()
        temperature.step()
        pygame.display.flip()

    while 1:
        main_step()


def main_step():
    global step_number
    step_number += 1
    inter.screen.blit(inter.bk, (0, 0))
    inter.step()
    earth.show()
    soil.step()
    water.step()
    unitmap.step()
    temperature.step()
    cursor.step()
    pygame.display.flip()

    while inter.pause:
        inter.screen.blit(inter.bk, (0, 0))
        earth.show()
        water.show()
        temperature.show()
        unitmap.show()
        soil.show()
        inter.step()
        Graph.screen_text('pause', inter.map_x + 10, inter.map_y + 10, (250, 0, 0))
        pygame.display.flip()

landscape_evolution_steps = 0
step_number = landscape_evolution_steps
inter = Interface()
earth = Earth()
temperature = Temperature()
water = Water()
unitmap = UnitMap()
soil = Soil()
cursor = Cursor()

if __name__ == "__main__":
    main()


