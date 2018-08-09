# -------------------------------------------------------------------------
#  File:    mb_derez_explosion.py
#  Created: Sat Mar  3 20:41:46 2007
# -------------------------------------------------------------------------

import math
import random
import pygame
from pygame.locals import *

class Derez:

    def __init__(self, x, y):

        self.x        = x
        self.y        = y
        self.heading  = random.uniform(0, 359)
        self.velocity = 20
        self.turns    = 0

    def compute_x(self):
        return int(self.x + self.velocity * math.cos(math.radians(self.heading)))

    def compute_y(self):
        return int(self.y + self.velocity * math.sin(math.radians(self.heading)))

class DerezManager:

    def __init__(self, x1, y1, x2, y2):
        self.clip_x1 = x1
        self.clip_y1 = y1
        self.clip_x2 = x2
        self.clip_y2 = y2
        self.derezes  = list()

    def add_derez(self, x, y):
        p = Derez(x + random.uniform(-10, 10), y + random.uniform(-10, 10))
        self.derezes.append(p)

    def move_derezes(self):

        # Derezs don't explode like bullets.

        for p in self.derezes:

            # Advance derez.
            p.x = p.compute_x()
            p.y = p.compute_y()
            p.turns += 1

            # Test if out of bounds.
            if p.turns > 4 or \
               p.x <= self.clip_x1 or \
               p.x >= self.clip_x2 or \
               p.y <= self.clip_y1 or \
               p.y >= self.clip_y2:
                self.derezes.remove(p)

    def draw_derezes(self, surface, color):
        for i, derez in enumerate(self.derezes):
            pygame.draw.circle(surface, color, (int(derez.x), int(derez.y)), 2, 0);
            if i > 0:
                pygame.draw.line(surface, color,
                                 (int(self.derezes[i-1].x), int(self.derezes[i-1].y)),
                                 (int(derez.x), int(derez.y)), 2);

