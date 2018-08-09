#!/usr/bin/env python

import math
import pygame
import random
import sys
import time

colors = { 'red'     : (255, 0, 0),
           'green'   : (0, 255, 0),
           'blue'    : (0, 0, 255),
           'yellow'  : (255,255,0),
           'cyan'    : (0,255,255),
           'magenta' : (255,0,255) }

mycolors = { 'yellow' : (255, 255, 0),
             'green'  : (0, 255, 0) }

class World:
    def __init__(self, world_x_dims = (-1000, 1000),
                 world_y_dims = (-1000, 1000)):

        self.world_x_min = world_x_dims[0]
        self.world_y_min = world_y_dims[0]
        self.world_width = sum([abs(p) for p in world_x_dims])
        self.world_height = sum([abs(p) for p in world_y_dims])
        
        self.screen = None
        self.bg_image = None
        
    def init_world(self, canvas_dims, display_flags, color_depth=32):
        self.canvas_width, self.canvas_height = canvas_dims
        self.screen = pygame.display.set_mode(canvas_dims, display_flags, color_depth)

    def set_background_image(self, bg_image_f):
        self.bg_image = pygame.image.load(bg_image_f).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.canvas_width, self.canvas_height))
        self.screen.blit(self.bg_image, (0,0))

    def world_to_canvas_x(self, x):
        dist_to_x_min = abs(self.world_x_min - x)
        dist_x_ratio = float(dist_to_x_min) / float(self.world_width)
        canvas_x = int(round(dist_x_ratio * self.canvas_width))

        return canvas_x

    def world_to_canvas_y(self, y):
        dist_to_y_min = abs(self.world_y_min - y)
        dist_y_ratio = float(dist_to_y_min) / float(self.world_height)
        canvas_y = int(round(dist_y_ratio * self.canvas_height))

        return canvas_y

    def putpixel(self, coords=(0,0), color=(0, 0, 0)):
        x, y = coords
        world_pt = (self.world_to_canvas_x(x),
                    self.world_to_canvas_y(y))
        self.screen.set_at(world_pt, color)


def plot_julia(c):
    """
    Compute and return the coordinates for a julia set plot.
    The 'filled-in' Julia set J_R is the set of points z which
    do not approach infinity after R(z) is repeatedly applied
    (corresponding to a strange attractor). The true Julia
    set J is the boundary of the filled-in set
    (the set of 'exceptional points').
    http://mathworld.wolfram.com/JuliaSet.html

    This version of the Julia set, I adapted from a book
    on the TI-92 calculator.

    """

    pixels = []
    x = -2.0
    while x < 2.0:
        y = 0.0
        while y < 2.0:
            n = 1; z = complex(x,y)
            while abs(z) < 2.0 and n < 30:
                z = pow(z, 2) + c
                n += 1
            # if z didn't start flying off into space,
            # include it in the set of pixels to plot.
            if abs(z) < 2.0:
                pixels += [(x,y), (-x, -y)]
            y += .01
        x += 0.015
    return pixels


def shutdown():
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)

def main(args):

    shapes = {'julia' : complex(-1, 0),
              'rabbit': complex(-0.1, 0.8),
              'lion'  : complex(0.360284, 0.100376),
              'rick'  : complex(-1, 0.25)}

    pygame.init()

    bg_image_f = 'assets/cyberpunk_city.jpg'
    my_world = World(world_x_dims=(-5, 5), world_y_dims=(-4, 4))
    my_world.init_world((800,600), 
                        pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF)
    my_world.set_background_image(bg_image_f)

    # rewrote the event loop.
    while True:
        new_size = None
        
        events = pygame.event.get()
        if len(events) == 0:
            pass
        else:
            if pygame.QUIT in [e.type for e in events]:
                shutdown()
                
        key_events = [e for e in events if e.type == pygame.KEYDOWN]
        if len(key_events) > 0:
            print("Encountered key event!")
            e = key_events[-1]
            if e.key == pygame.K_t:
                shutdown()
 
        resize_events = [e for e in events if e.type == pygame.VIDEORESIZE]
        if len(resize_events) > 0:
            # get last resize event
            new_size = resize_events[-1].size

        if new_size:
            my_world.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE, 32)
            my_world.canvas_width, my_world.canvas_height = new_size

        # blit the background before plot.
        my_world.set_background_image(bg_image_f)
        c = shapes[random.choice(list(shapes.keys()))]
        pixels = plot_julia(c)
        for p in pixels:
            col = mycolors[random.choice(list(mycolors.keys()))]
            my_world.putpixel(p, col)

        # update the frame.
        pygame.display.update()
        # time.sleep(0.1)

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        mesg = "Exception in world! %s" % str(e)
        print(mesg)


