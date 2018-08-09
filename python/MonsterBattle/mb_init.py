# -------------------------------------------------------------------------
#  File:    mb_init.py
#  Created: Fri Oct 13 20:51:40 2006
#  Comment: This class encapsulates some of the startup code and global
#           resources.
# -------------------------------------------------------------------------

import os, sys
import time
import random
import glob
import pygame
import pygame.image
from pygame.locals import *

import mb_io # Display, sound, input functions.
from mb_buffer import ScreenBuffer
from mb_win import PyGameWin
from mb_monster import Monster

class GameStartUp(object):

    def __init__(self, gamepack_path):

        self.globals        = None
        self.screen         = None
        self.main_screen    = None
        self.windows        = None
        self.colors         = None
        self.fonts          = None
        self.splash_image   = None
        self.splash_screen  = None
        self.boot_msg_row   = 10
        self.gamepack       = gamepack_path

        self.username = os.environ.get('USER')
        self.hostname = os.environ.get('HOSTNAME')
        self.machtype = os.environ.get('MACHTYPE')

        try:
            self._init_pygame()
        except Exception, e:
            raise RuntimeError, "Error setting up PyGame: %s" % e

        self._init_colors()

        try:
            self._init_globals()
        except Exception, e:
            raise RuntimeError, "Game Start up: %s" % e

    def _init_pygame(self):

        # Initialize Mixer
        pygame.init()

        # Enable PyGame mouse cursor.
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

    def _init_colors(self):

        # Define some colors!
        # Get more from /usr/X11R6/lib/X11/rgb.txt

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

    def _init_globals(self):

        # Storage for global type resources that need to
        # be passed around.  This is bad!!!  Cheaters!!!

        self.globals = dict()

        # Overall screen dimensions.

        self.globals['screen_width'] = 1000
        self.globals['screen_height'] = 600

        # Create root window.
        screen_size = (self.globals['screen_width'], self.globals['screen_height'])
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('MonsterBattle Beta.')

        # Define font sizes.

        self.fonts = { 'title'   : pygame.font.Font(None, 24),
                       'score'   : pygame.font.Font(None, 20),
                       'label'   : pygame.font.Font(None, 18),
                       'text'    : pygame.font.Font(None, 16),
                       'small'   : pygame.font.Font(None, 12),
                       'default' : pygame.font.Font(None, 32),
                       'health'  : pygame.font.Font(None, 100) }

        self.globals['gamedir'] = self.gamepack

        # Main pygame screen.

        self.globals['screen'] = self.screen

        # Define colors, fonts and subwindows.

        self.windows = dict()

        # Create main off-screen rendering buffer.
        self.main_screen = ScreenBuffer(self.screen, self.globals['screen_width'], self.globals['screen_height'])
        self.globals['main_screen'] = self.main_screen

        # Stash fonts and colors with windows too.

        self.windows['fonts'] = self.fonts
        self.windows['colors'] = self.colors

        self.windows['map'] = PyGameWin(self.globals['screen_width'], self.globals['screen_height']-25, 0, 0)
        self.windows['map'].set_bg(self.colors['black'])

        self.globals['map'] = self.windows['map']

        self.globals['player_switched_weapon'] = False

    def start_music(self):

        # Pick a random music selection
        try:
            music_path = os.path.join(self.globals['gamedir'], 'Music')
            music_list = glob.glob(os.path.join(music_path,'*.ogg'))
            music_list += glob.glob(os.path.join(music_path, '*.mp3'))
            if len(music_list) > 0:
                music_file = random.choice(music_list)
                mb_io.play_music(music_file)
        except Exception, e:
            raise RuntimeError, "Error starting music: %s" % e

    def display_splash(self):

        # Load splash screen

        self.splash_screen = ScreenBuffer(self.screen, self.globals['screen_width'], self.globals['screen_height'])

        splash_file = mb_io.splash_file()
        if splash_file:
            imag = pygame.image.load(splash_file)
            self.splash_image = pygame.transform.scale(imag,
                                (self.globals['screen_width'], self.globals['screen_height']))
            splash_pos = (0,0)
            self.splash_screen.buffer.surf.blit(self.splash_image, splash_pos)
            self.splash_screen.render()

        # Start displaying boot messages.

        self.boot_message('MONSTERBATTLE python-2.4 %s' % time.asctime(), 'label')
        mb_io.play_sound('welcome')

    def boot_message(self, msg, font='text'):

        # Display message on splash screen.

        msg = "%s..." % msg

        text = self.fonts[font].render(msg, 1, self.colors['yellow'])
        text_pos = (10, self.boot_msg_row)
        self.splash_screen.buffer.surf.blit(text, text_pos)
        self.splash_screen.render()
        time.sleep(0.5)

        self.boot_msg_row = self.boot_msg_row + 15

    def build_windows(self):

        # Bottom status or control window.

        self.windows['status'] = PyGameWin(self.globals['screen_width'], 25, 0, self.globals['screen_height'] - 25)
        self.windows['status'].set_bg(self.colors['black'])

        # Add the sub windows for the main screen.

        # self.main_screen.add_win(self.windows['god_left'])
        # self.main_screen.add_win(self.windows['god_right'])

        self.main_screen.add_win(self.windows['map'])
        # self.main_screen.add_win(self.windows['locations'])
        # self.main_screen.add_win(self.windows['scroll'])
        self.main_screen.add_win(self.windows['status'])

        # Also store main screen buffer so that
        # other functions can update whole screen if
        # necessary.

        self.windows['main'] = self.main_screen

        # Update the whole screen.
        self.windows['main'].render()

        # Save in case others want to use splash background.

        self.globals['splash'] = self.splash_image


