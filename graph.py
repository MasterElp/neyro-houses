'''
Created on 12 12 2014

@author: V.Galiullin
'''
import pygame
from pygame.locals import *
#import sys
import os



SCALE = 10

def blit():
    global screen
    screen.blit(background, (0, 0))

def flip():
    pygame.display.flip()

def draw_background():
    global background
    global screen
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    #back, back_rect = load_image("back.bmp")
    #screen.blit(back, (0, 0))
    pygame.display.flip()

def init_window(c_max_x, c_max_y, caption):  
    pygame.init()
    window = pygame.display.set_mode((c_max_x, c_max_y))
    pygame.display.set_caption(caption)
    draw_background()
    #pygame.mouse.set_visible(True)
    #self.screen = pygame.display.get_surface()

def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except:
        print ("Cannot load image:" + name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def color_norm(c_r, c_g, c_b):
    if c_r > 250 :
        c_r = 250
    if c_g > 250 :
        c_g = 250
    if c_b > 250 :
        c_b = 250
    if c_r < 0 :
        c_r = 0
    if c_g < 0 :
        c_g = 0
    if c_b < 0 :
        c_b = 0
    return c_r, c_g, c_b

def screen_text(c_text, c_x, c_y, c_color = (50, 200, 50)):
    screen = pygame.display.get_surface()
    text = str(c_text)
    myFont = pygame.font.SysFont("None", 30)
    fontImage = myFont.render(text, 0, c_color)
    screen.blit(fontImage, (c_x, c_y))

def draw_rect(c_x, c_y, c_color, c_alfa = 255):
    screen = pygame.display.get_surface()
    image = pygame.Surface((SCALE, SCALE))
    image.set_alpha(c_alfa)
    pygame.draw.rect (image, c_color, (0, 0, SCALE, SCALE))

    screen.blit(image, (c_x * SCALE, c_y * SCALE))

def show_sprites(c_list):
    screen = pygame.display.get_surface()
    for element in c_list:
        element.area = screen.get_rect()
        element.rect.x = element.x * SCALE
        element.rect.y = element.y * SCALE
    sprites = pygame.sprite.Group(c_list)
    sprites.update()
    sprites.draw(screen)

def draw_cursor(c_x, c_y, c_color):
    screen = pygame.display.get_surface()
    image = pygame.Surface((SCALE, SCALE))
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    pygame.draw.rect (image, c_color, (0, 0, SCALE, SCALE), 3)

    screen.blit(image, (c_x * SCALE, c_y * SCALE))

def draw_direction_creature(c_x, c_y, c_dir, c_color1, c_color2, c_direction, c_height, c_width):
    screen = pygame.display.get_surface()

    start_point = (c_direction, 0)
    end_point = (c_direction, c_height + 1)

    image = pygame.Surface((SCALE, SCALE))
    pygame.draw.line (image, c_color1, start_point, end_point, c_width)
    if c_dir == 3 :
        pygame.draw.line (image, c_color2, (0, c_height/2), (c_direction, c_height/2), 2)
    if c_dir == 1 :
        pygame.draw.line (image, c_color2, (c_direction, c_height/2), (c_direction*2, c_height/2), 2)
    if c_dir == 0 :
        pygame.draw.line (image, c_color2, (c_direction, 0), (c_direction, c_height/2), 2)
    if c_dir == 2 :
        pygame.draw.line (image, c_color2, (c_direction, c_height/2), (c_direction, c_height), 2)
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    screen.blit(image, (c_x * SCALE, c_y * SCALE))

def draw_list(c_name, c_list, c_x = 20, c_y = 550, c_color = (250, 250, 0)):
    screen = pygame.display.get_surface()
    max_step = int(len(c_list))
    if max_step > 800:
        c_list = c_list[(max_step - 800):]
        max_step = 800
    image = pygame.Surface((max_step, 400))
    #colorkey = image.get_at((0,0))
    #image.set_colorkey(colorkey, RLEACCEL)

    step = 0
    poligon_points = [(0, 0)]
    for value in c_list :
        step += 1
        poligon_points.append((step, value / 30))
    poligon_points.append((step, 0))
    poligon_points.append((0, 0))
    pygame.draw.polygon(image, c_color, poligon_points, 0)
    screen.blit(image, (c_x, c_y))
    screen_text(c_name  + ': ' + str(value), c_x, c_y + 20)

def draw_legend(c_x, c_y, c_color, c_width,c_population, c_next):
    screen = pygame.display.get_surface()
    image = pygame.Surface((SCALE, SCALE))
    pygame.draw.line (image, c_color, (SCALE/2, 0), (SCALE/2, SCALE/2), c_width)

    screen.blit(image, (c_x, c_y + c_next * SCALE * 2))
    screen_text("pop:", c_x + SCALE * 2, c_y + c_next * SCALE * 2)
    screen_text(c_population, c_x + SCALE * 7, c_y + c_next * SCALE * 2)