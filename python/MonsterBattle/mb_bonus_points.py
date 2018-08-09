# -------------------------------------------------------------------------
#  File:    mb_bonus_points.py
#  Created: Sat Mar  3 21:59:03 2007
# -------------------------------------------------------------------------

import math
import random

class Point:

    def __init__(self, x, y, value):

        self.x        = x
        self.y        = y
        self.heading  = random.uniform(0, 359)
        self.value    = value
        self.velocity = 30

    def compute_x(self):
        return self.x + self.velocity * math.cos(math.radians(self.heading))

    def compute_y(self):
        return self.y + self.velocity * math.sin(math.radians(self.heading))

class PointManager:

    def __init__(self, win, x1, y1, x2, y2, fonts):
        self.win     = win
        self.fonts   = fonts
        self.clip_x1 = x1
        self.clip_y1 = y1
        self.clip_x2 = x2
        self.clip_y2 = y2
        self.points  = list()

    def add_point(self, x, y, damage):
        p = Point(x, y, damage)
        self.points.append(p)

    def move_points(self):

        # Points don't explode like bullets.
        # They just drift off the screen.

        for p in self.points:

            # Advance point.
            p.x = p.compute_x()
            p.y = p.compute_y()

            # Test if out of bounds.
            if p.x <= self.clip_x1 or \
               p.x >= self.clip_x2 or \
               p.y <= self.clip_y1 or \
               p.y >= self.clip_y2:
                self.points.remove(p)

    def draw_points(self, plus_color, minus_color):
        for point in self.points:

            # Reverse plus and minus damage since
            # positive damage subtracts from health.
            if point.value >= 0:
                pass
                #color = minus_color
                #score = "-%d" % point.value
            else:
                color = plus_color
                score = "+%d" % abs(point.value)
                text = self.fonts['default'].render(score, 1, color)
                blit_info = (text, (point.x, point.y))
                self.win.bitblt(blit_info)
