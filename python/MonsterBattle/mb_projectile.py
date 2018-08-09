# -------------------------------------------------------------------------
#  File:    mb_projectile.py
#  Created: Thu Jul 26 22:14:47 2007
#  Comment: This class represents a projectile that can be loaded in a weapon.
# -------------------------------------------------------------------------

import os
import string
import pygame
from pygame.locals import *
from mb_configparser import mbConfigParser

from mb_go import GameObject

class Projectile(GameObject):

    """
    This class is used to define the projectiles that are loaded into a weapon.
    """
    def __init__(self, gamedir, filename = None):

        # Image(s) i.e. sprites are inherited from GameObject base class.

        # self.image

        # Sound made when projectile is launched.

        self.fire_sound = None

        # Image and sound to make upon impact with an object.  (i.e. explosion)

        self.impact_sound = None
        self.impact_image = None
        self.impact_image_back = None

        # Size of impact.

        self.impact_size_x = 0
        self.impact_size_y = 0

        GameObject.__init__(self, gamedir, filename)

    def read_in_config(self, filename):

        parser = GameObject.read_in_config(self, filename)

        if parser.has_option('bio', 'fire_sound'):
            fire_sound_str = parser.get('bio', 'fire_sound')
            self.fire_sound = os.path.join(self.gamedir, string.strip(fire_sound_str))

        # Image dimensions.  Used to define size of impact image.

        if parser.has_option('bio', 'impact_size_x'):
            self.impact_size_x = int(parser.get('bio', 'impact_size_x'))

        if parser.has_option('bio', 'impact_size_y'):
            self.impact_size_y = int(parser.get('bio', 'impact_size_y'))

        if parser.has_option('bio', 'impact_image'):
            self.impact_image_str = parser.get('bio', 'impact_image')
            self.impact_image = pygame.image.load(os.path.join(self.gamedir, self.impact_image_str.strip()))
            self.impact_image = pygame.transform.scale(self.impact_image, (self.impact_size_x, self.impact_size_y))

        if parser.has_option('bio', 'impact_image_back'):
            self.impact_image_back = parser.get('bio', 'impact_image_back')
            if self.impact_image is not None:
                self.impact_image.set_colorkey(self.colors[self.impact_image_back])

        if parser.has_option('bio', 'impact_sound'):
            impact_sound_str = parser.get('bio', 'impact_sound')
            self.impact_sound = os.path.join(self.gamedir, string.strip(impact_sound_str))

