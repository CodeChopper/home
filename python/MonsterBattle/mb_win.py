# -------------------------------------------------------------------------
#  File:    mb_win.py
#  Created: Tue Feb 28 20:44:13 2006
# -------------------------------------------------------------------------

import pygame
from pygame.locals import *

class PyGameWin:
    """
    This class defines a (sub) window within the main screen.
    """

    def __init__(self, width, height, x, y):

        # Dimensions
        self.width  = width
        self.height = height
        # Surface
        self.surf = pygame.Surface((width, height))
        # Coordinates on main screen.
        self.loc = (x,y)
        # Background color
        self.bg_color = (0,0,0)
        # Convert pixel format.  Speeds up blit'ing
        self.surf.convert()

    def set_bg(self, color):
        # Set background color
        self.bg_color = color
        self.surf.fill(self.bg_color)

    def clear(self):
        # Clear window.
        self.surf.fill(self.bg_color)

    def bitblt(self, blit_info):
        surface, position = blit_info
        # Blit another surface onto this surface.
        if surface:
            self.surf.blit(surface, position)

    def center_x(self):
        return self.surf.get_rect().centerx

    def get_blit(self):
        # Return info needed to blit this surface
        # onto another surface.
        return self.surf, self.loc








