# -------------------------------------------------------------------------
#  File:    mb_go.py
#  Created: Tue Feb  7 20:27:02 2006
# -------------------------------------------------------------------------

import os
import string
import pygame
from pygame.locals import *
from mb_configparser import mbConfigParser

# GameObject

class GameObject(object):

    """
    This is the base class for all game objects that appear in
    the game.

    """
    def __init__(self, gamedir = None, filename = None):

        self.gamedir = gamedir

        self.name = None
        self.type = None
        self.image_back = None
        #
        # For handling animated sprites for
        # this game object.  (i.e. Any subclass
        # of GameObject should be able to have
        # multi-frame animation.)
        #
        self.image            = None
        self.image_list       = list()
        self.image_frames     = list()
        self.image_back       = None
        self.image_facing     = None
        self.image_size_x     = 50
        self.image_size_y     = 50
        self.image_timer      = 0
        self.image_rate       = 5
        self.current_frame    = 0
        self.num_sprite_frames = 0
        #
        # These are the scaled down images for the playing field.
        #
        self.sprite_list = list()

        # These are even more scaled down images for when the
        # sprites of this game object need to appear smaller
        # than how they look lying on the playing field.
        #
        self.small_sprites = list()

        #
        #

        # Redefine colors here temporarily, even though
        # they are already defined in mb_init.py.

        self.colors = { 'white'     : (255, 255, 255),
                        'black'     : (0, 0, 0),
                        'grey'      : (190, 190, 190),
                        'red'       : (255, 0, 0),
                        'blue'      : (0, 0, 255),
                        'green'     : (0, 255, 0),
                        'yellow'    : (255, 255, 0),
                        'orange'    : (255, 165, 0),
                        'navy'      : (0, 0, 128),
                        'cyan'      : (0, 255, 255),
                        'tan'       : (210, 180, 140),
                        'chocolate' : (210, 105, 30),
                        'brown'     : (165, 42, 42),
                        'pink'      : (255, 192, 203),
                        'maroon'    : (176, 48, 96),
                        'violet'    : (238, 130, 238),
                        'purple'    : (160, 32, 240),
                        'slategrey' : (112, 128, 144),
                        'darkgrey'  : (47, 79, 79) }

        if filename:
            self.read_in_config(filename)
            self.filename = filename
        else:
            self.filename = None
            
        # Current position in current location.

        self.x = 0
        self.y = 0

        # Automatically build the scaled game sprite(s)
        # when this game object is loaded.

        self.build_sprites()

    def read_in_config(self, filename):
        parser = mbConfigParser()
        parser.read(filename)

        if parser.has_section('bio'):
            self.name = parser.get('bio', 'name')
            self.type = parser.get('bio', 'type')

        # This block of code gets the image filename(s) from the config file
        # and stores them in the image_frame list scaled to the proper size.

        if parser.has_option('bio', 'image'):
            images_str = parser.get('bio', 'image')
            self.image_list = images_str.split(',')

            for i in range(len(self.image_list)):
                self.image_list[i] = string.strip(self.image_list[i])
                self.image_frames.append(pygame.image.load(os.path.join(self.gamedir, self.image_list[i])))
                self.image_frames[i] =  pygame.transform.scale(self.image_frames[i], (400, 350))

        # Set image to first filename in list.  This is the full-size image used in the
        # game object display.

        if len(self.image_list) > 0:
            self.image = self.image_list[0]

        # Image background color.  Used to make the background transparent.

        if parser.has_option('bio', 'image_back'):
            self.image_back = parser.get('bio', 'image_back')

        # Image facing direction.  Used to determine correct orientation when
        # moving in a certain direction.  When moving towards opposite direction,
        # the sprite is flipped.  Possible values are 'left' or 'right'.

        if parser.has_option('bio', 'image_facing'):
            self.image_facing = parser.get('bio', 'image_facing')

        # Image dimensions.  Used to define size of sprite(s).

        if parser.has_option('bio', 'image_size_x'):
            self.image_size_x = int(parser.get('bio', 'image_size_x'))

        if parser.has_option('bio', 'image_size_y'):
            self.image_size_y = int(parser.get('bio', 'image_size_y'))

        # Image animation rate.  Factor used to tweak animation speed.

        if parser.has_option('bio', 'image_rate'):
            self.image_rate = int(parser.get('bio', 'image_rate'))

        return parser

    def build_sprites(self):

        """
        Takes list of image(s) specified in the game object file and creates scaled down
        sprite versions for use in the game screen.  Attempts to make background transparent
        by using 'image_back' specified in game object file.
        """

        try:
            for image in self.image_list:
                tmp_image  = pygame.image.load(os.path.join(self.gamedir, image))
                tmp_sprite = pygame.transform.scale(tmp_image, (self.image_size_x, self.image_size_y))
                if self.image_back is not None:
                    tmp_sprite.set_colorkey(self.colors[self.image_back])
                self.sprite_list.append(tmp_sprite)

                # scale even smaller for smaller sprite list.
                tmp_sprite = pygame.transform.scale(tmp_image,
                                                    ((int(self.image_size_x*0.70)),
                                                     (int(self.image_size_y*0.70))))
                if self.image_back is not None:
                    tmp_sprite.set_colorkey(self.colors[self.image_back])
                self.small_sprites.append(tmp_sprite)
                del tmp_image

            self.num_sprite_frames = len(self.sprite_list)
        except Exception, e:
            raise RuntimeError, "build_sprites-> %s" % e

    def get_sprite_frame(self):

        """
        Return current sprite frame and advance frame # if necessary.
        """

        try:
            if self.num_sprite_frames == 1:
                return self.sprite_list[0]
            else:
                self.image_timer += 1
                if self.image_timer > self.image_rate:
                    self.current_frame = (self.current_frame + 1) % self.num_sprite_frames
                    self.image_timer = 0
                return self.sprite_list[self.current_frame]

        except Exception, e:
            raise RuntimeError, "get_sprite_frame-> %s" % e

    def get_small_sprite_frame(self):

        """
        Return current small frame and advance frame # if necessary.
        """

        try:
            if self.num_sprite_frames == 1:
                return self.small_sprites[0]
            else:
                self.image_timer += 1
                if self.image_timer > self.image_rate:
                    self.current_frame = (self.current_frame + 1) % self.num_sprite_frames
                    self.image_timer = 0
                return self.small_sprites[self.current_frame]

        except Exception, e:
            raise RuntimeError, "get_small_sprite_frame-> %s" % e

    def debug_game_object(self, f):

        print >>f
        print >>f, "Name = %s" % self.name
        print >>f, "Type = %s" % self.type
        print >>f, "image_list: "
        print >>f, self.image_list
        print >>f, "image_back = %s" % self.image_back
        print >>f, "image_timer = %d" % self.image_timer
        print >>f, "image_rate = %d" % self.image_rate
        print >>f, "num sprite frames = %d" % self.num_sprite_frames
        print




