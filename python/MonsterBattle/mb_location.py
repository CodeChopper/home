# -------------------------------------------------------------------------
#  File:    mb_location.py
#  Created: Tue Feb  7 20:50:34 2006
# -------------------------------------------------------------------------

import os
import string
import random
import datetime
from mb_go import GameObject

import pygame
from pygame.locals import *

class Location(GameObject):

    """
    This class is used to create location objects.
    """
    def __init__(self, globals, gamedir, filename = None):

        #
        self.gamedir = gamedir
        #
        # Global resources.
        #
        self.globals = globals
        #
        self.descriptions = list()
        #
        # objects and beings contain
        # actual game objects.
        #
        self.objects      = list()
        self.beings       = list()
        #
        # traps, weapons and monsters
        # only contain names (strings)
        # of things and not the actual
        # game objects.
        #
        self.traps        = list()
        self.weapons      = list()
        self.monsters     = list()
        #
        # links begins with strings
        # but the strings are replaced
        # with references to actual locations.
        #
        self.links        = dict()
        #
        # Sound(s) for this location.
        #
        self.sound_list   = list()
        self.num_sounds   = 0
        #
        #
        self.height = self.globals['screen_height']
        self.width  = self.globals['screen_width']

        GameObject.__init__(self, gamedir, filename)


    def set_name(self, name):
        self.name = name

    def read_in_config(self, filename):

        if filename is None:
            pass # sometimes we want to create location objects w/ no 
                 # corresponding config file.
        else:
            parser = GameObject.read_in_config(self, filename)

            # Redefine image size over game object defaults
            # since location sprites need to be larger to
            # cover game area.  These probably won't ever
            # need to be defined in the file.
            #
            self.image_size_x = self.globals['screen_width']
            self.image_size_y = self.globals['screen_height'] - 25
            #

            if parser.has_section('bio'):

                if parser.has_option('bio', 'sounds'):
                    sounds_str = parser.get('bio', 'sounds')
                    self.sound_list = sounds_str.split(',')
                    for i in range(len(self.sound_list)):
                        self.sound_list[i] = os.path.join(self.gamedir, string.strip(self.sound_list[i]))
                        self.num_sounds = len(self.sound_list)

                if parser.has_option('bio', 'traps'):
                    traps_str = parser.get('bio', 'traps')
                    self.traps = traps_str.split(',')
                    # remove whitespace
                    for i in range(len(self.traps)):
                        self.traps[i] = string.strip(self.traps[i])
    
                if parser.has_option('bio', 'weapons'):
                    weapons_str = parser.get('bio', 'weapons')
                    self.weapons = weapons_str.split(',')
                    # remove whitespace
                    for i in range(len(self.weapons)):
                        self.weapons[i] = string.strip(self.weapons[i])
    
                if parser.has_option('bio', 'monsters'):
                    monsters_str = parser.get('bio', 'monsters')
                    self.monsters = monsters_str.split(',')
                    # remove whitespace
                    for i in range(len(self.monsters)):
                        self.monsters[i] = string.strip(self.monsters[i])
    
            if parser.has_section('links'):
    
                if parser.has_option('links', 'left'):
                    self.links['left'] = parser.get('links', 'left')
                else:
                    self.links['left'] = None
    
                if parser.has_option('links', 'right'):
                    self.links['right'] = parser.get('links', 'right')
                else:
                    self.links['right'] = None
    
                if parser.has_option('links', 'up'):
                    self.links['up'] = parser.get('links', 'up')
                else:
                    self.links['up'] = None
    
                if parser.has_option('links', 'down'):
                    self.links['down'] = parser.get('links', 'down')
                else:
                    self.links['down'] = None
            else:
                self.links['left'] = self.links['right'] = None
                self.links['up'] = self.links['down'] = None
    
            if parser.has_section('locations'):
                self.descriptions = parser.items('locations')

    def describe_location(self, being):
        description = random.choice(self.descriptions)
        return description[0] % being.name

    def add_object(self, go):
        self.objects.append(go)

    def del_object(self, go):
        try:
            if go in self.objects:
                self.objects.remove(go)
        except Exception, e:
            raise RuntimeError, "mb_location::del_object-> %s" % e

    def add_being(self, m):
        self.beings.append(m)
        m.location = self

    def del_being(self, m):
        try:
            if m in self.beings:
                self.beings.remove(m)
        except Exception, e:
            raise RuntimeError, "mb_location::del_being-> %s" % e

    def random_object(self):
        return random.choice(self.objects)

    def random_being(self):
        return random.choice(self.beings)

    def object_count(self):
        return len(self.objects)

    def being_count(self):
        return len(self.beings)

    def move_to(self, location, being):
        location.add_being(being)
        self.del_being(being)

    def move_left(self, being):
        left = self.links['left']
        if left:
            self.move_to(left, being)
            return left
        else:
            return False

    def move_right(self, being):
        right = self.links['right']
        if right:
            self.move_to(right, being)
            return right
        else:
            return False

    def move_up(self, being):
        up = self.links['up']
        if up:
            self.move_to(up, being)
            return up
        else:
            return False

    def move_down(self, being):
        down = self.links['down']
        if down:
            self.move_to(down, being)
            return down
        else:
            return False

    def has_name(self, name):
        names = [m.name for m in self.beings]
        if name in names:
            return True
        else:
            return False

    def not_family(self, being):

        not_family = [b for b in self.beings if b.family != being.family]
        return not_family

