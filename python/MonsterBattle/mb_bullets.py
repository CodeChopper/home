# -------------------------------------------------------------------------
#  File:    mb_bullets.py
#  Created: Sat Mar  3 20:39:56 2007
# -------------------------------------------------------------------------

import math
import pygame
from pygame.locals import *
import mb_io

class Bullet:

    def __init__(self, attacker, weapon):
        self.attacker   = attacker
        self.weapon     = weapon
        self.projectile = self.weapon.projectile
        self.x        = attacker.weapon_pointing_x
        self.y        = attacker.weapon_pointing_y
        self.heading  = attacker.weapon_pointing_angle
        self.radius   = 2
        self.velocity = 40
        self.exploded = False

    def compute_x(self):
        return int(self.x + self.velocity * math.cos(math.radians(self.heading)))

    def compute_y(self):
        return int(self.y + self.velocity * math.sin(math.radians(self.heading)))

    def pushback_x(self):
        return int(self.x + 0.25 * self.velocity * math.cos(math.radians(self.heading)))

    def pushback_y(self):
        return int(self.y + 0.25 * self.velocity * math.sin(math.radians(self.heading)))


class BulletManager:

    def __init__(self, surface, x1, y1, x2, y2):
        self.surface = surface
        self.clip_x1 = x1
        self.clip_y1 = y1
        self.clip_x2 = x2
        self.clip_y2 = y2
        self.bullets = list()

    def add_bullet(self, attacker, weapon):
        b = Bullet(attacker, weapon)
        self.bullets.append(b)

    def bullet_collision(self, bullet, object):

        # Compute distance between the bullet and the object.
        xdiff = bullet.x - object.x
        ydiff = bullet.y - object.y

        dist = math.sqrt((xdiff*xdiff) + (ydiff*ydiff))

        if dist < object.radius:
            return True
        else:
            return False

    def fire_bullets(self, monsters):

        monsters_hit = []

        for b in self.bullets:

            # remove exploded bullets.

            if b.exploded:
                if b in self.bullets:
                    self.bullets.remove(b)
            else:
                # Advance bullet.
                b.x = b.compute_x()
                b.y = b.compute_y()

                # Test if out of bounds.
                if b.x <= self.clip_x1 or \
                   b.x >= self.clip_x2 or \
                   b.y <= self.clip_y1 or \
                   b.y >= self.clip_y2:
                    if b in self.bullets:
                        self.bullets.remove(b)
                else:
                    # Test for collision against monster.
                    for m in monsters:
                        if self.bullet_collision(b, m):
                            if b.attacker.current_weapon is not None: # prevents bug.
                                b.attacker.weapon_attack(m)

                                # Give monster a little push, by moving him
                                # to what would have been the next location
                                # of the exploded bullet.
                                m.x = b.compute_x()
                                m.y = b.compute_y()

                                mb_io.play_soundpath(b.projectile.impact_sound)
                                b.exploded = True
                                monsters_hit.append(m)
        return monsters_hit

    def draw_bullets(self, arena):

        for i, b in enumerate(self.bullets):
            if b.exploded:
                blit_info = (b.projectile.impact_image, (int(b.x), int(b.y)) )
                arena.bitblt(blit_info)
            else:
                blit_info = (b.projectile.get_sprite_frame(), (int(b.x), int(b.y)) )
                arena.bitblt(blit_info)
