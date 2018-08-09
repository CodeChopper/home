# -------------------------------------------------------------------------
#  File:    mb_particle_explosion.py
#  Created: Sat Mar  3 20:41:46 2007
# -------------------------------------------------------------------------

import math
import random
import pygame
from pygame.locals import *

class Particle:

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

class ParticleManager:

    def __init__(self, x1, y1, x2, y2):
        self.clip_x1 = x1
        self.clip_y1 = y1
        self.clip_x2 = x2
        self.clip_y2 = y2
        self.particles  = list()

    def add_particle(self, x, y):
        p = Particle(x + random.uniform(-10, 10), y + random.uniform(-10, 10))
        self.particles.append(p)

    def move_particles(self):

        # Particles don't explode like bullets.
        # They just drift off the screen.

        for p in self.particles:

            # Advance particle.
            p.x = p.compute_x()
            p.y = p.compute_y()
            p.turns += 1

            # Test if out of bounds.
            if p.turns > 4 or \
               p.x <= self.clip_x1 or \
               p.x >= self.clip_x2 or \
               p.y <= self.clip_y1 or \
               p.y >= self.clip_y2:
                self.particles.remove(p)

    def draw_particles(self, surface, color):
        for i, particle in enumerate(self.particles):
            pygame.draw.circle(surface, color, (int(particle.x), int(particle.y)), 2, 0);


